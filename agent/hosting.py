"""
Hosting module for automatically building and serving generated React applications.
Provides local hosting with public URL sharing capabilities.
"""

import os
import subprocess
import time
import threading
import socket
from typing import Optional, Dict, Any
import json
import signal
import sys

class AppHosting:
    def __init__(self, project_dir: str):
        self.project_dir = project_dir
        self.dev_process = None
        self.build_process = None
        self.preview_process = None
        self.local_url = None
        self.public_url = None
        self.port = None
        
    def find_available_port(self, start_port: int = 3000) -> int:
        """Find an available port starting from the given port."""
        for port in range(start_port, start_port + 100):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
                    return port
            except OSError:
                continue
        raise RuntimeError("No available ports found")
    
    def install_dependencies(self) -> bool:
        """Install npm dependencies for the generated project."""
        print("📦 Installing dependencies...")
        print(f"🔍 Project directory: {self.project_dir}")
        
        # Check if project directory exists
        if not os.path.exists(self.project_dir):
            print(f"❌ Project directory does not exist: {self.project_dir}")
            return False
        
        # Check if package.json exists
        package_json_path = os.path.join(self.project_dir, 'package.json')
        if not os.path.exists(package_json_path):
            print(f"❌ package.json not found at: {package_json_path}")
            return False
        
        print(f"✅ Found package.json at: {package_json_path}")
        
        try:
            # First try npm install with better error reporting
            print("🔄 Running npm install...")
            result = subprocess.run(
                ['npm', 'install'],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            print(f"📊 npm install exit code: {result.returncode}")
            
            if result.stdout:
                print(f"📝 npm stdout: {result.stdout[:500]}...")  # First 500 chars
            
            if result.stderr:
                print(f"⚠️  npm stderr: {result.stderr[:500]}...")  # First 500 chars
            
            if result.returncode == 0:
                print("✅ Dependencies installed successfully")
                
                # Verify node_modules was created
                node_modules_path = os.path.join(self.project_dir, 'node_modules')
                if os.path.exists(node_modules_path):
                    print(f"✅ node_modules directory created: {node_modules_path}")
                    
                    # Check if vite is installed
                    vite_path = os.path.join(node_modules_path, '.bin', 'vite')
                    if os.path.exists(vite_path):
                        print("✅ Vite binary found")
                    else:
                        print("⚠️  Vite binary not found, but continuing...")
                else:
                    print("⚠️  node_modules directory not found")
                
                return True
            else:
                print(f"⚠️  npm install had warnings (exit code: {result.returncode})")
                
                # Check if node_modules exists despite warnings
                node_modules_path = os.path.join(self.project_dir, 'node_modules')
                if os.path.exists(node_modules_path):
                    print("✅ node_modules exists despite warnings, continuing...")
                    return True
                else:
                    print("❌ node_modules not created, trying alternative approach...")
                    
                    # Try with --force flag
                    print("🔄 Trying npm install --force...")
                    result2 = subprocess.run(
                        ['npm', 'install', '--force'],
                        cwd=self.project_dir,
                        capture_output=True,
                        text=True,
                        timeout=300
                    )
                    
                    if result2.returncode == 0 or os.path.exists(node_modules_path):
                        print("✅ Dependencies installed with --force")
                        return True
                    else:
                        print(f"❌ Failed to install dependencies: {result2.stderr}")
                        return False
                
        except subprocess.TimeoutExpired:
            print("❌ Dependency installation timed out (5 minutes)")
            return False
        except Exception as e:
            print(f"❌ Error installing dependencies: {e}")
            return False
    
    def build_application(self) -> bool:
        """Build the React application for production."""
        print("🔨 Building application...")
        
        try:
            result = subprocess.run(
                ['npm', 'run', 'build'],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=180  # 3 minutes timeout
            )
            
            if result.returncode == 0:
                print("✅ Application built successfully")
                return True
            else:
                print(f"❌ Build failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Build process timed out")
            return False
        except Exception as e:
            print(f"❌ Error building application: {e}")
            return False
    
    def start_development_server(self) -> Dict[str, Any]:
        """Start the development server and return connection details."""
        print("🚀 Starting development server...")
        
        try:
            # Check if npm run dev script exists
            package_json_path = os.path.join(self.project_dir, 'package.json')
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
                scripts = package_data.get('scripts', {})
                if 'dev' not in scripts:
                    raise RuntimeError("No 'dev' script found in package.json")
                print(f"✅ Found dev script: {scripts['dev']}")
            
            # Find available port
            self.port = self.find_available_port(3000)
            print(f"🔌 Using port: {self.port}")
            
            # Check if vite is available
            vite_check = subprocess.run(
                ['npm', 'run', 'dev', '--', '--help'],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if vite_check.returncode != 0:
                print("⚠️  Vite dev command test failed, but continuing...")
                print(f"Vite check stderr: {vite_check.stderr[:200]}...")
            
            # Start Vite dev server
            env = os.environ.copy()
            env['PORT'] = str(self.port)
            
            print(f"🔄 Starting: npm run dev -- --port {self.port} --host")
            
            self.dev_process = subprocess.Popen(
                ['npm', 'run', 'dev', '--', '--port', str(self.port), '--host'],
                cwd=self.project_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env
            )
            
            print(f"🔄 Process started with PID: {self.dev_process.pid}")
            
            # Wait for server to start with better monitoring
            max_attempts = 30
            for attempt in range(max_attempts):
                # Check if process is still running
                if self.dev_process.poll() is not None:
                    # Process has terminated
                    stdout, stderr = self.dev_process.communicate()
                    print(f"❌ Development server process terminated early")
                    print(f"Exit code: {self.dev_process.returncode}")
                    if stdout:
                        print(f"Stdout: {stdout[:500]}...")
                    if stderr:
                        print(f"Stderr: {stderr[:500]}...")
                    raise RuntimeError("Development server process terminated")
                
                # Check if port is available
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(1)
                        result = s.connect_ex(('localhost', self.port))
                        if result == 0:
                            print(f"✅ Server responding on port {self.port}")
                            break
                except Exception as e:
                    pass
                
                print(f"⏳ Waiting for server... (attempt {attempt + 1}/{max_attempts})")
                time.sleep(2)
            else:
                # Timeout reached, get process output
                if self.dev_process.poll() is None:
                    # Process still running but not responding
                    print("❌ Server started but not responding on expected port")
                    # Try to get some output
                    try:
                        stdout, stderr = self.dev_process.communicate(timeout=5)
                        if stdout:
                            print(f"Process stdout: {stdout[:500]}...")
                        if stderr:
                            print(f"Process stderr: {stderr[:500]}...")
                    except:
                        pass
                
                raise RuntimeError("Server failed to start within timeout")
            
            self.local_url = f"http://localhost:{self.port}"
            
            print(f"✅ Development server started successfully")
            print(f"🌐 Local URL: {self.local_url}")
            
            return {
                'status': 'success',
                'local_url': self.local_url,
                'port': self.port,
                'process_id': self.dev_process.pid
            }
            
        except Exception as e:
            print(f"❌ Failed to start development server: {e}")
            
            # Clean up process if it exists
            if hasattr(self, 'dev_process') and self.dev_process:
                try:
                    self.dev_process.terminate()
                except:
                    pass
            
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def start_preview_server(self) -> Dict[str, Any]:
        """Start preview server for built application."""
        print("🔍 Starting preview server...")
        
        try:
            # Find available port
            self.port = self.find_available_port(4173)
            
            # Start Vite preview server
            self.preview_process = subprocess.Popen(
                ['npm', 'run', 'preview', '--', '--port', str(self.port), '--host'],
                cwd=self.project_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for server to start
            time.sleep(3)
            
            self.local_url = f"http://localhost:{self.port}"
            
            print(f"✅ Preview server started successfully")
            print(f"🌐 Local URL: {self.local_url}")
            
            return {
                'status': 'success',
                'local_url': self.local_url,
                'port': self.port,
                'process_id': self.preview_process.pid
            }
            
        except Exception as e:
            print(f"❌ Failed to start preview server: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def create_public_tunnel(self) -> Optional[str]:
        """Create a public tunnel using ngrok or similar service."""
        print("🌍 Creating public tunnel...")
        
        try:
            # Check if ngrok is available
            result = subprocess.run(['which', 'ngrok'], capture_output=True)
            if result.returncode != 0:
                print("⚠️  ngrok not found. Install ngrok for public URL sharing:")
                print("   Visit: https://ngrok.com/download")
                print("   Or use: snap install ngrok")
                return None
            
            # Start ngrok tunnel
            ngrok_process = subprocess.Popen(
                ['ngrok', 'http', str(self.port), '--log=stdout'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for ngrok to establish tunnel
            time.sleep(5)
            
            # Get ngrok API to fetch public URL
            try:
                import requests
                response = requests.get('http://localhost:4040/api/tunnels')
                tunnels = response.json()
                
                if tunnels.get('tunnels'):
                    public_url = tunnels['tunnels'][0]['public_url']
                    self.public_url = public_url
                    print(f"✅ Public tunnel created: {public_url}")
                    return public_url
                else:
                    print("❌ Failed to get public URL from ngrok")
                    return None
                    
            except Exception as e:
                print(f"❌ Error getting ngrok URL: {e}")
                return None
                
        except Exception as e:
            print(f"❌ Failed to create public tunnel: {e}")
            return None
    
    def deploy_and_host(self, mode: str = 'development') -> Dict[str, Any]:
        """Complete deployment workflow: install, build (if needed), and host."""
        print("🚀 Starting deployment workflow...")
        
        deployment_info = {
            'status': 'starting',
            'local_url': None,
            'public_url': None,
            'mode': mode,
            'timestamp': time.time()
        }
        
        # Step 1: Install dependencies
        if not self.install_dependencies():
            deployment_info['status'] = 'failed'
            deployment_info['error'] = 'Failed to install dependencies'
            return deployment_info
        
        # Step 2: Build or start development server
        if mode == 'production':
            if not self.build_application():
                deployment_info['status'] = 'failed'
                deployment_info['error'] = 'Failed to build application'
                return deployment_info
            
            # Start preview server
            server_info = self.start_preview_server()
        else:
            # Start development server
            server_info = self.start_development_server()
        
        if server_info['status'] != 'success':
            deployment_info['status'] = 'failed'
            deployment_info['error'] = server_info.get('error', 'Failed to start server')
            return deployment_info
        
        deployment_info['local_url'] = server_info['local_url']
        deployment_info['port'] = server_info['port']
        
        # Step 3: Create public tunnel (optional)
        public_url = self.create_public_tunnel()
        if public_url:
            deployment_info['public_url'] = public_url
        
        deployment_info['status'] = 'success'
        
        print("\n🎉 Deployment Complete!")
        print(f"📱 Local URL: {deployment_info['local_url']}")
        if deployment_info['public_url']:
            print(f"🌍 Public URL: {deployment_info['public_url']}")
        print(f"⚙️  Mode: {mode}")
        
        return deployment_info
    
    def stop_servers(self):
        """Stop all running servers."""
        print("🛑 Stopping servers...")
        
        if self.dev_process:
            try:
                self.dev_process.terminate()
                self.dev_process.wait(timeout=5)
                print("✅ Development server stopped")
            except:
                try:
                    self.dev_process.kill()
                except:
                    pass
        
        if self.preview_process:
            try:
                self.preview_process.terminate()
                self.preview_process.wait(timeout=5)
                print("✅ Preview server stopped")
            except:
                try:
                    self.preview_process.kill()
                except:
                    pass
    
    def get_status(self) -> Dict[str, Any]:
        """Get current hosting status."""
        return {
            'local_url': self.local_url,
            'public_url': self.public_url,
            'port': self.port,
            'dev_running': self.dev_process and self.dev_process.poll() is None,
            'preview_running': self.preview_process and self.preview_process.poll() is None
        }
    
    def __del__(self):
        """Cleanup when object is destroyed."""
        self.stop_servers()
