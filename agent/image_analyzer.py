"""
Enhanced image analyzer that uses LLM vision to understand UI designs and determine page types.
"""

import openai
import base64
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class ImageAnalyzer:
    """Analyzes images using LLM vision to determine page type and content."""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def analyze_ui_design(self, image_data: bytes, filename: str) -> Dict[str, Any]:
        """Analyze UI design image to determine page type and content."""
        try:
            # Convert image to base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Create analysis prompt
            prompt = """
            Analyze this UI design/mockup/screenshot and determine:
            
            1. What type of page/screen is this? (login, dashboard, profile, homepage, product listing, form, etc.)
            2. What are the main UI elements visible? (forms, buttons, navigation, cards, tables, etc.)
            3. What is the primary purpose/function of this interface?
            4. What would be an appropriate React component name for this page?
            
            Respond in JSON format:
            {
                "page_type": "login|dashboard|profile|homepage|product|form|data|generic",
                "page_description": "Brief description of what this page does",
                "main_elements": ["list", "of", "main", "ui", "elements"],
                "suggested_component_name": "SuggestedComponentName",
                "layout_style": "description of the layout and design style",
                "primary_function": "what the user would do on this page"
            }
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",  # GPT-4 with vision
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500,
                temperature=0.1
            )
            
            # Parse the response
            analysis_text = response.choices[0].message.content
            
            # Try to extract JSON from the response
            import json
            import re
            
            # Find JSON in the response
            json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
            else:
                # Fallback analysis
                analysis = self._create_fallback_analysis(analysis_text, filename)
            
            print(f"🔍 Image analysis for {filename}:")
            print(f"   Page type: {analysis.get('page_type', 'unknown')}")
            print(f"   Description: {analysis.get('page_description', 'N/A')}")
            print(f"   Elements: {analysis.get('main_elements', [])}")
            
            return analysis
            
        except Exception as e:
            print(f"⚠️  Image analysis failed: {e}")
            return self._create_fallback_analysis("", filename)
    
    def _create_fallback_analysis(self, analysis_text: str, filename: str) -> Dict[str, Any]:
        """Create fallback analysis when vision analysis fails."""
        # Try to infer from analysis text or filename
        text_lower = analysis_text.lower()
        filename_lower = filename.lower()
        
        if 'login' in text_lower or 'sign' in text_lower or 'auth' in text_lower:
            page_type = 'login'
        elif 'dashboard' in text_lower or 'admin' in text_lower or 'metrics' in text_lower:
            page_type = 'dashboard'
        elif 'profile' in text_lower or 'account' in text_lower or 'user' in text_lower:
            page_type = 'profile'
        elif 'home' in text_lower or 'landing' in text_lower or 'hero' in text_lower:
            page_type = 'homepage'
        elif 'product' in text_lower or 'shop' in text_lower or 'store' in text_lower:
            page_type = 'product'
        elif 'form' in text_lower or 'contact' in text_lower:
            page_type = 'form'
        elif 'table' in text_lower or 'data' in text_lower or 'list' in text_lower:
            page_type = 'data'
        else:
            page_type = 'generic'
        
        return {
            'page_type': page_type,
            'page_description': f'UI interface from {filename}',
            'main_elements': ['container', 'content'],
            'suggested_component_name': f'{page_type.title()}Page',
            'layout_style': 'modern web interface',
            'primary_function': f'user interaction for {page_type} functionality'
        }

def analyze_image_for_page_type(image_data: bytes, filename: str) -> Dict[str, Any]:
    """Convenience function to analyze an image and determine page type."""
    analyzer = ImageAnalyzer()
    return analyzer.analyze_ui_design(image_data, filename)
