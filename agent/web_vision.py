"""
Web-based vision processor that works directly with uploaded files from the web UI.
Replaces directory-based image processing with direct file handling.
"""

import cv2
import numpy as np
from PIL import Image
import base64
import io
from typing import List, Dict, Any, Optional
import os

class WebVisionProcessor:
    def __init__(self):
        self.supported_formats = ['png', 'jpg', 'jpeg', 'gif', 'webp']
    
    def process_uploaded_files(self, uploaded_files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process uploaded files directly from web UI.
        
        Args:
            uploaded_files: List of file objects with 'filename', 'content', and 'content_type'
        
        Returns:
            List of processed image data
        """
        processed_images = []
        
        for file_data in uploaded_files:
            try:
                image_data = self._process_single_file(file_data)
                if image_data:
                    processed_images.append(image_data)
            except Exception as e:
                print(f"Error processing {file_data.get('filename', 'unknown')}: {e}")
                continue
        
        return processed_images
    
    def _process_single_file(self, file_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process a single uploaded file."""
        filename = file_data.get('filename', 'unknown.png')
        file_content = file_data.get('content')
        
        if not file_content:
            return None
        
        # Convert file content to image
        try:
            # If content is already bytes
            if isinstance(file_content, bytes):
                image_bytes = file_content
            else:
                # If it's a file object, read it
                image_bytes = file_content.read()
                file_content.seek(0)  # Reset file pointer
            
            # Open image with PIL
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Get image dimensions
            width, height = image.size
            
            # Convert to base64 for AI processing
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG", quality=85)
            image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            # Basic element detection (simplified for web processing)
            elements = self._detect_ui_elements_simple(image)
            
            return {
                'filename': filename,
                'dimensions': {'width': width, 'height': height},
                'elements': elements,
                'image_base64': image_base64,
                'file_size': len(image_bytes),
                'format': image.format or 'JPEG'
            }
            
        except Exception as e:
            print(f"Error processing image {filename}: {e}")
            return None
    
    def _detect_ui_elements_simple(self, image: Image.Image) -> List[Dict[str, Any]]:
        """
        Simplified UI element detection for web processing.
        Returns basic element information without heavy computer vision.
        """
        width, height = image.size
        
        # Basic heuristic-based element detection
        elements = []
        
        # Analyze image characteristics
        image_array = np.array(image)
        
        # Detect potential UI regions based on color analysis
        gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        
        # Find contours for basic shape detection
        try:
            # Apply threshold to find distinct regions
            _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Process significant contours
            for i, contour in enumerate(contours[:10]):  # Limit to top 10
                area = cv2.contourArea(contour)
                if area > (width * height * 0.01):  # At least 1% of image
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Classify element type based on dimensions and position
                    element_type = self._classify_element(x, y, w, h, width, height)
                    
                    elements.append({
                        'type': element_type,
                        'bbox': {'x': x, 'y': y, 'width': w, 'height': h},
                        'area': area,
                        'confidence': min(0.8, area / (width * height) * 10)
                    })
        
        except Exception as e:
            print(f"Error in element detection: {e}")
        
        # If no elements detected, add default elements based on image analysis
        if not elements:
            elements = self._generate_default_elements(width, height)
        
        return elements
    
    def _classify_element(self, x: int, y: int, w: int, h: int, img_width: int, img_height: int) -> str:
        """Classify UI element type based on position and dimensions."""
        aspect_ratio = w / h if h > 0 else 1
        relative_width = w / img_width
        relative_height = h / img_height
        relative_y = y / img_height
        
        # Classification logic
        if relative_y < 0.15 and relative_width > 0.7:
            return 'navbar'
        elif aspect_ratio > 3 and relative_width > 0.5:
            return 'header'
        elif aspect_ratio > 2 and w < img_width * 0.3:
            return 'button'
        elif relative_width > 0.8 and relative_height > 0.3:
            return 'container'
        elif aspect_ratio < 0.5:
            return 'sidebar'
        elif 0.8 < aspect_ratio < 1.2:
            return 'card'
        else:
            return 'component'
    
    def _generate_default_elements(self, width: int, height: int) -> List[Dict[str, Any]]:
        """Generate default elements when detection fails."""
        return [
            {
                'type': 'container',
                'bbox': {'x': 0, 'y': 0, 'width': width, 'height': height},
                'area': width * height,
                'confidence': 0.5
            },
            {
                'type': 'header',
                'bbox': {'x': 0, 'y': 0, 'width': width, 'height': int(height * 0.15)},
                'area': width * int(height * 0.15),
                'confidence': 0.6
            },
            {
                'type': 'content',
                'bbox': {'x': 0, 'y': int(height * 0.15), 'width': width, 'height': int(height * 0.85)},
                'area': width * int(height * 0.85),
                'confidence': 0.6
            }
        ]
    
    def validate_uploaded_file(self, file_data: Dict[str, Any]) -> bool:
        """Validate that uploaded file is a supported image format."""
        filename = file_data.get('filename', '').lower()
        
        # Check file extension
        if not any(filename.endswith(f'.{fmt}') for fmt in self.supported_formats):
            return False
        
        # Check if file has content
        content = file_data.get('content')
        if not content:
            return False
        
        # Try to open as image
        try:
            if isinstance(content, bytes):
                image_bytes = content
            else:
                image_bytes = content.read()
                content.seek(0)
            
            Image.open(io.BytesIO(image_bytes))
            return True
        except Exception:
            return False
    
    def get_image_info(self, file_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get basic information about an uploaded image."""
        try:
            content = file_data.get('content')
            if isinstance(content, bytes):
                image_bytes = content
            else:
                image_bytes = content.read()
                content.seek(0)
            
            image = Image.open(io.BytesIO(image_bytes))
            
            return {
                'filename': file_data.get('filename', 'unknown'),
                'format': image.format,
                'mode': image.mode,
                'size': image.size,
                'file_size': len(image_bytes)
            }
        except Exception as e:
            return {'error': str(e)}

def process_web_uploads(uploaded_files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Main function to process uploaded files from web UI.
    
    Args:
        uploaded_files: List of uploaded file data
    
    Returns:
        List of processed image data ready for AI generation
    """
    processor = WebVisionProcessor()
    return processor.process_uploaded_files(uploaded_files)
