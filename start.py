#!/usr/bin/env python3
"""
HealthCare Symptom Checker - Startup Script
Simple script to start the application with proper configuration
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import flask
        import flask_cors
        print("✅ Required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file with default configuration...")
        env_content = """# HealthCare Symptom Checker Configuration
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
SECRET_KEY=your_secret_key_here_change_in_production
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env file created")

def start_backend():
    """Start the Flask backend server"""
    print("🚀 Starting HealthCare Symptom Checker backend...")
    
    # Set environment variables
    os.environ['FLASK_DEBUG'] = 'True'
    os.environ['FLASK_HOST'] = '0.0.0.0'
    os.environ['FLASK_PORT'] = '5000'
    
    try:
        # Import and run the Flask app
        from app import app
        print("✅ Backend server started successfully!")
        print("🌐 API available at: http://localhost:5000")
        print("📊 Health check: http://localhost:5000/api/health")
        
        # Start the server
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=False  # Disable reloader to avoid duplicate processes
        )
        
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        print("Please check the error messages above and ensure all dependencies are installed")
        sys.exit(1)

def start_frontend():
    """Start a simple HTTP server for the frontend"""
    print("🌐 Starting frontend server...")
    
    try:
        # Start Python HTTP server
        import http.server
        import socketserver
        
        PORT = 8000
        Handler = http.server.SimpleHTTPRequestHandler
        
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"✅ Frontend server started at: http://localhost:{PORT}")
            print("📱 Open your browser and navigate to the URL above")
            print("🔄 Press Ctrl+C to stop the server")
            
            # Open browser automatically
            webbrowser.open(f'http://localhost:{PORT}')
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n🛑 Frontend server stopped")
                
    except Exception as e:
        print(f"❌ Error starting frontend server: {e}")
        print("You can still open index.html directly in your browser")

def main():
    """Main startup function"""
    print("🏥 HealthCare Symptom Checker - Startup Script")
    print("=" * 50)
    
    # Check prerequisites
    check_python_version()
    
    if not check_dependencies():
        print("\n💡 To install dependencies, run:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Create configuration files
    create_env_file()
    
    print("\n🎯 Choose an option:")
    print("1. Start backend only (API server)")
    print("2. Start frontend only (web interface)")
    print("3. Start both (recommended)")
    print("4. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == '1':
                print("\n" + "="*50)
                start_backend()
                break
                
            elif choice == '2':
                print("\n" + "="*50)
                start_frontend()
                break
                
            elif choice == '3':
                print("\n" + "="*50)
                print("🚀 Starting both backend and frontend...")
                
                # Start backend in a separate process
                import threading
                backend_thread = threading.Thread(target=start_backend, daemon=True)
                backend_thread.start()
                
                # Wait a moment for backend to start
                time.sleep(2)
                
                # Start frontend
                start_frontend()
                break
                
            elif choice == '4':
                print("👋 Goodbye!")
                sys.exit(0)
                
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please try again or choose option 4 to exit")

if __name__ == "__main__":
    main()
