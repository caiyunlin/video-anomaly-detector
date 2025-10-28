"""
Azure AI Foundry integration module for video anomaly detection.
"""
import os
import json
import logging
from typing import List, Dict, Any, Optional
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, ClientSecretCredential
import base64

logger = logging.getLogger(__name__)

class AzureAIVideoAnalyzer:
    """Azure AI Foundry video analyzer using GPT-4V."""
    
    def __init__(self):
        """Initialize the Azure AI client."""
        self.api_key = os.environ.get('AZURE_OPENAI_API_KEY')
        self.endpoint = os.environ.get('AZURE_OPENAI_ENDPOINT')
        self.api_version = os.environ.get('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')
        self.deployment_name = os.environ.get('AZURE_OPENAI_DEPLOYMENT_NAME', 'gpt-4-vision-preview')
        
        # Optional: Use service principal for authentication
        self.tenant_id = os.environ.get('AZURE_TENANT_ID')
        self.client_id = os.environ.get('AZURE_CLIENT_ID')
        self.client_secret = os.environ.get('AZURE_CLIENT_SECRET')
        
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Azure OpenAI client with appropriate authentication."""
        try:
            # Validate required configuration
            if not self.endpoint:
                raise ValueError(
                    "Azure OpenAI endpoint is required. Please set AZURE_OPENAI_ENDPOINT environment variable."
                )
            
            if not self.deployment_name:
                raise ValueError(
                    "Azure OpenAI deployment name is required. Please set AZURE_OPENAI_DEPLOYMENT_NAME environment variable."
                )
            
            if not self.api_key:
                raise ValueError(
                    "Azure OpenAI API key is required. Please set AZURE_OPENAI_API_KEY environment variable."
                )
            
            logger.info(f"Initializing Azure OpenAI client with endpoint: {self.endpoint}")
            logger.info(f"Using deployment: {self.deployment_name}")
            
            # Use API key authentication only for now
            self.client = AzureOpenAI(
                api_key=self.api_key,
                api_version=self.api_version,
                azure_endpoint=self.endpoint
            )
            logger.info("Initialized Azure OpenAI client with API key authentication")
        except Exception as e:
            logger.error(f"Failed to initialize Azure OpenAI client: {e}")
            logger.error("Please check your Azure OpenAI configuration:")
            logger.error("- AZURE_OPENAI_ENDPOINT should be set to your Azure OpenAI resource endpoint")
            logger.error("- AZURE_OPENAI_API_KEY should be set to your API key (or use managed identity)")
            logger.error("- AZURE_OPENAI_DEPLOYMENT_NAME should be set to your model deployment name")
            raise
    
    def analyze_frames(self, frames: List[Dict], anomaly_prompt: str, video_info: Dict) -> Dict[str, Any]:
        """
        Analyze video frames for anomalies using Azure OpenAI GPT-4V.
        
        Args:
            frames: List of frame data with base64 encoded images
            anomaly_prompt: User-specified anomaly types to detect
            video_info: Video metadata information
            
        Returns:
            Dictionary containing analysis results
        """
        if not self.client:
            raise RuntimeError("Azure OpenAI client is not initialized")
        
        try:
            # Construct the analysis prompt
            system_prompt = self._create_analysis_prompt(anomaly_prompt, video_info)
            
            # Prepare message content with frames
            content = [{"type": "text", "text": system_prompt}]
            
            # Add frames (limit to avoid token limits)
            max_frames_for_analysis = min(len(frames), 10)
            for i, frame in enumerate(frames[:max_frames_for_analysis]):
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{frame['image_data']}",
                        "detail": "high"  # Use high detail for better analysis
                    }
                })
                
                # Add frame context
                content.append({
                    "type": "text",
                    "text": f"Frame {i+1}/{max_frames_for_analysis} - Timestamp: {frame['timestamp']:.2f}s"
                })
            
            # Make the API call
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[{
                    "role": "user",
                    "content": content
                }],
                max_tokens=2000,
                temperature=0.1,  # Low temperature for consistent analysis
                top_p=0.9
            )
            
            # Parse the response
            result_text = response.choices[0].message.content
            logger.info(f"Received analysis result: {result_text[:200]}...")
            
            # Try to parse as JSON
            try:
                result = json.loads(result_text)
                # Validate required fields
                result = self._validate_analysis_result(result)
            except (json.JSONDecodeError, KeyError) as e:
                logger.warning(f"Failed to parse JSON result: {e}, using fallback format")
                result = self._create_fallback_result(result_text, anomaly_prompt)
            
            # Add metadata
            result['analysis_metadata'] = {
                'frames_analyzed': max_frames_for_analysis,
                'total_frames_available': len(frames),
                'model_used': self.deployment_name,
                'api_version': self.api_version
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error during video analysis: {e}")
            return self._create_error_result(str(e))
    
    def _create_analysis_prompt(self, anomaly_prompt: str, video_info: Dict) -> str:
        """Create the analysis prompt for GPT-4V."""
        return f"""You are a professional surveillance video anomaly detection AI expert. Please analyze the following video frame sequence to detect whether there are user-specified anomalous situations.

**Target Anomaly Types to Detect:** {anomaly_prompt}

**Video Information:**
- Total Frames: {video_info['total_frames']}
- Frame Rate: {video_info['fps']:.2f} FPS
- Video Duration: {video_info['duration']:.2f} seconds
- Analyzed Frames: {video_info['extracted_frames']}

**Analysis Requirements:**
1. Carefully observe the content of each frame
2. Identify whether there are user-specified types of anomalies
3. Evaluate the severity and confidence of anomalies
4. Determine the specific time points when anomalies occur

**Output Format (must be valid JSON):**
{{
    "has_anomaly": true/false,
    "confidence_score": 0.0-1.0,
    "anomaly_type": "detected anomaly type",
    "severity": "low/medium/high",
    "detected_frames": [1, 3, 5],
    "timestamps": [1.2, 3.4, 5.6],
    "description": "detailed description of detected anomalies, including specific manifestations, locations and characteristics",
    "evidence": "specific visual evidence supporting anomaly judgment",
    "recommendations": "recommended response measures",
    "false_positive_risk": 0.0-1.0
}}

if user using Chinese, then you will reply in Chinese also.

Please conduct professional and objective analysis based on the video frames."""

    def _validate_analysis_result(self, result: Dict) -> Dict:
        """Validate and ensure required fields in analysis result."""
        required_fields = {
            'has_anomaly': False,
            'confidence_score': 0.0,
            'anomaly_type': 'No anomaly detected',
            'detected_frames': [],
            'timestamps': [],
            'description': 'Analysis completed',
            'recommendations': 'No special recommendations'
        }
        
        # Ensure all required fields exist
        for field, default_value in required_fields.items():
            if field not in result:
                result[field] = default_value
        
        # Validate data types and ranges
        result['confidence_score'] = max(0.0, min(1.0, float(result.get('confidence_score', 0.0))))
        result['has_anomaly'] = bool(result.get('has_anomaly', False))
        
        if not isinstance(result['detected_frames'], list):
            result['detected_frames'] = []
        
        if not isinstance(result['timestamps'], list):
            result['timestamps'] = []
            
        return result
    
    def _create_fallback_result(self, result_text: str, anomaly_prompt: str) -> Dict:
        """Create a fallback result when JSON parsing fails."""
        return {
            'has_anomaly': 'anomaly' in result_text.lower() or 'abnormal' in result_text.lower(),
            'confidence_score': 0.5,
            'anomaly_type': anomaly_prompt,
            'detected_frames': [],
            'timestamps': [],
            'description': result_text,
            'recommendations': '请人工复核分析结果',
            'analysis_note': 'AI返回的结果格式不标准，已进行自动处理'
        }
    
    def _create_error_result(self, error_message: str) -> Dict:
        """Create an error result format."""
        return {
            'error': error_message,
            'has_anomaly': False,
            'confidence_score': 0.0,
            'anomaly_type': '分析失败',
            'detected_frames': [],
            'timestamps': [],
            'description': f'分析过程中发生错误: {error_message}',
            'recommendations': '请检查配置并重试'
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """Test the connection to Azure OpenAI service."""
        try:
            if not self.client:
                return {'success': False, 'error': 'Client not initialized'}
            
            # Simple test call
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[{
                    "role": "user",
                    "content": "你好，请回复'连接测试成功'"
                }],
                max_tokens=50,
                temperature=0.1
            )
            
            result_text = response.choices[0].message.content
            return {
                'success': True,
                'response': result_text,
                'model': self.deployment_name,
                'endpoint': self.endpoint
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'endpoint': self.endpoint
            }