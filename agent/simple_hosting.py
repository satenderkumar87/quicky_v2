"""
Simplified hosting module that focuses on reliability over features.
"""

import os
import subprocess
import time
import socket
from typing import Dict, Any

class SimpleHosting:
    """Simplified hosting that prioritizes reliability."""
    
    def __init__(self, project_dir: str):
        self.project_dir = project_dir
        self.process = None
        self.port = None
        self.local_url = None
    
    def find_available_port(self, start_port: int = 3000) -> int:
        """Find an available port."""
        for port in range(start_port, start_port + 50):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
                    return port
            except OSError:
                continue
        return start_port  # Fallback
    
    def quick_install(self) -> bool:
        """Quick dependency installation with timeout."""
        print("📦 Quick installing dependencies...")
        
        if not os.path.exists(os.path.join(self.project_dir, 'package.json')):
            print("❌ No package.json found")
            return False
        
        try:
            # Quick install with timeout
            result = subprocess.run(
                ['npm', 'install', '--prefer-offline', '--no-audit'],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=120  # 2 minutes max
            )
            
            # Check if node_modules exists (success indicator)
            node_modules = os.path.join(self.project_dir, 'node_modules')
            if os.path.exists(node_modules):
                print("✅ Dependencies installed")
                return True
            else:
                print("⚠️  Dependencies may not be fully installed")
                return False
                
        except subprocess.TimeoutExpired:
            print("⚠️  Installation timed out, but may have partially succeeded")
            # Check if node_modules exists
            return os.path.exists(os.path.join(self.project_dir, 'node_modules'))
        except Exception as e:
            print(f"⚠️  Installation error: {e}")
            return False
    
    def start_server(self) -> Dict[str, Any]:
        """Start development server with quick timeout."""
        print("🚀 Starting development server...")
        
        try:
            self.port = self.find_available_port(3000)
            
            # Start server with timeout monitoring
            self.process = subprocess.Popen(
                ['npm', 'run', 'dev', '--', '--port', str(self.port), '--host', '0.0.0.0'],
                cwd=self.project_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Quick check if server starts
            max_wait = 15  # 15 seconds max
            for i in range(max_wait):
                if self.process.poll() is not None:
                    # Process died
                    stdout, stderr = self.process.communicate()
                    print(f"❌ Server process died: {stderr[:200]}...")
                    return {'status': 'error', 'error': 'Server process terminated'}
                
                # Check if port is responding
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(1)
                        if s.connect_ex(('localhost', self.port)) == 0:
                            self.local_url = f"http://localhost:{self.port}"
                            print(f"✅ Server started: {self.local_url}")
                            return {
                                'status': 'success',
                                'local_url': self.local_url,
                                'port': self.port
                            }
                except:
                    pass
                
                time.sleep(1)
            
            # Timeout reached
            print("⚠️  Server may be starting but not responding yet")
            self.local_url = f"http://localhost:{self.port}"
            return {
                'status': 'partial',
                'local_url': self.local_url,
                'port': self.port,
                'note': 'Server started but may need more time to be ready'
            }
            
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def deploy_quick(self) -> Dict[str, Any]:
        """Quick deployment with minimal waiting."""
        print("🚀 Quick deployment starting...")
        
        # Step 1: Quick install
        if not self.quick_install():
            return {
                'status': 'error',
                'error': 'Failed to install dependencies',
                'manual_instructions': f'Run manually: cd {self.project_dir} && npm install && npm run dev'
            }
        
        # Step 2: Start server
        server_result = self.start_server()
        
        if server_result['status'] in ['success', 'partial']:
            print("🎉 Quick deployment complete!")
            return {
                'status': 'success',
                'local_url': server_result['local_url'],
                'port': server_result['port'],
                'note': server_result.get('note', 'Server ready')
            }
        else:
            return {
                'status': 'error',
                'error': server_result.get('error', 'Unknown error'),
                'manual_instructions': f'Run manually: cd {self.project_dir} && npm install && npm run dev'
            }
    
    def stop(self):
        """Stop the server."""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
                print("✅ Server stopped")
            except:
                try:
                    self.process.kill()
                except:
                    pass

def quick_deploy(project_dir: str) -> Dict[str, Any]:
    """Quick deployment function."""
    hosting = SimpleHosting(project_dir)
    return hosting.deploy_quick()
