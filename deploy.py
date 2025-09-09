#!/usr/bin/env python3
"""
Deployment script for Beneath the Blue Django application
"""

import os
import sys
import subprocess

def run_command(command):
    """Run a command and return its output"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running command: {command}")
            print(f"Error: {result.stderr}")
            return False
        print(result.stdout)
        return True
    except Exception as e:
        print(f"Exception running command: {command}")
        print(f"Exception: {e}")
        return False

def main():
    print("🌊 Beneath the Blue Deployment Script 🌊")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: manage.py not found. Run this script from the Django project root.")
        sys.exit(1)
    
    print("📦 Installing dependencies...")
    if not run_command("pip install -r requirements.txt"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    print("🔧 Creating migrations...")
    if not run_command("python manage.py makemigrations"):
        print("⚠️  Warning: Failed to create migrations, continuing...")
    
    print("🗄️  Applying migrations...")
    if not run_command("python manage.py migrate"):
        print("⚠️  Warning: Failed to apply migrations, continuing...")
    
    print("📁 Collecting static files...")
    if not run_command("python manage.py collectstatic --noinput"):
        print("⚠️  Warning: Failed to collect static files")
    
    print("👤 Creating superuser (if needed)...")
    print("You can create a superuser later with: python manage.py createsuperuser")
    
    print("✅ Deployment preparation complete!")
    print("🚀 To run the server: python manage.py runserver")
    print("🔧 Admin panel: http://localhost:8000/admin/")

if __name__ == "__main__":
    main()
