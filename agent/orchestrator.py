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
        Generate React component code from layout information with enhanced LLM processing.
        """
        # Generate smart component name
        component_name = generate_smart_component_name(
            filename=layout_info.get('filename', 'unknown'),
            elements=layout_info.get('basic_elements', []),
            project_description=project_description
        )
        
        # Create enhanced prompt with image analysis
        prompt = self._create_enhanced_code_generation_prompt(layout_info, project_description, component_name)
        
        print(f"🤖 Generating React component: {component_name}")
        print(f"📝 Using enhanced LLM prompt with image analysis")
        
        try:
            response = self.client.chat.completions.create(
                model=self.text_model,
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are an expert React developer. You MUST generate a complete, working React functional component.

STRICT REQUIREMENTS:
1. Component name MUST be exactly: {component_name}
2. MUST start with: import React from 'react';
3. MUST have functional component: const {component_name} = () => {{
4. MUST end with: export default {component_name};
5. Use Tailwind CSS classes for ALL styling
6. Create a responsive, modern design
7. NO markdown code blocks (```jsx or ```)
8. NO explanatory text before or after the code
9. Return ONLY the complete React component code

EXAMPLE STRUCTURE:
import React from 'react';

const {component_name} = () => {{
  return (
    <div className="min-h-screen bg-gray-50">
      {{/* Your component JSX here */}}
    </div>
  );
}};

export default {component_name};

Generate the complete component now."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=3000,
                temperature=0.1  # Low temperature for consistency
            )
            
            raw_code = response.choices[0].message.content.strip()
            
            print(f"📝 Raw AI response length: {len(raw_code)} chars")
            print(f"📝 First 100 chars: {raw_code[:100]}...")
            
            # Enhanced code cleaning
            cleaned_code = self._enhanced_code_cleaning(raw_code, component_name)
            
            # Enhanced validation
            is_valid, final_code, errors = self._enhanced_code_validation(cleaned_code, component_name)
            
            if is_valid:
                log_success(f"✅ AI generated valid React component: {component_name}")
                print(f"✅ AI generation successful!")
                return final_code
            else:
                log_error(f"❌ AI-generated code validation failed: {errors}")
                print(f"❌ AI validation failed: {errors}")
                print("🔄 Using enhanced fallback component")
                return self._generate_fallback_component(layout_info, component_name)
            
        except Exception as e:
            log_error(f"❌ AI generation error: {e}")
            print(f"❌ AI generation error: {e}")
            print("🔄 Using enhanced fallback component")
            return self._generate_fallback_component(layout_info, component_name)
    
    def _create_enhanced_code_generation_prompt(self, layout_info: Dict[str, Any], project_description: str, component_name: str) -> str:
        """Create an enhanced prompt with image analysis and specific instructions."""
        filename = layout_info.get('filename', 'unknown')
        elements = layout_info.get('basic_elements', [])
        dimensions = layout_info.get('dimensions', {})
        
        # Use image analysis if available
        image_analysis = layout_info.get('image_analysis', {})
        page_type = layout_info.get('page_type', 'generic')
        page_description = layout_info.get('page_description', '')
        
        # Create specific instructions based on page type
        if page_type == 'login':
            specific_instructions = f"""
            Create a LOGIN PAGE component named {component_name} with:
            - Centered login form (max-width: 400px)
            - Email input field with proper validation styling
            - Password input field with proper validation styling
            - "Sign In" button (blue, full width)
            - "Forgot Password?" link
            - Clean, professional design with white card on gray background
            - Proper form structure with labels and placeholders
            """
        elif page_type == 'dashboard':
            specific_instructions = f"""
            Create a DASHBOARD component named {component_name} with:
            - Top navigation bar with title and user menu
            - Grid of 4 metric cards showing statistics (users, revenue, orders, conversion)
            - Each card with title, large number, and trend indicator
            - Recent activity section with timeline items
            - Charts/analytics placeholder section
            - Professional admin interface styling with proper spacing
            """
        elif page_type == 'profile':
            specific_instructions = f"""
            Create a USER PROFILE component named {component_name} with:
            - Profile header with avatar placeholder and user name
            - Personal information form section with input fields
            - Account settings section with toggle switches
            - Save/Update buttons
            - Clean, user-friendly design with proper form styling
            """
        elif page_type == 'homepage':
            specific_instructions = f"""
            Create a HOMEPAGE component named {component_name} with:
            - Navigation header with logo and menu items
            - Hero section with large heading and call-to-action button
            - Features section with 3-4 feature cards
            - Professional marketing-focused design
            """
        elif page_type == 'product':
            specific_instructions = f"""
            Create an E-COMMERCE component named {component_name} with:
            - Product grid layout (3-4 columns)
            - Product cards with image placeholder, title, and price
            - Filter sidebar with categories and price ranges
            - Search functionality
            - Shopping cart integration
            """
        else:
            # Generic but specific instructions
            specific_instructions = f"""
            Create a {page_type.upper()} component named {component_name} with:
            - Modern, responsive layout using Tailwind CSS
            - Header section with appropriate title
            - Main content area with relevant sections
            - Professional styling with proper spacing and colors
            - Interactive elements like buttons and forms where appropriate
            """
        
        return f"""
        Generate a complete React functional component based on this analysis:
        
        COMPONENT REQUIREMENTS:
        - Component name: {component_name}
        - Source file: {filename}
        - Page type: {page_type}
        - Description: {page_description}
        
        DETECTED ELEMENTS:
        - UI elements found: {len(elements)} ({', '.join(set([e.get('type', 'unknown') for e in elements]))})
        - Screen dimensions: {dimensions.get('width', 'unknown')}x{dimensions.get('height', 'unknown')}px
        
        SPECIFIC INSTRUCTIONS:
        {specific_instructions}
        
        PROJECT CONTEXT:
        {project_description}
        
        TECHNICAL REQUIREMENTS:
        - Use Tailwind CSS for ALL styling
        - Make it fully responsive (mobile-first approach)
        - Use semantic HTML elements (header, main, section, etc.)
        - Add proper ARIA labels for accessibility
        - Include hover states and smooth transitions
        - Use modern React functional component pattern
        - Add realistic placeholder content
        - Ensure proper JSX syntax and structure
        
        Generate the complete React component code now. Start with import React and end with export default.
        """
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
        
    def _enhanced_code_cleaning(self, raw_code: str, component_name: str) -> str:
        """Enhanced code cleaning with better error handling."""
        import re
        
        # Remove markdown code blocks
        code = re.sub(r'```(?:jsx?|javascript)?\n?', '', raw_code)
        code = re.sub(r'```\n?', '', code)
        
        # Remove any explanatory text before import
        lines = code.split('\n')
        cleaned_lines = []
        found_import = False
        
        for line in lines:
            if 'import React' in line:
                found_import = True
            
            if found_import:
                cleaned_lines.append(line)
        
        code = '\n'.join(cleaned_lines)
        
        # Ensure proper import statement
        if not code.strip().startswith('import React'):
            code = "import React from 'react';\n\n" + code
        
        # Fix component name if needed
        code = self._fix_component_name_in_code(code, component_name)
        
        # Ensure proper export
        if f'export default {component_name}' not in code:
            code = code.rstrip() + f'\n\nexport default {component_name};'
        
        return code.strip()
    
    def _enhanced_code_validation(self, code: str, component_name: str) -> tuple:
        """Enhanced code validation with detailed error checking."""
        errors = []
        
        # Check for import statement
        if 'import React' not in code:
            errors.append('Missing React import statement')
        
        # Check for functional component declaration
        if f'const {component_name} = () =>' not in code and f'function {component_name}(' not in code:
            errors.append('Missing functional component declaration')
        
        # Check for export statement
        if f'export default {component_name}' not in code:
            errors.append('Missing export default statement')
        
        # Check for return statement
        if 'return (' not in code and 'return<' not in code:
            errors.append('Missing return statement')
        
        # Check for basic JSX structure
        if '<div' not in code and '<main' not in code and '<section' not in code:
            errors.append('Missing JSX elements')
        
        # Check for proper JSX closing
        open_tags = code.count('<div')
        close_tags = code.count('</div>')
        if open_tags > 0 and close_tags == 0:
            errors.append('Unclosed JSX tags detected')
        
        # If no errors, code is valid
        if not errors:
            return True, code, []
        
        # Try to fix common issues
        fixed_code = self._attempt_code_fixes(code, component_name, errors)
        
        # Re-validate fixed code
        if self._quick_validation(fixed_code, component_name):
            return True, fixed_code, []
        
        return False, code, errors
    
    def _attempt_code_fixes(self, code: str, component_name: str, errors: list) -> str:
        """Attempt to fix common code issues."""
        fixed_code = code
        
        # Fix missing import
        if 'Missing React import statement' in errors:
            if not fixed_code.strip().startswith('import React'):
                fixed_code = "import React from 'react';\n\n" + fixed_code
        
        # Fix missing component declaration
        if 'Missing functional component declaration' in errors:
            if f'const {component_name} = () =>' not in fixed_code:
                # Try to find and fix component declaration
                import re
                pattern = r'const\s+\w+\s*=\s*\(\s*\)\s*=>'
                if re.search(pattern, fixed_code):
                    fixed_code = re.sub(pattern, f'const {component_name} = () =>', fixed_code)
                else:
                    # Add component declaration if missing
                    lines = fixed_code.split('\n')
                    for i, line in enumerate(lines):
                        if 'return (' in line or 'return<' in line:
                            lines.insert(i, f'const {component_name} = () => {{')
                            break
                    fixed_code = '\n'.join(lines)
        
        # Fix missing export
        if 'Missing export default statement' in errors:
            if f'export default {component_name}' not in fixed_code:
                fixed_code = fixed_code.rstrip() + f'\n\nexport default {component_name};'
        
        # Fix missing return statement
        if 'Missing return statement' in errors:
            if 'return (' not in fixed_code and 'return<' not in fixed_code:
                # Try to add return statement
                lines = fixed_code.split('\n')
                for i, line in enumerate(lines):
                    if '<div' in line and 'return' not in lines[max(0, i-1)]:
                        lines[i] = '  return (' + line.strip()
                        # Find closing and add );
                        for j in range(len(lines)-1, i, -1):
                            if '</div>' in lines[j] or '/>' in lines[j]:
                                lines[j] = lines[j] + '\n  );'
                                break
                        break
                fixed_code = '\n'.join(lines)
        
        return fixed_code
    
    def _quick_validation(self, code: str, component_name: str) -> bool:
        """Quick validation check."""
        required_elements = [
            'import React',
            f'const {component_name} = () =>',
            'return (',
            f'export default {component_name}'
        ]
        
        return all(element in code for element in required_elements)
    
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
