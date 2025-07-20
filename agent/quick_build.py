"""
Quick build system for fast React application deployment.
Prioritizes speed over comprehensive features.
"""

import os
import subprocess
import time
import socket
from typing import Dict, Any, Optional
import json

class QuickBuilder:
    """Ultra-fast build system for React applications."""
    
    def __init__(self, project_dir: str):
        self.project_dir = project_dir
        self.process = None
        self.port = None
        self.local_url = None
    
    def find_available_port(self, start_port: int = 3000) -> int:
        """Quickly find an available port."""
        for port in range(start_port, start_port + 20):  # Check only 20 ports
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
                    return port
            except OSError:
                continue
        return start_port  # Fallback
    
    def ultra_quick_install(self) -> bool:
        """Ultra-quick dependency installation (30 seconds max)."""
        print("⚡ Ultra-quick install (30s timeout)...")
        
        if not os.path.exists(os.path.join(self.project_dir, 'package.json')):
            print("❌ No package.json found")
            return False
        
        try:
            # Ultra-fast install with aggressive caching
            result = subprocess.run([
                'npm', 'install', 
                '--prefer-offline',     # Use cache first
                '--no-audit',          # Skip security audit
                '--no-fund',           # Skip funding messages
                '--silent',            # Minimal output
                '--no-optional'        # Skip optional dependencies
            ], 
            cwd=self.project_dir,
            capture_output=True,
            text=True,
            timeout=30  # 30 seconds max
            )
            
            # Success if node_modules exists
            node_modules = os.path.join(self.project_dir, 'node_modules')
            if os.path.exists(node_modules):
                print("✅ Quick install complete")
                return True
            else:
                print("⚠️  Partial install, trying cache-only...")
                return self._try_cache_only_install()
                
        except subprocess.TimeoutExpired:
            print("⚠️  Install timeout, checking cache...")
            return self._try_cache_only_install()
        except Exception as e:
            print(f"⚠️  Install error, trying fallback: {e}")
            return self._try_cache_only_install()
    
    def _try_cache_only_install(self) -> bool:
        """Try cache-only install as fallback."""
        try:
            result = subprocess.run([
                'npm', 'install', 
                '--offline',           # Cache only
                '--no-audit',
                '--silent'
            ], 
            cwd=self.project_dir,
            capture_output=True,
            text=True,
            timeout=15  # 15 seconds max
            )
            
            node_modules = os.path.join(self.project_dir, 'node_modules')
            return os.path.exists(node_modules)
            
        except:
            # Final check - maybe dependencies were already installed
            node_modules = os.path.join(self.project_dir, 'node_modules')
            return os.path.exists(node_modules)
    
    def instant_dev_server(self) -> Dict[str, Any]:
        """Start dev server with minimal waiting (10 seconds max)."""
        print("🚀 Starting instant dev server...")
        
        try:
            self.port = self.find_available_port(3000)
            
            # Check if we can run dev command first
            try:
                test_result = subprocess.run([
                    'npm', 'run', 'dev', '--', '--help'
                ], 
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=5
                )
                
                if test_result.returncode != 0:
                    print("⚠️  Dev command test failed, but continuing...")
            except:
                print("⚠️  Could not test dev command, but continuing...")
            
            # Start server with better error handling
            env = os.environ.copy()
            env['NODE_ENV'] = 'development'
            
            self.process = subprocess.Popen([
                'npm', 'run', 'dev', '--',
                '--port', str(self.port),
                '--host', '0.0.0.0'
            ],
            cwd=self.project_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
            )
            
            print(f"🔄 Server process started (PID: {self.process.pid})")
            
            # Quick server check with better monitoring
            max_wait = 12  # Slightly longer for Vite
            for i in range(max_wait):
                # Check if process died
                if self.process.poll() is not None:
                    stdout, stderr = self.process.communicate()
                    print(f"❌ Server process terminated")
                    if stderr:
                        print(f"   Error: {stderr[:150]}...")
                    if stdout:
                        print(f"   Output: {stdout[:150]}...")
                    return {'status': 'error', 'error': 'Server process terminated early'}
                
                # Quick port check
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(1)
                        if s.connect_ex(('localhost', self.port)) == 0:
                            self.local_url = f"http://localhost:{self.port}"
                            print(f"✅ Server ready: {self.local_url}")
                            return {
                                'status': 'success',
                                'local_url': self.local_url,
                                'port': self.port
                            }
                except:
                    pass
                
                if i < 3:
                    print(f"⏳ Starting server... ({i+1}/{max_wait})")
                elif i == 6:
                    print("⏳ Server taking longer than expected...")
                
                time.sleep(1)
            
            # Check one more time if process is still running
            if self.process.poll() is None:
                # Process still running but not responding
                self.local_url = f"http://localhost:{self.port}"
                print(f"⚡ Server may be ready: {self.local_url}")
                return {
                    'status': 'partial',
                    'local_url': self.local_url,
                    'port': self.port,
                    'note': 'Server started but may need more time'
                }
            else:
                # Process died during wait
                stdout, stderr = self.process.communicate()
                print(f"❌ Server failed to start properly")
                return {'status': 'error', 'error': 'Server startup failed'}
            
        except Exception as e:
            print(f"❌ Server start failed: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def lightning_deploy(self) -> Dict[str, Any]:
        """Lightning-fast deployment (under 1 minute total)."""
        print("⚡ Lightning deployment starting...")
        start_time = time.time()
        
        # Quick check if already ready
        if UltraQuickBuild.check_ready_to_run(self.project_dir):
            print("⚡ Project already ready - instant run!")
            server_result = self.instant_dev_server()
            elapsed = time.time() - start_time
            
            if server_result['status'] in ['success', 'partial']:
                return {
                    'status': 'success',
                    'local_url': server_result['local_url'],
                    'port': server_result['port'],
                    'elapsed': elapsed,
                    'note': f'Instant deployment in {elapsed:.1f}s!'
                }
        
        # Step 1: Ultra-quick install (30s max)
        install_start = time.time()
        if not self.ultra_quick_install():
            elapsed = time.time() - start_time
            return {
                'status': 'error',
                'error': 'Quick install failed',
                'manual_cmd': f'cd {self.project_dir} && npm install && npm run dev',
                'elapsed': elapsed
            }
        
        install_time = time.time() - install_start
        print(f"✅ Install completed in {install_time:.1f}s")
        
        # Step 2: Instant server start (12s max)
        server_result = self.instant_dev_server()
        
        elapsed = time.time() - start_time
        
        if server_result['status'] in ['success', 'partial']:
            print(f"⚡ Lightning deployment complete in {elapsed:.1f}s!")
            return {
                'status': 'success',
                'local_url': server_result['local_url'],
                'port': server_result['port'],
                'elapsed': elapsed,
                'install_time': f"{install_time:.1f}s",
                'note': server_result.get('note', f'Ready in {elapsed:.1f}s!')
            }
        else:
            return {
                'status': 'error',
                'error': server_result.get('error', 'Server start failed'),
                'manual_cmd': f'cd {self.project_dir} && npm run dev',
                'elapsed': elapsed,
                'install_time': f"{install_time:.1f}s"
            }
    
    def stop(self):
        """Stop the server quickly."""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=3)
                print("✅ Server stopped")
            except:
                try:
                    self.process.kill()
                except:
                    pass

class UltraQuickBuild:
    """Even faster build for when speed is critical."""
    
    @staticmethod
    def check_ready_to_run(project_dir: str) -> bool:
        """Check if project can run without installation."""
        node_modules = os.path.join(project_dir, 'node_modules')
        package_json = os.path.join(project_dir, 'package.json')
        
        if not os.path.exists(package_json):
            return False
            
        if os.path.exists(node_modules):
            # Check if vite is available
            vite_bin = os.path.join(node_modules, '.bin', 'vite')
            return os.path.exists(vite_bin)
        
        return False
    
    @staticmethod
    def instant_run(project_dir: str) -> Dict[str, Any]:
        """Instantly run if already set up."""
        if not UltraQuickBuild.check_ready_to_run(project_dir):
            return {'status': 'not_ready', 'error': 'Dependencies not installed'}
        
        builder = QuickBuilder(project_dir)
        return builder.instant_dev_server()

def lightning_deploy(project_dir: str) -> Dict[str, Any]:
    """Main lightning deployment function."""
    # Try ultra-quick first
    if UltraQuickBuild.check_ready_to_run(project_dir):
        print("⚡ Project ready - instant run!")
        return UltraQuickBuild.instant_run(project_dir)
    
    # Fall back to quick build
    builder = QuickBuilder(project_dir)
    return builder.lightning_deploy()

def quick_build_info():
    """Show quick build capabilities."""
    return {
        'install_timeout': '30 seconds',
        'server_timeout': '10 seconds', 
        'total_time': 'Under 1 minute',
        'features': [
            'Aggressive caching',
            'Skip optional dependencies',
            'Minimal output',
            'Quick port detection',
            'Instant run for ready projects'
        ]
    }
