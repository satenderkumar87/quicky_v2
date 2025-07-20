"""
AI Orchestrator for converting UI layouts to React components using OpenAI.
Updated to use current OpenAI models (gpt-4o) and comprehensive code validation with clean logging.
"""

import openai
from typing import List, Dict, Any
import json
import os
from dotenv import load_dotenv
from .model_checker import ModelChecker
from .template_generator import create_error_free_component
from .code_cleaner import clean_generated_code
from .code_validator import validate_generated_code, create_safe_component
from .logger import log_processing, log_success, log_error, clean_print
from .component_namer import generate_smart_component_name

load_dotenv()

class AIOrchestrator:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Use model checker to get best available models
        model_checker = ModelChecker()
        best_models = model_checker.get_best_models()
        
        self.model = best_models['vision']  # GPT-4o has built-in vision capabilities
        self.text_model = best_models['text']  # Using gpt-4o for both vision and text
        
        clean_print(f"🤖 Using models: Vision={self.model}, Text={self.text_model}")
    
    def analyze_layout_with_vision(self, image_data: Dict[str, Any], project_description: str = "") -> Dict[str, Any]:
        """
        Use OpenAI Vision API to analyze the UI layout from image.
        """
        try:
            messages = [
                {
                    "role": "system",
                    "content": """You are a UI/UX expert. Analyze the provided UI screenshot and extract detailed layout information. 
                    Return a JSON structure describing all UI elements, their positions, types, and relationships.
                    Focus on identifying: buttons, inputs, cards, navigation, headers, content areas, etc."""
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Analyze this UI screenshot and describe its layout structure. Project context: {project_description}"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data['image_base64']}",
                                "detail": "high"  # Use high detail for better analysis
                            }
                        }
                    ]
                }
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1500,  # Increased for more detailed analysis
                temperature=0.1   # Lower temperature for more consistent analysis
            )
            
            # Parse the response to extract layout information
            layout_description = response.choices[0].message.content
            
            return {
                'filename': image_data['filename'],
                'layout_description': layout_description,
                'basic_elements': image_data['elements'],
                'dimensions': image_data['dimensions']
            }
            
        except Exception as e:
            print(f"Error in vision analysis: {e}")
            return {
                'filename': image_data['filename'],
                'layout_description': f"Basic layout with {len(image_data['elements'])} detected elements",
                'basic_elements': image_data['elements'],
                'dimensions': image_data['dimensions']
            }
    
    def generate_react_component(self, layout_info: Dict[str, Any], project_description: str = "") -> str:
        """
        Generate React component code from layout information with comprehensive validation.
        """
        # Generate smart component name
        component_name = generate_smart_component_name(
            filename=layout_info.get('filename', 'unknown'),
            elements=layout_info.get('basic_elements', []),
            project_description=project_description
        )
        
        prompt = self._create_code_generation_prompt(layout_info, project_description)
        
        try:
            response = self.client.chat.completions.create(
                model=self.text_model,
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are an expert React developer. Generate clean, production-ready React components using:
                        - Modern React with functional components and hooks
                        - Tailwind CSS for styling (latest version)
                        - Responsive design principles (mobile-first)
                        - Accessible HTML structure with proper ARIA labels
                        - Clean, readable code with proper component structure
                        - Modern JavaScript/JSX syntax
                        
                        CRITICAL REQUIREMENTS:
                        - Component name MUST be: {component_name}
                        - Return ONLY valid JavaScript/JSX code
                        - NO markdown code blocks (```jsx or ```)
                        - NO explanatory text or comments outside the code
                        - NO feature descriptions or documentation
                        - NO text after the export statement
                        - Use simple className strings, avoid complex template literals
                        - Ensure all JSX is properly closed and formatted
                        
                        The code must be ready to save directly as a .jsx file and build without errors."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=2500,
                temperature=0.05  # Very low temperature for maximum consistency
            )
            
            raw_code = response.choices[0].message.content
            
            # Clean the AI-generated code
            cleaned_code = clean_generated_code(raw_code)
            
            # Ensure the component name is correct in the code
            cleaned_code = self._fix_component_name_in_code(cleaned_code, component_name)
            
            # Validate the cleaned code
            is_valid, final_code, errors = validate_generated_code(cleaned_code, component_name)
            
            if is_valid:
                log_success(f"Generated valid React component: {component_name}")
                return final_code
            else:
                log_error(f"AI-generated code had issues: {errors}")
                clean_print("🔄 Using error-free fallback component")
                return self._generate_fallback_component(layout_info, component_name)
            
        except Exception as e:
            log_error(f"Error generating React component: {e}")
            return self._generate_fallback_component(layout_info, component_name)
    
    def _create_code_generation_prompt(self, layout_info: Dict[str, Any], project_description: str) -> str:
        """Create a detailed prompt for code generation."""
        filename = layout_info.get('filename', 'unknown')
        elements = layout_info.get('basic_elements', [])
        dimensions = layout_info.get('dimensions', {})
        
        # Analyze elements to create specific layout requirements
        element_types = [elem.get('type', 'unknown') for elem in elements]
        
        # Determine page type and create specific layouts
        page_type = "generic"
        specific_layout = ""
        
        if 'login' in filename.lower() or 'signin' in filename.lower():
            page_type = "login"
            specific_layout = """
            Create a LOGIN PAGE with:
            - Centered login form (max-width: 400px)
            - Email and password input fields
            - "Sign In" button (blue, full width)
            - "Forgot Password?" link
            - Optional: Social login buttons (Google, GitHub)
            - Clean, minimal design with white card on gray background
            """
        elif 'dashboard' in filename.lower() or 'admin' in filename.lower():
            page_type = "dashboard"
            specific_layout = """
            Create a DASHBOARD PAGE with:
            - Top navigation bar with logo and user menu
            - Sidebar navigation (if space allows) or mobile menu
            - Grid of metric cards (4 cards showing numbers/stats)
            - Charts/graphs section (use placeholder rectangles)
            - Recent activity table or list
            - Quick action buttons
            - Professional admin interface styling
            """
        elif 'profile' in filename.lower() or 'account' in filename.lower():
            page_type = "profile"
            specific_layout = """
            Create a USER PROFILE PAGE with:
            - Profile header with avatar placeholder and name
            - Tabs or sections: Personal Info, Settings, Security
            - Form fields for user information (name, email, bio)
            - Profile picture upload area
            - Save/Update buttons
            - Account settings toggles
            - Clean, user-friendly design
            """
        elif 'home' in filename.lower() or 'landing' in filename.lower():
            page_type = "homepage"
            specific_layout = """
            Create a HOMEPAGE/LANDING PAGE with:
            - Hero section with large heading and CTA button
            - Navigation header with menu items
            - Features section (3-4 feature cards)
            - Testimonials or benefits section
            - Footer with links and contact info
            - Modern, marketing-focused design
            """
        elif 'product' in filename.lower() or 'shop' in filename.lower():
            page_type = "ecommerce"
            specific_layout = """
            Create an E-COMMERCE PAGE with:
            - Product grid layout (3-4 columns)
            - Product cards with image, title, price
            - Filter sidebar or top filters
            - Search bar
            - Shopping cart icon with count
            - Pagination or "Load More" button
            - E-commerce styling with product focus
            """
        else:
            # Analyze elements to determine layout
            if 'form' in element_types:
                page_type = "form"
                specific_layout = """
                Create a FORM PAGE with:
                - Centered form layout
                - Multiple input fields with labels
                - Form validation styling
                - Submit and Cancel buttons
                - Progress indicator (if multi-step)
                - Clean, form-focused design
                """
            elif 'table' in element_types:
                page_type = "data"
                specific_layout = """
                Create a DATA TABLE PAGE with:
                - Data table with headers and sample rows
                - Search and filter controls
                - Pagination controls
                - Action buttons (Add, Edit, Delete)
                - Export/Import options
                - Professional data management interface
                """
            elif 'card' in element_types:
                page_type = "cards"
                specific_layout = """
                Create a CARD-BASED PAGE with:
                - Grid of content cards
                - Each card with image, title, description
                - Hover effects on cards
                - Filter or category tabs
                - Load more functionality
                - Modern card-based layout
                """
            else:
                specific_layout = """
                Create a CONTENT PAGE with:
                - Header section with title
                - Main content area with sections
                - Sidebar with navigation or info
                - Call-to-action buttons
                - Footer section
                - Clean, content-focused design
                """
        
        return f"""
        Generate a React component for a {page_type.upper()} PAGE based on this analysis:
        
        **SPECIFIC LAYOUT REQUIREMENTS:**
        {specific_layout}
        
        **DETECTED ELEMENTS:**
        - Elements found: {len(elements)} ({', '.join(set(element_types))})
        - Screen size: {dimensions.get('width', 'unknown')}x{dimensions.get('height', 'unknown')}px
        - Source: {filename}
        
        **PROJECT CONTEXT:**
        {project_description}
        
        **TECHNICAL REQUIREMENTS:**
        - Use Tailwind CSS for ALL styling
        - Make it fully responsive (mobile-first)
        - Use semantic HTML elements
        - Add proper ARIA labels for accessibility
        - Include hover states and smooth transitions
        - Use modern React functional component pattern
        - Add realistic placeholder content specific to the page type
        
        **IMPORTANT:** Create a layout that is DISTINCTLY DIFFERENT from other page types. 
        The {page_type} page should have a unique structure and purpose-specific elements.
        
        Generate complete, production-ready JSX code that clearly represents a {page_type} interface.
        """
    
    def _fix_component_name_in_code(self, code: str, correct_name: str) -> str:
        """Fix component name in the generated code to match the intended name."""
        import re
        
        # Find existing component name pattern
        component_pattern = r'const\s+(\w+)\s*=\s*\(\s*\)\s*=>\s*\{'
        export_pattern = r'export\s+default\s+(\w+);?'
        
        # Replace component declaration
        code = re.sub(component_pattern, f'const {correct_name} = () => {{', code)
        
        # Replace export statement
        code = re.sub(export_pattern, f'export default {correct_name};', code)
        
        return code
    
    def _generate_fallback_component(self, layout_info: Dict[str, Any], component_name: str = None) -> str:
        """Generate a guaranteed error-free fallback component with smart naming."""
        if not component_name:
            component_name = generate_smart_component_name(
                filename=layout_info.get('filename', 'unknown'),
                elements=layout_info.get('basic_elements', [])
            )
        
        # Use our FIXED template generator instead of the old generic one
        print(f"🔄 Using fixed template generator for fallback: {component_name}")
        return create_error_free_component(layout_info, component_name)
    
    def process_multiple_layouts(self, layout_data: List[Dict[str, Any]], project_description: str = "") -> List[Dict[str, Any]]:
        """Process multiple layout analyses and generate components."""
        results = []
        
        for layout in layout_data:
            filename = layout.get('filename', 'unknown')
            log_processing(filename)
            
            # Analyze with vision if we have image data
            if 'image_base64' in layout:
                analyzed_layout = self.analyze_layout_with_vision(layout, project_description)
            else:
                analyzed_layout = layout
            
            # Generate React component
            component_code = self.generate_react_component(analyzed_layout, project_description)
            
            results.append({
                'filename': layout['filename'],
                'component_name': layout['filename'].replace('.', '').replace('-', '').replace('_', '').title() + 'Component',
                'layout_info': analyzed_layout,
                'component_code': component_code
            })
        
        return results
