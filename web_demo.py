#!/usr/bin/env python3
"""
Web-based demo that works directly with uploaded files instead of directory processing.
"""

import os
import sys
from agent.web_vision import process_web_uploads
from agent.template_generator import create_error_free_component
from agent.codegen import CodeGenerator
from agent.hosting import AppHosting

def create_demo_from_web_uploads():
    """Create a demo project using web-based file processing."""
    print("🚀 Creating Demo with Web-based File Processing...")
    
    # Simulate uploaded files (in real usage, these come from Flask)
    demo_files = []
    
    # Check if we have sample images
    sample_images = ['input/dashboard.png', 'input/login.png']
    
    for img_path in sample_images:
        if os.path.exists(img_path):
            with open(img_path, 'rb') as f:
                file_data = {
                    'filename': os.path.basename(img_path),
                    'content': f.read(),
                    'content_type': 'image/png'
                }
                demo_files.append(file_data)
    
    if not demo_files:
        print("❌ No sample images found!")
        print("💡 Add some images to the 'input' directory to test")
        return False
    
    print(f"📸 Processing {len(demo_files)} uploaded files...")
    
    # Process uploaded files directly
    image_data = process_web_uploads(demo_files)
    
    if not image_data:
        print("❌ Failed to process uploaded images")
        return False
    
    print(f"✅ Processed {len(image_data)} images successfully")
    
    # Generate components using error-free templates
    components_data = []
    for img_data in image_data:
        component_name = img_data['filename'].replace('.', '').replace('-', '').replace('_', '').title() + 'Component'
        
        # Create layout info for template generation
        layout_info = {
            'filename': img_data['filename'],
            'basic_elements': img_data['elements'],
            'dimensions': img_data['dimensions']
        }
        
        # Generate error-free React component
        component_code = create_error_free_component(layout_info)
        
        components_data.append({
            'filename': img_data['filename'],
            'component_name': component_name,
            'layout_info': layout_info,
            'component_code': component_code
        })
    
    print(f"✅ Generated {len(components_data)} React components")
    
    # Generate complete React project
    print("⚛️  Creating React project structure...")
    project_dir = "web_demo_project"
    code_generator = CodeGenerator(project_dir)
    
    project_description = "Demo project generated from web uploads with modern React components and Tailwind CSS styling."
    code_generator.generate_project(components_data, project_description)
    
    print("🎉 Demo Project Generated Successfully!")
    print(f"📁 Location: {project_dir}")
    
    # Auto-host the application
    print("\n🌐 Starting automatic hosting...")
    hosting = AppHosting(project_dir)
    deployment_info = hosting.deploy_and_host(mode='development')
    
    if deployment_info['status'] == 'success':
        print("\n🎊 Complete Success!")
        print("=" * 60)
        print(f"📱 Your app is live at: {deployment_info['local_url']}")
        if deployment_info.get('public_url'):
            print(f"🌍 Public URL: {deployment_info['public_url']}")
            print("   👆 Share this URL with anyone!")
        print("=" * 60)
        
        print("\n💡 Demo is running. Press Ctrl+C to stop...")
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping demo...")
            hosting.stop_servers()
            print("✅ Demo stopped successfully!")
    else:
        print(f"⚠️  Hosting failed: {deployment_info.get('error', 'Unknown error')}")
        print("💡 You can still run manually:")
        print(f"   cd {project_dir}")
        print("   npm install")
        print("   npm run dev")
    
    return True

def test_web_vision_processor():
    """Test the web vision processor with sample files."""
    print("🧪 Testing Web Vision Processor...")
    
    # Test with sample files
    sample_files = []
    
    # Look for sample images
    for filename in ['input/dashboard.png', 'input/login.png']:
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                file_data = {
                    'filename': os.path.basename(filename),
                    'content': f.read(),
                    'content_type': 'image/png'
                }
                sample_files.append(file_data)
    
    if not sample_files:
        print("❌ No sample files found for testing")
        return False
    
    # Process files
    processed_data = process_web_uploads(sample_files)
    
    print(f"✅ Processed {len(processed_data)} files")
    
    for data in processed_data:
        print(f"   📸 {data['filename']}: {len(data['elements'])} elements detected")
        print(f"      Size: {data['dimensions']['width']}x{data['dimensions']['height']}")
        print(f"      Elements: {[e['type'] for e in data['elements'][:3]]}")
    
    return True

if __name__ == "__main__":
    print("🌐 Web-based AI UI Generator Demo")
    print("=" * 40)
    
    # Test the web vision processor first
    if test_web_vision_processor():
        print("\n" + "=" * 40)
        # Run the complete demo
        create_demo_from_web_uploads()
    else:
        print("❌ Web vision processor test failed")
        print("💡 Make sure you have sample images in the 'input' directory")
