import os
import secrets
from flask import Flask, request, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import cv2
import base64
import tempfile
import json
import logging
from azure_ai_analyzer import AzureAIVideoAnalyzer

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(16))
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_CONTENT_LENGTH', 50 * 1024 * 1024))  # 50MB

# Allowed video extensions
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}

# Validate Azure OpenAI configuration
def validate_azure_config():
    """Validate Azure OpenAI configuration before initializing."""
    required_vars = {
        'AZURE_OPENAI_ENDPOINT': os.environ.get('AZURE_OPENAI_ENDPOINT'),
        'AZURE_OPENAI_DEPLOYMENT_NAME': os.environ.get('AZURE_OPENAI_DEPLOYMENT_NAME', 'gpt-4-vision-preview')
    }
    
    missing_vars = []
    for var_name, var_value in required_vars.items():
        if not var_value or var_value == 'your_endpoint_here' or var_value == 'your-resource-name.openai.azure.com':
            missing_vars.append(var_name)
    
    if missing_vars:
        logger.error("❌ Missing or invalid Azure OpenAI configuration:")
        for var in missing_vars:
            logger.error(f"   - {var}")
        logger.error("📋 Please update your .env file with valid Azure OpenAI configuration:")
        logger.error("   - AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/")
        logger.error("   - AZURE_OPENAI_API_KEY=your-api-key")
        logger.error("   - AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4-vision-preview")
        logger.error("🔗 See .env.example for configuration template")
        return False
    
    logger.info("✅ Azure OpenAI configuration validated")
    return True

# Initialize Azure AI analyzer with validation
try:
    if not validate_azure_config():
        logger.warning("⚠️ Running with incomplete Azure OpenAI configuration - some features may not work")
        ai_analyzer = None
    else:
        ai_analyzer = AzureAIVideoAnalyzer()
        logger.info("✅ Azure AI analyzer initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize Azure AI analyzer: {e}")
    ai_analyzer = None

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_frames_from_video(video_path, max_frames=10):
    """Extract frames from video for analysis."""
    frames = []
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise ValueError("Cannot open video file")
    
    # Get video properties
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps if fps > 0 else 0
    
    # Calculate frame intervals for sampling
    if total_frames <= max_frames:
        frame_interval = 1
    else:
        frame_interval = total_frames // max_frames
    
    frame_count = 0
    extracted_count = 0
    
    while cap.isOpened() and extracted_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_count % frame_interval == 0:
            # Convert frame to base64
            _, buffer = cv2.imencode('.jpg', frame)
            frame_b64 = base64.b64encode(buffer).decode('utf-8')
            frames.append({
                'frame_number': frame_count,
                'timestamp': frame_count / fps if fps > 0 else 0,
                'image_data': frame_b64
            })
            extracted_count += 1
            
        frame_count += 1
    
    cap.release()
    
    return frames, {
        'total_frames': total_frames,
        'fps': fps,
        'duration': duration,
        'extracted_frames': len(frames)
    }



@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')

@app.route('/config-status')
def config_status():
    """Configuration status page."""
    return render_template('config-status.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    """Handle video upload and analysis."""
    try:
        # Check if video file is present
        if 'video' not in request.files:
            return jsonify({'error': 'No video file selected'}), 400
        
        file = request.files['video']
        anomaly_prompt = request.form.get('anomaly_prompt', '').strip()
        
        if file.filename == '':
            return jsonify({'error': 'No video file selected'}), 400
        
        if not anomaly_prompt:
            return jsonify({'error': 'Please enter the anomaly types to detect'}), 400
        
        if file and allowed_file(file.filename):
            # Save the uploaded file
            filename = secure_filename(file.filename)
            # Add timestamp to avoid filename conflicts
            import time
            timestamp = str(int(time.time()))
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                # Extract frames from video
                logger.info(f"Processing video: {filename}")
                frames, video_info = extract_frames_from_video(filepath)
                
                # Analyze with Azure AI
                if ai_analyzer is None:
                    return jsonify({
                        'error': 'Azure AI analyzer not properly configured. Please check Azure OpenAI configuration.',
                        'config_help': {
                            'required_vars': [
                                'AZURE_OPENAI_ENDPOINT',
                                'AZURE_OPENAI_API_KEY',
                                'AZURE_OPENAI_DEPLOYMENT_NAME'
                            ],
                            'example_endpoint': 'https://your-resource-name.openai.azure.com/'
                        }
                    }), 500
                
                logger.info("Starting video analysis with Azure AI Foundry")
                analysis_result = ai_analyzer.analyze_frames(frames, anomaly_prompt, video_info)
                
                # Clean up the uploaded file
                os.remove(filepath)
                
                logger.info("Video analysis completed successfully")
                return jsonify({
                    'success': True,
                    'video_info': video_info,
                    'analysis': analysis_result,
                    'prompt_used': anomaly_prompt
                })
                
            except Exception as e:
                logger.error(f"Error processing video: {str(e)}")
                # Clean up the uploaded file in case of error
                if os.path.exists(filepath):
                    os.remove(filepath)
                return jsonify({'error': f'Video processing failed: {str(e)}'}), 500
        
        else:
            return jsonify({'error': 'Unsupported file format. Please upload MP4, AVI, MOV, MKV or WEBM video files'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for container deployment."""
    config_status = {
        'azure_openai_endpoint': bool(os.environ.get('AZURE_OPENAI_ENDPOINT')),
        'azure_openai_api_key': bool(os.environ.get('AZURE_OPENAI_API_KEY')),
        'azure_openai_deployment': bool(os.environ.get('AZURE_OPENAI_DEPLOYMENT_NAME')),
        'ai_analyzer_initialized': ai_analyzer is not None
    }
    
    overall_status = 'healthy' if all(config_status.values()) else 'degraded'
    
    return jsonify({
        'status': overall_status,
        'service': 'video-anomaly-detector',
        'configuration': config_status,
        'message': 'All systems operational' if overall_status == 'healthy' else 'Some configuration missing'
    })

@app.route('/test-connection')
def test_azure_connection():
    """Test Azure AI connection."""
    try:
        if ai_analyzer is None:
            return jsonify({
                'success': False,
                'error': 'Azure AI analyzer not initialized',
                'help': 'Please check Azure OpenAI configuration in .env file'
            }), 500
        
        result = ai_analyzer.test_connection()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'help': 'Please verify your Azure OpenAI endpoint and credentials'
        }), 500

if __name__ == '__main__':
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Run the app
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=True)