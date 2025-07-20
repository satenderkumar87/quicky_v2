#!/usr/bin/env python3
"""
Web UI for AI-Powered UI Generator
Flask-based interface for uploading files and generating React UIs
Updated to process images directly from web uploads without directory dependencies
"""

import os
import sys
import shutil
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import threading
import time
from datetime import datetime

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.web_vision import process_web_uploads
from agent.orchestrator import AIOrchestrator
from agent.codegen import CodeGenerator
from agent.hosting import AppHosting
from agent.simple_hosting import quick_deploy
from agent.quick_build import lightning_deploy
from agent.component_namer import generate_smart_component_name, reset_component_names
from agent.image_analyzer import analyze_image_for_page_type

app = Flask(__name__)
app.secret_key = 'ai-ui-generator-secret-key-2024'

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Global variables for tracking generation status
generation_status = {
    'status': 'idle',  # idle, processing, completed, error
    'progress': 0,
    'message': '',
    'result': None,
    'error': None
}

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_directories():
    """Ensure required directories exist."""
    directories = [UPLOAD_FOLDER, 'generated_projects']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

@app.route('/')
def index():
    """Main upload page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle file upload and project description."""
    global generation_status
    
    try:
        # Reset status
        generation_status = {
            'status': 'processing',
            'progress': 10,
            'message': 'Processing uploaded files...',
            'result': None,
            'error': None
        }
        
        # Get project description
        project_description = request.form.get('description', '').strip()
        if not project_description:
            project_description = "A modern web application with clean, professional design."
        
        # Get uploaded files
        uploaded_files = request.files.getlist('files')
        if not uploaded_files or all(file.filename == '' for file in uploaded_files):
            generation_status['status'] = 'error'
            generation_status['error'] = 'No files uploaded'
            return jsonify({'error': 'No files uploaded'}), 400
        
        # Process uploaded files directly (no directory saving)
        file_data_list = []
        for file in uploaded_files:
            if file and file.filename != '' and allowed_file(file.filename):
                file_data = {
                    'filename': secure_filename(file.filename),
                    'content': file.stream.read(),
                    'content_type': file.content_type
                }
                file.stream.seek(0)  # Reset stream
                file_data_list.append(file_data)
        
        if not file_data_list:
            generation_status['status'] = 'error'
            generation_status['error'] = 'No valid image files uploaded'
            return jsonify({'error': 'No valid image files uploaded'}), 400
        
        generation_status['progress'] = 30
        generation_status['message'] = f'Processed {len(file_data_list)} files. Starting AI generation...'
        
        # Start UI generation in background thread
        thread = threading.Thread(target=generate_ui_from_uploads, args=(file_data_list, project_description))
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'message': f'Uploaded {len(file_data_list)} files',
            'files': [f['filename'] for f in file_data_list]
        })
        
    except Exception as e:
        generation_status['status'] = 'error'
        generation_status['error'] = str(e)
        return jsonify({'error': str(e)}), 500

def generate_ui_from_uploads(uploaded_files: list, project_description: str):
    """Background task to generate UI from uploaded files."""
    global generation_status
    
    try:
        generation_status['progress'] = 40
        generation_status['message'] = 'Analyzing UI screenshots with AI...'
        
        # Process uploaded images directly
        image_data = process_web_uploads(uploaded_files)
        
        if not image_data:
            generation_status['status'] = 'error'
            generation_status['error'] = 'Failed to process uploaded images'
            return
        
        generation_status['progress'] = 60
        generation_status['message'] = 'Analyzing images and generating React components...'
        
        # Reset component names for new project
        reset_component_names()
        
        # Initialize AI orchestrator
        ai_orchestrator = AIOrchestrator()
        
        # Generate components from processed images
        components_data = []
        for img_data in image_data:
            try:
                print(f"🔍 Processing {img_data['filename']}...")
                
                # ENHANCED: Analyze the actual image content to determine page type
                print("🤖 Analyzing image content with LLM vision...")
                image_analysis = analyze_image_for_page_type(
                    image_data=img_data['raw_data'],  # Original image bytes
                    filename=img_data['filename']
                )
                
                # Generate smart component name using image analysis
                component_name = generate_smart_component_name(
                    filename=img_data['filename'],
                    elements=img_data['elements'],
                    project_description=f"{project_description}. Page type: {image_analysis.get('page_type', 'generic')}"
                )
                
                # Enhanced layout info with image analysis AND image reference
                layout_info = {
                    'filename': img_data['filename'],
                    'layout_description': f"UI layout with {len(img_data['elements'])} detected elements",
                    'basic_elements': img_data['elements'],
                    'dimensions': img_data['dimensions'],
                    # Image analysis results
                    'image_analysis': image_analysis,
                    'page_type': image_analysis.get('page_type', 'generic'),
                    'page_description': image_analysis.get('page_description', ''),
                    'suggested_elements': image_analysis.get('main_elements', []),
                    # CRITICAL: Include actual image data for visual reference
                    'image_base64': img_data.get('image_base64'),  # For AI visual analysis
                    'raw_data': img_data.get('raw_data')  # For backup processing
                }
                
                print(f"📊 Image analysis: {image_analysis.get('page_type', 'unknown')} page")
                print(f"🏷️  Component name: {component_name}")
                
                # Generate React component with enhanced context
                component_code = ai_orchestrator.generate_react_component(layout_info, project_description)
                
                components_data.append({
                    'filename': img_data['filename'],
                    'component_name': component_name,
                    'layout_info': layout_info,
                    'component_code': component_code,
                    'page_type': image_analysis.get('page_type', 'generic')
                })
                
            except Exception as e:
                print(f"Error generating component for {img_data['filename']}: {e}")
                continue
        
        if not components_data:
            generation_status['status'] = 'error'
            generation_status['error'] = 'Failed to generate React components'
            return
        
        generation_status['progress'] = 80
        generation_status['message'] = 'Creating React project structure...'
        
        # Generate complete React project
        timestamp = int(time.time())
        output_dir = f'generated_projects/project_{timestamp}'
        code_generator = CodeGenerator(output_dir)
        code_generator.generate_project(components_data, project_description)
        
        generation_status['progress'] = 90
        generation_status['message'] = 'Lightning-fast deployment starting...'
        
        # Try lightning deployment first (under 1 minute)
        try:
            print("⚡ Attempting lightning deployment...")
            lightning_result = lightning_deploy(output_dir)
            
            if lightning_result['status'] == 'success':
                generation_status['status'] = 'completed'
                generation_status['progress'] = 100
                generation_status['message'] = f'UI generated in {lightning_result.get("elapsed", 0):.1f}s!'
                generation_status['result'] = {
                    'components_generated': len(components_data),
                    'local_url': lightning_result.get('local_url'),
                    'project_dir': output_dir,
                    'build_time': f"{lightning_result.get('elapsed', 0):.1f} seconds",
                    'note': lightning_result.get('note', 'Lightning fast!')
                }
                return
            else:
                print(f"⚠️  Lightning deployment failed: {lightning_result.get('error')}")
                generation_status['message'] = 'Trying alternative hosting...'
        
        except Exception as lightning_error:
            print(f"⚠️  Lightning deployment error: {lightning_error}")
            generation_status['message'] = 'Trying alternative hosting...'
        
        # Fallback to simple hosting (quick but not lightning)
        try:
            print("🔄 Trying simple hosting fallback...")
            simple_result = quick_deploy(output_dir)
            
            if simple_result['status'] == 'success':
                generation_status['status'] = 'completed'
                generation_status['progress'] = 100
                generation_status['message'] = 'UI generated successfully!'
                generation_status['result'] = {
                    'components_generated': len(components_data),
                    'local_url': simple_result.get('local_url'),
                    'project_dir': output_dir,
                    'note': simple_result.get('note', 'Ready to use')
                }
                return
            else:
                print(f"⚠️  Simple hosting failed: {simple_result.get('error')}")
        
        except Exception as simple_error:
            print(f"⚠️  Simple hosting error: {simple_error}")
        
        # Final fallback - provide manual instructions
        generation_status['status'] = 'completed'
        generation_status['progress'] = 100
        generation_status['message'] = 'Project generated - manual setup required'
        generation_status['result'] = {
            'components_generated': len(components_data),
            'project_dir': output_dir,
            'manual_instructions': f'cd {output_dir} && npm install && npm run dev',
            'note': 'Project generated successfully, run manually for best performance'
        }
            
    except Exception as e:
        generation_status['status'] = 'error'
        generation_status['error'] = str(e)
        print(f"Error in UI generation: {e}")

@app.route('/status')
def get_status():
    """Get current generation status."""
    return jsonify(generation_status)

@app.route('/result')
def show_result():
    """Show generation result page."""
    if generation_status['status'] != 'completed':
        return redirect(url_for('index'))
    
    return render_template('result.html', result=generation_status['result'])

@app.route('/projects')
def list_projects():
    """List all generated projects."""
    projects = []
    projects_dir = 'generated_projects'
    
    if os.path.exists(projects_dir):
        for project_name in os.listdir(projects_dir):
            project_path = os.path.join(projects_dir, project_name)
            if os.path.isdir(project_path):
                # Get project info
                package_json_path = os.path.join(project_path, 'package.json')
                created_time = os.path.getctime(project_path)
                
                projects.append({
                    'name': project_name,
                    'path': project_path,
                    'created': datetime.fromtimestamp(created_time).strftime('%Y-%m-%d %H:%M:%S'),
                    'has_package_json': os.path.exists(package_json_path)
                })
    
    # Sort by creation time (newest first)
    projects.sort(key=lambda x: x['created'], reverse=True)
    
    return render_template('projects.html', projects=projects)

@app.route('/download/<project_name>')
def download_project(project_name):
    """Download a generated project as ZIP."""
    import zipfile
    import io
    
    project_path = os.path.join('generated_projects', secure_filename(project_name))
    if not os.path.exists(project_path):
        flash('Project not found', 'error')
        return redirect(url_for('list_projects'))
    
    # Create ZIP file in memory
    memory_file = io.BytesIO()
    
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(project_path):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, project_path)
                zf.write(file_path, arc_name)
    
    memory_file.seek(0)
    
    from flask import Response
    return Response(
        memory_file.getvalue(),
        mimetype='application/zip',
        headers={'Content-Disposition': f'attachment; filename={project_name}.zip'}
    )

@app.route('/preview/<project_name>')
def preview_project(project_name):
    """Preview a generated project."""
    project_path = os.path.join('generated_projects', secure_filename(project_name))
    if not os.path.exists(project_path):
        flash('Project not found', 'error')
        return redirect(url_for('list_projects'))
    
    # Start hosting for this project
    try:
        hosting = AppHosting(project_path)
        deployment_info = hosting.deploy_and_host(mode='development')
        
        if deployment_info['status'] == 'success':
            return render_template('preview.html', 
                                 project_name=project_name,
                                 local_url=deployment_info['local_url'],
                                 public_url=deployment_info.get('public_url'))
        else:
            flash(f'Failed to start preview: {deployment_info.get("error")}', 'error')
            return redirect(url_for('list_projects'))
            
    except Exception as e:
        flash(f'Error starting preview: {str(e)}', 'error')
        return redirect(url_for('list_projects'))

@app.route('/api/examples')
def get_examples():
    """Get example project descriptions."""
    examples = [
        {
            'title': 'E-commerce Dashboard',
            'description': 'A modern e-commerce dashboard for managing products, orders, and customer data. The design should be clean and professional with a sidebar navigation, product grid/list views, data tables for orders, customer profile cards, and modern buttons and form elements. Use a blue and gray color scheme with white backgrounds.'
        },
        {
            'title': 'Social Media App',
            'description': 'A social media application with a modern, mobile-first design. Include features like user profiles, news feed, post creation, messaging interface, and notification system. Use a clean, minimalist design with vibrant accent colors and smooth animations.'
        },
        {
            'title': 'Project Management Tool',
            'description': 'A project management dashboard with task boards, team collaboration features, project timelines, and progress tracking. The design should be professional and organized with clear visual hierarchy, using cards, lists, and charts to display information effectively.'
        },
        {
            'title': 'Learning Management System',
            'description': 'An educational platform with course listings, student dashboard, progress tracking, and interactive learning modules. The design should be friendly and accessible with clear navigation, progress indicators, and engaging visual elements.'
        },
        {
            'title': 'Healthcare Portal',
            'description': 'A healthcare management system with patient records, appointment scheduling, medical charts, and communication tools. The design should be clean, trustworthy, and accessible with a professional medical aesthetic using calming colors.'
        }
    ]
    
    return jsonify(examples)

if __name__ == '__main__':
    ensure_directories()
    print("🚀 Starting AI UI Generator Web Interface...")
    print("📱 Access the web UI at: http://localhost:5000")
    print("🔧 Upload UI screenshots and generate React apps!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
