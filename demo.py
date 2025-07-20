#!/usr/bin/env python3
"""
Demo script to show the AI UI Generator functionality without requiring OpenAI API.
This creates a sample React project using error-free fallback components.
"""

import os
from agent.vision import VisionProcessor
from agent.codegen import CodeGenerator
from agent.template_generator import create_error_free_component

def create_demo_project():
    """Create a demo project using the vision processor and error-free components."""
    print("🚀 Creating Demo AI-Generated UI Project...")
    
    # Initialize components
    vision_processor = VisionProcessor()
    code_generator = CodeGenerator("demo_project")
    
    # Process images
    print("🖼️  Processing images...")
    image_data = vision_processor.process_multiple_images("input")
    
    if not image_data:
        print("❌ No images found!")
        return False
    
    print(f"✅ Processed {len(image_data)} images")
    
    # Create mock components data (simulating AI generation)
    components_data = []
    for img_data in image_data:
        component_name = img_data['filename'].replace('.', '').replace('-', '').replace('_', '').title() + 'Component'
        
        # Generate error-free React component
        component_code = create_error_free_component(img_data)
        
        components_data.append({
            'filename': img_data['filename'],
            'component_name': component_name,
            'layout_info': img_data,
            'component_code': component_code
        })
    
    print(f"✅ Generated {len(components_data)} React components")
    
    # Load project description
    desc_file = "input/project_description.txt"
    project_description = ""
    if os.path.exists(desc_file):
        with open(desc_file, 'r') as f:
            project_description = f.read().strip()
    
    # Generate complete React project
    print("⚛️  Creating React project structure...")
    code_generator.generate_project(components_data, project_description)
    
    print("🎉 Demo Project Generated Successfully!")
    print(f"📁 Location: demo_project")
    print("\n🚀 To run the demo project:")
    print("   cd demo_project")
    print("   npm install")
    print("   npm run dev")
    
    return True

if __name__ == "__main__":
    create_demo_project()
