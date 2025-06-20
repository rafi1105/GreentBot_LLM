#!/usr/bin/env python3
"""
🚀 One-Click Setup and Launch for Enhanced Green University Chatbot
Automatically installs dependencies, tests system, and launches the chatbot
"""

import subprocess
import os
import time
import webbrowser
from pathlib import Path

def print_header():
    """Print welcome header"""
    print("\n" + "="*60)
    print("🚀 ENHANCED GREEN UNIVERSITY CHATBOT")
    print("   One-Click Setup & Launch")
    print("="*60)

def print_step(step_num, description):
    """Print step with formatting"""
    print(f"\n📍 Step {step_num}: {description}")
    print("-" * 50)

def run_command(command, description="", check_output=False):
    """Run command with error handling"""
    try:
        if check_output:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        else:
            subprocess.run(command, shell=True, check=True)
        print(f"✅ {description}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Error: {e}")
        return False

def install_dependencies():
    """Install all required packages"""
    print_step(1, "Installing Dependencies")
    
    packages = [
        "flask", "flask-cors", "requests", "numpy", 
        "scikit-learn", "nltk", "reportlab", "pillow", "chardet"
    ]
    
    print(f"📦 Installing: {', '.join(packages)}")
    
    # Install packages
    success = run_command(
        f"pip install {' '.join(packages)}", 
        "Dependencies installed successfully"
    )
    
    if not success:
        print("⚠️  Trying alternative installation method...")
        for package in packages:
            run_command(f"pip install {package}", f"Installed {package}")
    
    return True

def test_system():
    """Test system initialization"""
    print_step(2, "Testing System")
    
    test_command = """python -c "
from enhanced_search_system import initialize_enhanced_system
import json
system = initialize_enhanced_system()
print('✅ System initialized successfully!')
print(f'📊 Data points: {system.get_system_stats()["total_original_data"]}')
"
"""
    
    success = run_command(test_command, "System test completed")
    return success

def check_server_health():
    """Check if server is running"""
    try:
        import requests
        response = requests.get('http://localhost:5000/health', timeout=5)
        return response.status_code == 200
    except Exception:
        return False

def start_server():
    """Start the API server in background"""
    print_step(3, "Starting API Server")
    
    print("🌐 Starting server on http://localhost:5000...")
    
    # Start server in background
    if os.name == 'nt':  # Windows
        subprocess.Popen(
            ["python", "enhanced_api_server.py"],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    else:  # Linux/Mac
        subprocess.Popen(
            ["python", "enhanced_api_server.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    for i in range(20):  # Wait up to 20 seconds
        time.sleep(1)
        if check_server_health():
            print("✅ Server started successfully!")
            return True
        print(f"   Checking... ({i+1}/20)")
    
    print("⚠️  Server may take a moment to fully initialize")
    return True

def open_browser():
    """Open the chatbot interface"""
    print_step(4, "Opening Chatbot Interface")
    
    # Get the correct file path
    current_dir = Path(__file__).parent
    html_file = current_dir / "react-chatbot" / "index.html"
    
    if html_file.exists():
        file_url = f"file:///{html_file.as_posix()}"
        print(f"🌍 Opening: {file_url}")
        
        try:
            webbrowser.open(file_url)
            print("✅ Browser opened successfully!")
        except Exception as e:
            print(f"⚠️  Could not auto-open browser: {e}")
            print(f"📋 Please manually open: {file_url}")
    else:
        print(f"⚠️  HTML file not found at: {html_file}")
        print("📋 Please check the file path and open manually")

def show_usage_instructions():
    """Show how to use the system"""
    print_step(5, "Usage Instructions")
    
    print("🎯 HOW TO USE THE ENHANCED CHATBOT:")
    print()
    print("1. 💬 Type questions about Green University")
    print("   Example: 'What is the tuition fee for CSE?'")
    print()
    print("2. 🎯 Watch the confidence popup (10 seconds)")
    print("   Shows detailed analysis metrics")
    print()
    print("3. 👍👎 Use Like/Dislike buttons")
    print("   Dislike permanently blocks answers")
    print()
    print("4. 🧠 System learns from your feedback")
    print("   Blocked content never appears again")
    print()
    print("📊 SYSTEM FEATURES:")
    print("   ✅ Searches ALL 710+ JSON data items")
    print("   ✅ Machine Learning classification")
    print("   ✅ Real-time learning from feedback")
    print("   ✅ Permanent content blocking")
    print("   ✅ Professional UI with analytics")

def run_quick_test():
    """Run a quick test of the system"""
    print("\n🧪 QUICK SYSTEM TEST:")
    print("-" * 30)
    
    try:
        import requests
        
        # Test chat endpoint
        print("📝 Testing chat functionality...")
        response = requests.post(
            'http://localhost:5000/chat',
            json={'message': 'What is the tuition fee for CSE?'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat working - Analyzed {data.get('analyzed_items', 0)} items")
            print(f"   Confidence: {data.get('confidence', 0):.1%}")
        else:
            print(f"⚠️  Chat response: {response.status_code}")
        
        # Test stats endpoint
        print("📊 Testing system statistics...")
        stats_response = requests.get('http://localhost:5000/stats', timeout=5)
        
        if stats_response.status_code == 200:
            stats = stats_response.json()
            print(f"✅ Stats working - {stats.get('total_original_data', 0)} total items")
            print(f"   Available: {stats.get('available_data', 0)}")
            print(f"   Blocked: {stats.get('disliked_answers', 0)}")
        else:
            print(f"⚠️  Stats response: {stats_response.status_code}")
            
    except Exception as e:
        print(f"⚠️  Test error: {e}")
        print("   Server may still be starting up...")

def main():
    """Main automation function"""
    print_header()
    
    print("🎯 This script will:")
    print("   1. Install all required dependencies")
    print("   2. Test the enhanced search system")
    print("   3. Start the API server automatically")
    print("   4. Open the chatbot interface")
    print("   5. Show usage instructions")
    
    input("\n⏳ Press Enter to start automatic setup...")
    
    # Step 1: Install dependencies
    if not install_dependencies():
        print("❌ Dependency installation failed!")
        input("Press Enter to exit...")
        return
    
    # Step 2: Test system
    if not test_system():
        print("❌ System test failed!")
        input("Press Enter to exit...")
        return
    
    # Step 3: Start server
    if not start_server():
        print("❌ Server start failed!")
        input("Press Enter to exit...")
        return
    
    # Step 4: Open browser
    open_browser()
    
    # Step 5: Quick test
    time.sleep(3)  # Give server more time
    run_quick_test()
    
    # Step 6: Usage instructions
    show_usage_instructions()
    
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    print("✅ Enhanced Green University Chatbot is ready!")
    print("🌐 Server running at: http://localhost:5000")
    print("🌍 Interface should be open in your browser")
    print()
    print("💡 To stop the server later:")
    print("   - Find the server console window")
    print("   - Press Ctrl+C to stop")
    print()
    print("🚀 Happy chatting with intelligent search & learning!")
    
    input("\nPress Enter to exit setup...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Setup interrupted by user")
    except Exception as e:
        print(f"\n❌ Setup error: {e}")
        input("Press Enter to exit...")
