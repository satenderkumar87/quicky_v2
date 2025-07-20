"""
Builder coordinator that orchestrates the entire UI generation workflow.
"""

import os
import time
from typing import List, Dict, Any
from .vision import VisionProcessor
from .orchestrator import AIOrchestrator
from .codegen import CodeGenerator
from .hosting import AppHosting

class UIBuilder:
    def __init__(self, input_dir: str = "input", output_dir: str = "generated_project"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.vision_processor = VisionProcessor()
        self.ai_orchestrator = AIOrchestrator()
        self.code_generator = CodeGenerator(output_dir)
    
    def build_ui_from_images(self, auto_host: bool = True, host_mode: str = 'development') -> Dict[str, Any]:
        """
        Main workflow: Process images -> Generate layouts -> Create React app -> Host
        """
        result = {
            'success': False,
            'components_generated': 0,
            'local_url': None,
            'public_url': None,
            'error': None
        }
        
        try:
            print("🚀 Starting AI-Powered UI Generation...")
            
            # Step 1: Load project description
            project_description = self._load_project_description()
            print(f"📝 Project Description: {project_description[:100]}..." if len(project_description) > 100 else project_description)
            
            # Step 2: Process images with computer vision
            print("🖼️  Processing images...")
            image_data = self.vision_processor.process_multiple_images(self.input_dir)
            
            if not image_data:
                result['error'] = "No images found in input directory!"
                print("❌ No images found in input directory!")
                return result
            
            print(f"✅ Processed {len(image_data)} images")
            
            # Step 3: Generate layouts and components with AI
            print("🧠 Generating React components with AI...")
            components_data = self.ai_orchestrator.process_multiple_layouts(
                image_data, project_description
            )
            
            if not components_data:
                result['error'] = "Failed to generate components!"
                print("❌ Failed to generate components!")
                return result
            
            result['components_generated'] = len(components_data)
            print(f"✅ Generated {len(components_data)} React components")
            
            # Step 4: Generate complete React project
            print("⚛️  Creating React project structure...")
            self.code_generator.generate_project(components_data, project_description)
            
            print("🎉 UI Generation Complete!")
            print(f"📁 Generated project location: {self.output_dir}")
            
            # Step 5: Auto-host if requested
            if auto_host:
                print("\n🌐 Starting automatic hosting...")
                hosting = AppHosting(self.output_dir)
                deployment_info = hosting.deploy_and_host(mode=host_mode)
                
                if deployment_info['status'] == 'success':
                    result['local_url'] = deployment_info['local_url']
                    result['public_url'] = deployment_info.get('public_url')
                    result['hosting_info'] = deployment_info
                    
                    print("\n🎊 Complete Success!")
                    print("=" * 50)
                    print(f"📱 Your app is live at: {result['local_url']}")
                    if result['public_url']:
                        print(f"🌍 Public URL: {result['public_url']}")
                        print("   Share this URL with anyone!")
                    print("=" * 50)
                    
                    # Keep the server running
                    self._keep_server_running(hosting)
                    
                else:
                    print(f"⚠️  Hosting failed: {deployment_info.get('error', 'Unknown error')}")
                    print("💡 You can still run manually:")
                    print(f"   cd {self.output_dir}")
                    print("   npm install")
                    print("   npm run dev")
            else:
                print("\n🚀 To run the generated project:")
                print(f"   cd {self.output_dir}")
                print("   npm install")
                print("   npm run dev")
            
            result['success'] = True
            return result
            
        except Exception as e:
            result['error'] = str(e)
            print(f"❌ Error during UI generation: {e}")
            return result
    
    def _load_project_description(self) -> str:
        """Load project description from input directory."""
        description_file = os.path.join(self.input_dir, "project_description.txt")
        
        if os.path.exists(description_file):
            with open(description_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        else:
            # Create a default description file
            default_description = """A modern web application with clean, professional design.
The UI should be responsive, accessible, and follow modern design principles.
Use a minimal color palette with good contrast and typography."""
            
            os.makedirs(self.input_dir, exist_ok=True)
            with open(description_file, 'w', encoding='utf-8') as f:
                f.write(default_description)
            
            return default_description
    
    def get_project_status(self) -> Dict[str, Any]:
        """Get current project status and statistics."""
        status = {
            'input_dir_exists': os.path.exists(self.input_dir),
            'output_dir_exists': os.path.exists(self.output_dir),
            'images_found': 0,
            'project_description_exists': False
        }
        
        if status['input_dir_exists']:
            # Count images
            for filename in os.listdir(self.input_dir):
                if any(filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg']):
                    status['images_found'] += 1
            
            # Check for project description
            desc_file = os.path.join(self.input_dir, "project_description.txt")
            status['project_description_exists'] = os.path.exists(desc_file)
        
        return status
    
    def setup_example_project(self):
        """Set up an example project for testing."""
        print("🔧 Setting up example project...")
        
        # Create input directory
        os.makedirs(self.input_dir, exist_ok=True)
        
        # Create example project description
        example_description = """E-commerce Product Dashboard

A modern e-commerce dashboard for managing products, orders, and customer data.
The design should be clean and professional with:
- A sidebar navigation
- Product grid/list views
- Data tables for orders
- Customer profile cards
- Modern buttons and form elements
- Responsive design for mobile and desktop

Color scheme: Use blues and grays with white backgrounds.
Typography: Clean, readable fonts with proper hierarchy."""
        
        desc_file = os.path.join(self.input_dir, "project_description.txt")
        with open(desc_file, 'w', encoding='utf-8') as f:
            f.write(example_description)
        
        print(f"✅ Example project description created at: {desc_file}")
        print("📸 Add your UI screenshots to the input/ directory and run the generator!")
        
        return True
    
    def _keep_server_running(self, hosting: AppHosting):
        """Keep the server running and handle graceful shutdown."""
        print("\n💡 Server is running. Press Ctrl+C to stop...")
        
        try:
            # Keep the main thread alive
            while True:
                time.sleep(1)
                
                # Check if processes are still running
                status = hosting.get_status()
                if not status['dev_running'] and not status['preview_running']:
                    print("⚠️  Server stopped unexpectedly")
                    break
                    
        except KeyboardInterrupt:
            print("\n🛑 Shutting down servers...")
            hosting.stop_servers()
            print("✅ Servers stopped successfully")
        except Exception as e:
            print(f"❌ Error: {e}")
            hosting.stop_servers()
