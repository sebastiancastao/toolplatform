#!/usr/bin/env python3
"""
Setup script for Flask Keyword Search Application
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}:")
        print(f"Command: {command}")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 or higher is required!")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def create_virtual_environment():
    """Create a virtual environment"""
    if os.path.exists('venv'):
        print("📁 Virtual environment already exists")
        return True
    
    return run_command('python -m venv venv', 'Creating virtual environment')

def activate_and_install():
    """Activate virtual environment and install dependencies"""
    system = platform.system().lower()
    
    if system == 'windows':
        activate_cmd = 'venv\\Scripts\\activate'
        pip_cmd = 'venv\\Scripts\\pip'
    else:
        activate_cmd = 'source venv/bin/activate'
        pip_cmd = 'venv/bin/pip'
    
    # Install dependencies
    install_cmd = f'{pip_cmd} install -r requirements.txt'
    return run_command(install_cmd, 'Installing Python dependencies')

def check_credentials():
    """Check if Google Sheets credentials exist"""
    creds_path = 'C:/Users/sebas/Downloads/phonic-goods-317118-1353ffa1774d.json'
    if os.path.exists(creds_path):
        print("✅ Google Sheets credentials file found")
        return True
    else:
        print("⚠️  Google Sheets credentials file not found")
        print(f"Expected location: {creds_path}")
        print("Please ensure you have the Google service account JSON file")
        return False

def main():
    """Main setup function"""
    print("🚀 Flask Keyword Search App Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        print("❌ Failed to create virtual environment")
        sys.exit(1)
    
    # Install dependencies
    if not activate_and_install():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Check credentials
    check_credentials()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Activate virtual environment:")
    
    system = platform.system().lower()
    if system == 'windows':
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("2. Run the application:")
    print("   python app.py")
    print("3. Open your browser to: http://localhost:5000")
    
    print("\n📝 For Google Sheets integration:")
    print("- Ensure your credentials file is in the correct location")
    print("- Add URLs to column A in your spreadsheet")
    print("- Add keyword to cell D1 (optional)")
    
    print("\n🔗 Need help? Check the README.md file for detailed instructions.")

if __name__ == '__main__':
    main()