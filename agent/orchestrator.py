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
        Generate React component code from layout information with actual image reference.
        """
        # Generate smart component name
        component_name = generate_smart_component_name(
            filename=layout_info.get('filename', 'unknown'),
            elements=layout_info.get('basic_elements', []),
            project_description=project_description
        )
        
        print(f"🤖 Generating React component: {component_name}")
        print(f"📝 Using image-referenced generation with visual analysis")
        
        # Check if we have image data for visual reference
        image_base64 = layout_info.get('image_base64')
        if image_base64:
            print("📸 Using actual image reference for accurate generation")
            return self._generate_with_image_reference(layout_info, project_description, component_name, image_base64)
        else:
            print("⚠️  No image reference available, using text-based generation")
            return self._generate_without_image_reference(layout_info, project_description, component_name)
    
    def _generate_with_image_reference(self, layout_info: Dict[str, Any], project_description: str, component_name: str, image_base64: str) -> str:
        """Generate component with actual image reference for accurate design replication."""
        
        # Create image-referenced prompt
        prompt = self._create_image_referenced_prompt(layout_info, project_description, component_name)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",  # Use vision model
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are an expert React developer and UI/UX designer. You MUST generate a complete, professional, production-ready React functional component that follows all modern UI/UX best practices.

MANDATORY REQUIREMENTS - MUST INCLUDE ALL:
1. Component name MUST be exactly: {component_name}
2. MUST start with: import React from 'react';
3. MUST have: const {component_name} = () => {{
4. MUST end with: export default {component_name};
5. MUST use semantic HTML tags: <header>, <main>, <section>, <aside>, <nav>, <button>, <form>
6. MUST include responsive classes: sm:, md:, lg:, xl: for different screen sizes
7. MUST add hover states: hover:bg-blue-700, hover:shadow-lg, etc.
8. MUST add focus states: focus:ring-2, focus:ring-blue-500, focus:outline-none
9. MUST include transitions: transition-all, duration-200, ease-in-out
10. MUST add accessibility: aria-label, role, tabIndex, alt attributes
11. MUST use professional styling: shadows, borders, gradients, rounded corners
12. MUST include interactive states: onClick, onSubmit, onChange handlers
13. MUST be production-ready: no placeholder content, realistic data
14. NO markdown code blocks (```jsx or ```)
15. NO explanatory text before or after the code

PROFESSIONAL STYLING REQUIREMENTS - MUST IMPLEMENT:
- Use shadow-sm, shadow-md, shadow-lg for depth
- Use rounded-md, rounded-lg for modern corners
- Use border, border-gray-300 for subtle borders
- Use hover:shadow-lg, hover:scale-105 for interactions
- Use focus:ring-2, focus:ring-blue-500 for accessibility
- Use transition-all, duration-200 for smooth animations
- Use bg-gradient-to-r, from-blue-500, to-purple-600 for modern gradients
- Use text-gray-900, text-gray-600, text-blue-600 for proper typography
- Use space-y-4, space-x-4 for consistent spacing

RESPONSIVE DESIGN REQUIREMENTS - MUST IMPLEMENT:
- Use sm:text-sm, md:text-base, lg:text-lg for responsive typography
- Use sm:grid-cols-1, md:grid-cols-2, lg:grid-cols-3 for responsive grids
- Use sm:p-4, md:p-6, lg:p-8 for responsive padding
- Use hidden sm:block for responsive visibility
- Use sm:w-full, md:w-1/2, lg:w-1/3 for responsive widths

ACCESSIBILITY REQUIREMENTS - MUST IMPLEMENT:
- Add aria-label="Description" to all interactive elements
- Add role="button", role="navigation", role="main" where appropriate
- Add tabIndex="0" for keyboard navigation
- Add alt="Description" for all images and icons
- Use proper heading hierarchy: h1, h2, h3
- Add focus:outline-none focus:ring-2 for keyboard users

INTERACTIVE ELEMENTS - MUST IMPLEMENT:
- Add onClick={{() => console.log('Action')}} to buttons
- Add onSubmit={{(e) => e.preventDefault()}} to forms
- Add onChange={{(e) => console.log(e.target.value)}} to inputs
- Add disabled={{false}} state management
- Add loading states with conditional rendering

Generate a component that demonstrates professional, production-ready quality with ALL requirements implemented."""
                    },
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
                max_tokens=3000,
                temperature=0.05  # Very low temperature for accuracy
            )
            
            raw_code = response.choices[0].message.content.strip()
            
            print(f"📝 Image-referenced AI response length: {len(raw_code)} chars")
            print(f"📝 First 100 chars: {raw_code[:100]}...")
            
            # Enhanced code cleaning
            cleaned_code = self._enhanced_code_cleaning(raw_code, component_name)
            
            # Enhanced validation
            is_valid, final_code, errors = self._enhanced_code_validation(cleaned_code, component_name)
            
            if is_valid:
                log_success(f"✅ AI generated image-referenced component: {component_name}")
                print(f"✅ Image-referenced generation successful!")
                return final_code
            else:
                log_error(f"❌ Image-referenced generation validation failed: {errors}")
                print(f"❌ Image validation failed: {errors}")
                print("🔄 Trying text-based generation as fallback")
                return self._generate_without_image_reference(layout_info, project_description, component_name)
            
        except Exception as e:
            log_error(f"❌ Image-referenced generation error: {e}")
            print(f"❌ Image generation error: {e}")
            print("🔄 Trying text-based generation as fallback")
            return self._generate_without_image_reference(layout_info, project_description, component_name)
    
    def _generate_without_image_reference(self, layout_info: Dict[str, Any], project_description: str, component_name: str) -> str:
        """Generate component without image reference (fallback method)."""
        
        # Create enhanced prompt with image analysis
        prompt = self._create_enhanced_code_generation_prompt(layout_info, project_description, component_name)
        
        try:
            response = self.client.chat.completions.create(
                model=self.text_model,
                messages=[
                    {
                        "role": "system",
                        "role": "system",
                        "content": f"""You are an expert React developer and UI/UX designer. You MUST generate a complete, professional, production-ready React functional component.

MANDATORY REQUIREMENTS - MUST INCLUDE ALL:
1. Component name MUST be exactly: {component_name}
2. MUST start with: import React from 'react';
3. MUST have: const {component_name} = () => {{
4. MUST end with: export default {component_name};
5. MUST use semantic HTML tags: <header>, <main>, <section>, <aside>, <nav>, <button>, <form>
6. MUST include responsive classes: sm:, md:, lg:, xl: for different screen sizes
7. MUST add hover states: hover:bg-blue-700, hover:shadow-lg, etc.
8. MUST add focus states: focus:ring-2, focus:ring-blue-500, focus:outline-none
9. MUST include transitions: transition-all, duration-200, ease-in-out
10. MUST add accessibility: aria-label, role, tabIndex, alt attributes
11. MUST use professional styling: shadows, borders, gradients, rounded corners
12. MUST include interactive states: onClick, onSubmit, onChange handlers
13. MUST be production-ready: no placeholder content, realistic data
14. NO markdown code blocks (```jsx or ```)
15. NO explanatory text before or after the code

PROFESSIONAL STYLING REQUIREMENTS - MUST IMPLEMENT:
- Use shadow-sm, shadow-md, shadow-lg for depth
- Use rounded-md, rounded-lg for modern corners
- Use border, border-gray-300 for subtle borders
- Use hover:shadow-lg, hover:scale-105 for interactions
- Use focus:ring-2, focus:ring-blue-500 for accessibility
- Use transition-all, duration-200 for smooth animations
- Use bg-gradient-to-r, from-blue-500, to-purple-600 for modern gradients
- Use text-gray-900, text-gray-600, text-blue-600 for proper typography
- Use space-y-4, space-x-4 for consistent spacing

RESPONSIVE DESIGN REQUIREMENTS - MUST IMPLEMENT:
- Use sm:text-sm, md:text-base, lg:text-lg for responsive typography
- Use sm:grid-cols-1, md:grid-cols-2, lg:grid-cols-3 for responsive grids
- Use sm:p-4, md:p-6, lg:p-8 for responsive padding
- Use hidden sm:block for responsive visibility
- Use sm:w-full, md:w-1/2, lg:w-1/3 for responsive widths

ACCESSIBILITY REQUIREMENTS - MUST IMPLEMENT:
- Add aria-label="Description" to all interactive elements
- Add role="button", role="navigation", role="main" where appropriate
- Add tabIndex="0" for keyboard navigation
- Add alt="Description" for all images and icons
- Use proper heading hierarchy: h1, h2, h3
- Add focus:outline-none focus:ring-2 for keyboard users

INTERACTIVE ELEMENTS - MUST IMPLEMENT:
- Add onClick={{() => console.log('Action')}} to buttons
- Add onSubmit={{(e) => e.preventDefault()}} to forms
- Add onChange={{(e) => console.log(e.target.value)}} to inputs
- Add disabled={{false}} state management
- Add loading states with conditional rendering

Generate a professional component that demonstrates ALL requirements implemented."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=3000,
                temperature=0.1
            )
            
            raw_code = response.choices[0].message.content.strip()
            
            print(f"📝 Text-based AI response length: {len(raw_code)} chars")
            
            # Enhanced code cleaning
            cleaned_code = self._enhanced_code_cleaning(raw_code, component_name)
            
            # Enhanced validation
            is_valid, final_code, errors = self._enhanced_code_validation(cleaned_code, component_name)
            
            if is_valid:
                log_success(f"✅ AI generated text-based component: {component_name}")
                print(f"✅ Text-based generation successful!")
                return final_code
            else:
                log_error(f"❌ Text-based generation validation failed: {errors}")
                print(f"❌ Text validation failed: {errors}")
                print("🔄 Using enhanced fallback component")
                return self._generate_fallback_component(layout_info, component_name)
            
        except Exception as e:
            log_error(f"❌ Text-based generation error: {e}")
            print(f"❌ Text generation error: {e}")
            print("🔄 Using enhanced fallback component")
            return self._generate_fallback_component(layout_info, component_name)
    
    def _create_image_referenced_prompt(self, layout_info: Dict[str, Any], project_description: str, component_name: str) -> str:
        """Create a prompt that emphasizes following the actual image design with comprehensive UI/UX constraints."""
        filename = layout_info.get('filename', 'unknown')
        elements = layout_info.get('basic_elements', [])
        dimensions = layout_info.get('dimensions', {})
        
        # Use image analysis if available, but emphasize visual accuracy
        page_type = layout_info.get('page_type', 'generic')
        page_description = layout_info.get('page_description', '')
        
        return f"""
        CRITICAL: Analyze the provided UI design image and create a React component that EXACTLY matches what you see with professional UI/UX standards.

        🎯 PRIMARY PROJECT REQUIREMENTS (HIGHEST PRIORITY):
        {project_description}
        
        ⚠️  IMPORTANT: The above project description contains specific requirements, features, and instructions that MUST be incorporated into the component. Do not ignore these requirements - they are the primary goals for this component.

        UX DESIGN INTERPRETATION REQUIREMENTS:
        - Take as much inspiration as possible from the provided image - replicate every visual detail
        - Use the project description to understand the specific functionality and features needed
        - Make sure the design is intuitive and user-friendly with clear visual hierarchy
        - Don't miss any important UI elements shown in the image - include every button, input, icon, text
        - Recreate each screen or state shown in the image with pixel-perfect accuracy
        - Group related images into a single layout if applicable
        - Build separate components for unrelated sections if they serve different purposes
        - Avoid basic/unstyled HTML elements – ensure polished, professional styling
        - Use semantic HTML tags (`<section>`, `<button>`, `<nav>`, `<header>`, `<main>`, `<aside>`, `<footer>`, etc.)
        - Ensure all interactive elements are accessible and keyboard-navigable
        - Use consistent color schemes and typography throughout
        - Ensure the final output is production-ready with no placeholder content
        - Make sure the design is responsive and works well on different screen sizes
        - Create attractive and modern design, suitable for a professional application

        VISUAL ANALYSIS REQUIREMENTS:
        - Look at the ACTUAL colors in the image and use matching Tailwind CSS classes
        - Observe the EXACT layout structure, spacing, and alignment
        - Notice the specific positioning of elements (top, center, left, right, etc.)
        - If the design is rough/sketchy, interpret it as a professional, polished interface
        - Don't assume standard UI patterns - follow the ACTUAL visual design
        - Match text content if visible in the image, or create realistic professional content
        - Replicate button styles, shapes, and colors from the image with enhanced polish
        - Follow the actual color scheme (backgrounds, text, accents) with professional refinement
        - Identify and recreate any icons, graphics, or visual elements shown
        
        COMPONENT GROUPING AND SEPARATION LOGIC:
        - Group related images into one layout or screen where applicable
        - If the image shows multiple related sections (header + main content + sidebar), combine them into one cohesive component
        - Separate distinct UI parts into different components if they don't seem to be part of the same page
        - If the image contains clearly separate UI elements (like a modal + background page), focus on the primary element
        - For complex layouts, create logical sections within the single component rather than splitting unnecessarily
        - Maintain visual hierarchy and relationships between elements as shown in the image
        
        PROFESSIONAL STYLING REQUIREMENTS:
        - Use modern Tailwind CSS classes for professional appearance
        - Implement proper hover states, focus states, and transitions
        - Add subtle shadows, borders, and rounded corners for polish
        - Use appropriate spacing (padding, margins) for visual breathing room
        - Implement proper typography hierarchy with varied font sizes and weights
        - Add loading states, disabled states for interactive elements where appropriate
        - Use consistent color palette throughout the component
        - Implement proper form validation styling if forms are present
        
        ACCESSIBILITY AND INTERACTION REQUIREMENTS:
        - Add proper ARIA labels, roles, and descriptions
        - Ensure keyboard navigation works for all interactive elements
        - Use semantic HTML elements for screen reader compatibility
        - Implement proper focus management and visual focus indicators
        - Add alt text for images and icons
        - Ensure color contrast meets WCAG guidelines
        - Use proper heading hierarchy (h1, h2, h3, etc.)
        
        RESPONSIVE DESIGN REQUIREMENTS:
        - Use responsive Tailwind classes (sm:, md:, lg:, xl:)
        - Ensure layout adapts gracefully to different screen sizes
        - Stack elements vertically on mobile when appropriate
        - Adjust font sizes and spacing for different breakpoints
        - Hide/show elements appropriately for different screen sizes
        - Ensure touch targets are appropriately sized for mobile
        
        PRODUCTION-READY REQUIREMENTS:
        - No placeholder content - use realistic, professional text and data
        - Include proper error handling for forms and interactive elements
        - Add loading states and feedback for user actions
        - Implement proper data formatting (dates, numbers, currency)
        - Use realistic sample data that matches the application context
        - Include proper navigation and routing considerations
        - Add appropriate micro-interactions and animations
        
        COMPONENT DETAILS:
        - Component name: {component_name}
        - Source file: {filename}
        - Detected page type: {page_type}
        - Description: {page_description}
        - Screen dimensions: {dimensions.get('width', 'unknown')}x{dimensions.get('height', 'unknown')}px
        
        DETECTED ELEMENTS (use as reference, but prioritize visual analysis):
        - Elements found: {len(elements)} ({', '.join(set([e.get('type', 'unknown') for e in elements]))})
        
        🎯 REMEMBER: The project description at the top contains the most important requirements. Make sure to incorporate all specified features, functionality, and design requirements from the project description into your component.
        
        TECHNICAL IMPLEMENTATION:
        - Use Tailwind CSS classes that match the visual colors and styling with professional enhancements
        - Implement responsive design with mobile-first approach
        - Use semantic HTML elements for proper document structure
        - Add comprehensive accessibility attributes
        - Ensure the layout matches the image proportions with responsive adaptations
        - Use appropriate Tailwind color classes with consistent palette
        - Implement proper spacing with Tailwind spacing classes
        - Add hover effects, transitions, and micro-interactions
        - Use modern CSS Grid and Flexbox layouts where appropriate
        
        IMPORTANT CONSTRAINTS:
        - DO NOT use basic HTML elements without styling
        - DO NOT create placeholder or dummy content
        - DO NOT miss any UI elements visible in the image
        - DO NOT assume generic patterns - follow the actual design
        - DO NOT ignore the project description requirements
        - DO create polished, professional interfaces
        - DO ensure production-ready quality
        - DO make it fully responsive and accessible
        - DO use semantic HTML throughout
        - DO implement proper interactive states
        - DO create intuitive and user-friendly interfaces
        - DO incorporate all features mentioned in the project description
        
        Generate a React component that represents a professional, production-ready implementation of the design shown in the image, with all UI/UX best practices applied and all project requirements fulfilled.
        """
    
    def _create_enhanced_code_generation_prompt(self, layout_info: Dict[str, Any], project_description: str, component_name: str) -> str:
        """Create an enhanced prompt with comprehensive UI/UX constraints and professional standards."""
        filename = layout_info.get('filename', 'unknown')
        elements = layout_info.get('basic_elements', [])
        dimensions = layout_info.get('dimensions', {})
        
        # Use image analysis if available
        image_analysis = layout_info.get('image_analysis', {})
        page_type = layout_info.get('page_type', 'generic')
        page_description = layout_info.get('page_description', '')
        
        # Create specific instructions based on page type with comprehensive UI/UX constraints
        if page_type == 'login':
            specific_instructions = f"""
            Create a professional LOGIN PAGE component named {component_name} with:
            - Centered login form (max-width: 400px) with polished card design and subtle shadow
            - Email input field with proper validation styling, focus states, and error handling
            - Password input field with show/hide toggle and validation feedback
            - Primary "Sign In" button with hover effects and loading state
            - "Forgot Password?" link with proper hover styling
            - Social login options if applicable (Google, GitHub, etc.) with branded styling
            - Clean, professional design with consistent spacing and typography
            - Proper form validation with real-time feedback
            - Accessibility features: ARIA labels, keyboard navigation, focus management
            - Responsive design that works on mobile and desktop
            - Production-ready with no placeholder content
            """
        elif page_type == 'dashboard':
            specific_instructions = f"""
            Create a professional DASHBOARD component named {component_name} with:
            - Top navigation bar with logo, search, notifications, and user menu with dropdown
            - Sidebar navigation with icons, active states, and hover effects (collapsible on mobile)
            - Grid of metric cards with real data, trend indicators, and interactive hover states
            - Each card with proper typography hierarchy, icons, and color-coded values
            - Charts and data visualization sections with loading states and tooltips
            - Recent activity feed with timestamps, user avatars, and action descriptions
            - Quick action buttons with proper styling and feedback
            - Professional color scheme with consistent branding
            - Responsive layout that adapts to different screen sizes
            - Accessibility: proper headings, ARIA labels, keyboard navigation
            - Production-ready with realistic data and proper formatting
            """
        elif page_type == 'profile':
            specific_instructions = f"""
            Create a professional USER PROFILE component named {component_name} with:
            - Profile header with avatar upload, cover photo, and user information
            - Tabbed interface for different sections (Profile, Settings, Security, Preferences)
            - Personal information form with proper validation and error handling
            - Account settings with toggle switches, dropdowns, and proper feedback
            - Security section with password change, 2FA setup, and session management
            - Save/Update buttons with loading states and success feedback
            - Professional styling with consistent spacing and typography
            - Form validation with real-time feedback and error messages
            - Accessibility: proper form labels, keyboard navigation, screen reader support
            - Responsive design that works across all devices
            - Production-ready with realistic user data and proper formatting
            """
        elif page_type == 'homepage':
            specific_instructions = f"""
            Create a professional HOMEPAGE component named {component_name} with:
            - Navigation header with logo, menu items, and call-to-action button
            - Hero section with compelling headline, description, and primary CTA
            - Features section with icons, descriptions, and benefits
            - Testimonials or social proof section with user photos and quotes
            - Pricing or product showcase with comparison tables
            - Footer with links, contact information, and social media
            - Professional marketing design with consistent branding
            - Smooth scrolling and micro-interactions
            - Accessibility: proper headings, alt text, keyboard navigation
            - Fully responsive design optimized for all devices
            - Production-ready with compelling copy and realistic content
            """
        elif page_type == 'product':
            specific_instructions = f"""
            Create a professional E-COMMERCE component named {component_name} with:
            - Product grid with high-quality images, titles, prices, and ratings
            - Advanced filtering sidebar with categories, price ranges, and brand filters
            - Search functionality with autocomplete and search suggestions
            - Product cards with hover effects, quick view, and add to cart buttons
            - Shopping cart with item count, total, and checkout process
            - Pagination or infinite scroll with loading states
            - Professional e-commerce styling with consistent product presentation
            - Wishlist functionality and product comparison features
            - Accessibility: proper product information, keyboard navigation
            - Mobile-optimized design with touch-friendly interactions
            - Production-ready with realistic product data and pricing
            """
        else:
            # Generic but comprehensive instructions with UI/UX constraints
            specific_instructions = f"""
            Create a professional {page_type.upper()} component named {component_name} with:
            - Modern, responsive layout using professional design principles
            - Header section with proper navigation and branding
            - Main content area with logical sections and clear hierarchy
            - Interactive elements with proper hover, focus, and active states
            - Professional styling with consistent spacing, typography, and colors
            - Semantic HTML structure with proper accessibility attributes
            - Responsive design that adapts to all screen sizes
            - Production-ready with realistic content and proper data formatting
            - Polished UI with subtle animations and micro-interactions
            - Error handling and loading states for dynamic content
            """
        
        return f"""
        Generate a professional, production-ready React functional component based on this analysis:
        
        UX DESIGN INTERPRETATION REQUIREMENTS:
        - Take as much inspiration as possible from the detected elements and page type
        - Make sure the design is intuitive and user-friendly with clear visual hierarchy
        - Don't miss any important UI elements that should be present for this page type
        - Recreate professional versions of common UI patterns for this screen type
        - Group related functionality into logical sections
        - Build cohesive layouts that serve the user's primary goals
        - Avoid basic/unstyled HTML elements – ensure polished, professional styling
        - Use semantic HTML tags (`<section>`, `<button>`, `<nav>`, `<header>`, `<main>`, `<aside>`, `<footer>`, etc.)
        - Ensure all interactive elements are accessible and keyboard-navigable
        - Use consistent color schemes and typography throughout
        - Ensure the final output is production-ready with no placeholder content
        - Make sure the design is responsive and works well on different screen sizes
        - Create attractive and modern design, suitable for a professional application
        
        COMPONENT REQUIREMENTS:
        - Component name: {component_name}
        - Source file: {filename}
        - Page type: {page_type}
        - Description: {page_description}
        
        DETECTED ELEMENTS:
        - UI elements found: {len(elements)} ({', '.join(set([e.get('type', 'unknown') for e in elements]))})
        - Screen dimensions: {dimensions.get('width', 'unknown')}x{dimensions.get('height', 'unknown')}px
        
        COMPONENT GROUPING AND SEPARATION GUIDELINES:
        - Group related images into one layout or screen where applicable
        - Separate distinct UI parts into different components if they don't seem to be part of the same page
        - For multi-section layouts (navigation + content + footer), create one component with proper semantic sections
        - Use logical grouping for related functionality (all form inputs together, all navigation together, etc.)
        - Maintain visual hierarchy and relationships between elements
        - Create cohesive layouts that reflect natural user flow and interaction patterns
        
        SPECIFIC IMPLEMENTATION INSTRUCTIONS:
        {specific_instructions}
        
        PROJECT CONTEXT:
        {project_description}
        
        PROFESSIONAL STYLING REQUIREMENTS:
        - Use modern Tailwind CSS classes for professional appearance
        - Implement proper hover states, focus states, and transitions
        - Add subtle shadows, borders, and rounded corners for polish
        - Use appropriate spacing (padding, margins) for visual breathing room
        - Implement proper typography hierarchy with varied font sizes and weights
        - Add loading states, disabled states for interactive elements where appropriate
        - Use consistent color palette throughout the component
        - Implement proper form validation styling if forms are present
        - Add micro-interactions and smooth transitions
        
        ACCESSIBILITY AND INTERACTION REQUIREMENTS:
        - Add proper ARIA labels, roles, and descriptions
        - Ensure keyboard navigation works for all interactive elements
        - Use semantic HTML elements for screen reader compatibility
        - Implement proper focus management and visual focus indicators
        - Add alt text for images and icons
        - Ensure color contrast meets professional standards
        - Use proper heading hierarchy (h1, h2, h3, etc.)
        - Implement proper form validation and error messaging
        
        RESPONSIVE DESIGN REQUIREMENTS:
        - Use responsive Tailwind classes (sm:, md:, lg:, xl:, 2xl:)
        - Ensure layout adapts gracefully to different screen sizes
        - Stack elements vertically on mobile when appropriate
        - Adjust font sizes and spacing for different breakpoints
        - Hide/show elements appropriately for different screen sizes
        - Ensure touch targets are appropriately sized for mobile
        - Optimize for both portrait and landscape orientations
        
        PRODUCTION-READY REQUIREMENTS:
        - No placeholder content - use realistic, professional text and data
        - Include proper error handling for forms and interactive elements
        - Add loading states and feedback for user actions
        - Implement proper data formatting (dates, numbers, currency)
        - Use realistic sample data that matches the application context
        - Include proper navigation and routing considerations
        - Add appropriate status indicators and feedback messages
        - Implement proper state management for interactive elements
        
        TECHNICAL IMPLEMENTATION:
        - Use Tailwind CSS for ALL styling with professional design patterns
        - Make it fully responsive with mobile-first approach
        - Use semantic HTML elements (header, main, section, aside, footer, nav, button) for proper structure
        - Add comprehensive accessibility attributes (ARIA labels, roles, descriptions)
        - Include hover states, focus states, and smooth transitions
        - Use modern React functional component patterns with proper state management
        - Implement realistic, professional content and data
        - Ensure proper JSX syntax and component structure
        - Group related elements in logical containers with proper spacing
        - Separate distinct functional areas with appropriate visual hierarchy
        
        LAYOUT STRUCTURE GUIDELINES:
        - For full-page layouts: Use semantic sections that group related content professionally
        - For card-based designs: Group related cards in appropriate containers with consistent styling
        - For form layouts: Group form elements logically with proper validation and feedback
        - For dashboard layouts: Organize metrics, charts, and controls in professional sections
        - For navigation layouts: Group navigation elements with proper hierarchy and interaction states
        
        IMPORTANT CONSTRAINTS:
        - DO NOT use basic HTML elements without professional styling
        - DO NOT create placeholder or dummy content
        - DO NOT miss important UI elements for this page type
        - DO NOT use generic patterns without considering the specific use case
        - DO create polished, professional interfaces with attention to detail
        - DO ensure production-ready quality with proper error handling
        - DO make it fully responsive and accessible
        - DO use semantic HTML throughout with proper structure
        - DO implement proper interactive states and feedback
        - DO create intuitive and user-friendly interfaces that serve real user needs
        
        Generate the complete React component code now. Start with import React and end with export default.
        Create a component that represents professional, production-ready quality with comprehensive UI/UX best practices applied.
        """
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
        Generate a professional, production-ready React functional component based on this analysis:
        
        🎯 PRIMARY PROJECT REQUIREMENTS (HIGHEST PRIORITY):
        {project_description}
        
        ⚠️  CRITICAL: The above project description contains specific requirements, features, and instructions that MUST be incorporated into the component. This is the most important part of your task - ensure all specified features and functionality are included.
        
        COMPONENT REQUIREMENTS:
        - Component name: {component_name}
        - Source file: {filename}
        - Page type: {page_type}
        - Description: {page_description}
        
        DETECTED ELEMENTS:
        - UI elements found: {len(elements)} ({', '.join(set([e.get('type', 'unknown') for e in elements]))})
        - Screen dimensions: {dimensions.get('width', 'unknown')}x{dimensions.get('height', 'unknown')}px
        
        SPECIFIC IMPLEMENTATION INSTRUCTIONS:
        {specific_instructions}
        
        🎯 REMEMBER: Incorporate ALL features, functionality, and requirements mentioned in the project description above. This is the primary goal of the component.
        
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
