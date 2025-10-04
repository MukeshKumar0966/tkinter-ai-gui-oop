"""
Main entry point for the Tkinter AI GUI Application
This file brings everything together and runs the application
"""

import sys
import os
from main_application import MainApplication

def check_dependencies():
    """Check if required dependencies are installed"""
    required_modules = ['tkinter', 'transformers', 'torch', 'PIL']
    missing_modules = []
    
    for module in required_modules:
        try:
            if module == 'PIL':
                import PIL
            else:
                __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print("Missing required modules:")
        for module in missing_modules:
            print(f"  - {module}")
        print("\nPlease install missing modules using:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main function to start the application"""
    print("=" * 60)
    print("TKINTER AI GUI - OOP DEMONSTRATION")
    print("HIT137 Assignment 3")
    print("=" * 60)
    print()
    
    # Check dependencies
    print("Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    print("✓ All dependencies found")
    print()
    
    # Start application
    print("Starting application...")
    try:
        app = MainApplication()
        print("✓ Application initialized successfully")
        print("✓ GUI is now running...")
        print()
        print("INSTRUCTIONS:")
        print("1. Select a model from the dropdown menu")
        print("2. Click 'Load Model' and wait for confirmation")
        print("3. Choose input type (Text or Image)")
        print("4. Provide input data")
        print("5. Click 'Run Model 1' or 'Run Model 2' to process")
        print("6. View results in the output section")
        print()
        
        app.run()
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"Application error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("Application closed successfully")

if __name__ == "__main__":
    main()
