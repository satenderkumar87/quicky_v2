#!/usr/bin/env python3
"""
Test script to verify the hosting system works correctly.
"""

import os
import sys
from agent.hosting import AppHosting

def test_hosting():
    """Test the hosting system with a generated project."""
    print("🧪 Testing Hosting System")
    print("=" * 40)
    
    # Find the most recent generated project
    projects_dir = "generated_projects"
    if not os.path.exists(projects_dir):
        print("❌ No generated_projects directory found")
        return False
    
    projects = [d for d in os.listdir(projects_dir) if os.path.isdir(os.path.join(projects_dir, d))]
    if not projects:
        print("❌ No projects found in generated_projects")
        return False
    
    # Use the most recent project
    projects.sort()
    latest_project = projects[-1]
    project_path = os.path.join(projects_dir, latest_project)
    
    print(f"📁 Testing project: {latest_project}")
    print(f"📍 Project path: {project_path}")
    
    # Check project structure
    required_files = ['package.json', 'vite.config.js', 'index.html']
    for file in required_files:
        file_path = os.path.join(project_path, file)
        if os.path.exists(file_path):
            print(f"✅ Found: {file}")
        else:
            print(f"❌ Missing: {file}")
            return False
    
    # Test hosting
    print("\n🚀 Starting Hosting Test...")
    hosting = AppHosting(project_path)
    
    try:
        # Test dependency installation
        print("\n📦 Testing dependency installation...")
        if hosting.install_dependencies():
            print("✅ Dependencies installed successfully")
        else:
            print("❌ Dependency installation failed")
            return False
        
        # Test development server
        print("\n🚀 Testing development server...")
        result = hosting.start_development_server()
        
        if result['status'] == 'success':
            print(f"✅ Development server started successfully")
            print(f"🌐 Local URL: {result['local_url']}")
            print(f"🔌 Port: {result['port']}")
            
            # Test if server is actually responding
            import requests
            try:
                response = requests.get(result['local_url'], timeout=10)
                if response.status_code == 200:
                    print("✅ Server is responding correctly")
                else:
                    print(f"⚠️  Server responded with status: {response.status_code}")
            except Exception as e:
                print(f"⚠️  Could not test server response: {e}")
            
            # Stop the server
            print("\n🛑 Stopping server...")
            hosting.stop_servers()
            print("✅ Server stopped")
            
            return True
        else:
            print(f"❌ Development server failed to start: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Hosting test failed: {e}")
        return False

def test_manual_commands():
    """Test manual npm commands in the project directory."""
    print("\n🔧 Testing Manual Commands")
    print("=" * 30)
    
    projects_dir = "generated_projects"
    projects = [d for d in os.listdir(projects_dir) if os.path.isdir(os.path.join(projects_dir, d))]
    if not projects:
        print("❌ No projects found")
        return False
    
    latest_project = sorted(projects)[-1]
    project_path = os.path.join(projects_dir, latest_project)
    
    print(f"📁 Testing in: {project_path}")
    
    import subprocess
    
    # Test npm list
    try:
        result = subprocess.run(
            ['npm', 'list', '--depth=0'],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=30
        )
        print(f"📋 npm list exit code: {result.returncode}")
        if result.stdout:
            print(f"📝 Installed packages: {len(result.stdout.splitlines())} lines")
        if result.stderr:
            print(f"⚠️  npm list warnings: {result.stderr[:200]}...")
    except Exception as e:
        print(f"❌ npm list failed: {e}")
    
    # Test npm run dev --help
    try:
        result = subprocess.run(
            ['npm', 'run', 'dev', '--', '--help'],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=10
        )
        print(f"🔧 npm run dev --help exit code: {result.returncode}")
        if result.returncode == 0:
            print("✅ Vite dev command is available")
        else:
            print("❌ Vite dev command failed")
            if result.stderr:
                print(f"Error: {result.stderr[:200]}...")
    except Exception as e:
        print(f"❌ npm run dev test failed: {e}")

if __name__ == "__main__":
    print("🧪 Hosting System Diagnostic")
    print("=" * 50)
    
    # Test hosting system
    if test_hosting():
        print("\n🎉 Hosting system test PASSED")
    else:
        print("\n❌ Hosting system test FAILED")
    
    # Test manual commands
    test_manual_commands()
    
    print("\n📋 Diagnostic complete!")
