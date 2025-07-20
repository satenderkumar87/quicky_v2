"""
Basic vision module for extracting UI layout from images.
This is a simplified version that focuses on basic element detection.
"""

import cv2
import numpy as np
from PIL import Image
import base64
import io
from typing import List, Dict, Any
import os

class VisionProcessor:
    def __init__(self):
        self.supported_formats = ['.png', '.jpg', '.jpeg']
    
    def process_image(self, image_path: str) -> Dict[str, Any]:
        """
        Process a single image and extract basic layout information.
        For now, this is a simplified version that will be enhanced later.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        height, width = image.shape[:2]
        
        # Basic layout detection (simplified)
        layout_elements = self._detect_basic_elements(image)
        
        # Convert image to base64 for OpenAI Vision API
        image_base64 = self._image_to_base64(image_path)
        
        return {
            'filename': os.path.basename(image_path),
            'dimensions': {'width': width, 'height': height},
            'elements': layout_elements,
            'image_base64': image_base64
        }
    
    def _detect_basic_elements(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """
        Basic element detection using simple computer vision techniques.
        This will be enhanced with more sophisticated methods later.
        """
        elements = []
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect rectangular regions (potential buttons, cards, etc.)
        contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for i, contour in enumerate(contours):
            # Filter small contours
            area = cv2.contourArea(contour)
            if area < 1000:  # Minimum area threshold
                continue
            
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            
            # Classify element type based on dimensions
            element_type = self._classify_element(w, h, area)
            
            elements.append({
                'id': f'element_{i}',
                'type': element_type,
                'bbox': {'x': x, 'y': y, 'width': w, 'height': h},
                'area': area
            })
        
        return elements
    
    def _classify_element(self, width: int, height: int, area: int) -> str:
        """
        Simple element classification based on dimensions.
        """
        aspect_ratio = width / height if height > 0 else 1
        
        if aspect_ratio > 3:
            return 'navbar'
        elif aspect_ratio > 2:
            return 'button'
        elif aspect_ratio < 0.5:
            return 'sidebar'
        elif area > 50000:
            return 'container'
        else:
            return 'component'
    
    def _image_to_base64(self, image_path: str) -> str:
        """Convert image to base64 string for OpenAI Vision API."""
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def process_multiple_images(self, input_dir: str) -> List[Dict[str, Any]]:
        """Process all images in the input directory."""
        results = []
        
        if not os.path.exists(input_dir):
            print(f"Input directory not found: {input_dir}")
            return results
        
        for filename in os.listdir(input_dir):
            if any(filename.lower().endswith(ext) for ext in self.supported_formats):
                image_path = os.path.join(input_dir, filename)
                try:
                    result = self.process_image(image_path)
                    results.append(result)
                    print(f"Processed: {filename}")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
        
        return results
