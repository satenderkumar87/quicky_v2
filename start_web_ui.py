#!/usr/bin/env python3
"""
Startup script for AI UI Generator Web Interface
"""

import os
import sys
import subprocess

def main():
    print("🚀 Starting AI UI Generator Web Interface...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('web_ui/app.py'):
        print("❌ Error: Please run this script from the project root directory")
        print("   Current directory:", os.getcwd())
        print("   Expected files: web_ui/app.py")
        sys.exit(1)
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Virtual environment not detected")
        print("   Consider activating the virtual environment:")
        print("   source venv/bin/activate")
        print()
    
    # Check if Flask is installed
    try:
        import flask
        print(f"✅ Flask {flask.__version__} detected")
    except ImportError:
        print("❌ Flask not found. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'Flask==3.0.0'])
        print("✅ Flask installed")
    
    # Set environment variables
    os.environ['FLASK_APP'] = 'web_ui/app.py'
    os.environ['FLASK_ENV'] = 'development'
    
    print("\n🌐 Web Interface Information:")
    print("   URL: http://localhost:5000")
    print("   Features:")
    print("   • Upload UI screenshots")
    print("   • Add project descriptions")
    print("   • Generate React applications")
    print("   • Auto-hosting with shareable URLs")
    print("   • Project management")
    print()
    
    print("🔧 Usage Instructions:")
    print("   1. Open http://localhost:5000 in your browser")
    print("   2. Upload UI screenshots (PNG, JPG, etc.)")
    print("   3. Describe your project requirements")
    print("   4. Click 'Generate React Application'")
    print("   5. Get live URLs for your generated app!")
    print()
    
    print("⚡ Starting Flask development server...")
    print("   Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Change to web_ui directory and start Flask
    os.chdir('web_ui')
    
    try:
        # Start Flask app
        import app
        app.app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("💡 Try running directly: cd web_ui && python app.py")
        sys.exit(1)

if __name__ == '__main__':
    main()
