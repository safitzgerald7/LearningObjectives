#!/usr/bin/env python3
"""
Startup script for the Learning Objectives Generator
Provides easy access to all available modes
"""

import sys
import subprocess
import os

def print_header():
    print("🎯 Learning Objectives Generator")
    print("=" * 50)
    print("Choose how you'd like to use the Learning Objectives Generator:")
    print()

def print_options():
    print("1. 🌐 Web Interface (Recommended)")
    print("   - Easy-to-use browser interface")
    print("   - No additional dependencies required")
    print()
    print("2. 💻 Command Line (Single Goal)")
    print("   - Enter a goal as a command line argument")
    print()
    print("3. 💬 Interactive Command Line")
    print("   - Enter multiple goals in a conversational mode")
    print()
    print("4. ❓ Show Help")
    print("   - Display detailed usage instructions")
    print()
    print("5. 🚪 Exit")
    print()

def start_web_interface():
    print("Starting web interface...")
    print("Your browser should open automatically.")
    print("If not, go to: http://localhost:8080")
    print("Press Ctrl+C to stop the server when done.")
    print()
    
    try:
        # Try to open browser automatically
        import webbrowser
        import threading
        import time
        
        def open_browser():
            time.sleep(2)  # Wait for server to start
            webbrowser.open('http://localhost:8080')
        
        # Start browser opener in background
        threading.Thread(target=open_browser, daemon=True).start()
        
        # Start web server
        subprocess.run([sys.executable, 'simple_web_server.py'])
    except KeyboardInterrupt:
        print("\nWeb server stopped.")
    except Exception as e:
        print(f"Error starting web interface: {e}")

def start_command_line():
    goal = input("Enter your course goal: ").strip()
    if goal:
        try:
            subprocess.run([sys.executable, 'learning_objectives_generator.py', goal])
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("No goal provided.")

def start_interactive():
    try:
        subprocess.run([sys.executable, 'learning_objectives_generator.py', '-i'])
    except Exception as e:
        print(f"Error: {e}")

def show_help():
    print("📚 Learning Objectives Generator Help")
    print("=" * 40)
    print()
    print("DESCRIPTION:")
    print("  This tool helps instructional designers create learning objectives")
    print("  aligned to Bloom's Taxonomy levels. It analyzes course goals and")
    print("  generates structured objectives with proper hierarchical numbering.")
    print()
    print("BLOOM'S TAXONOMY LEVELS:")
    print("  1. Remember - Recall facts and basic concepts")
    print("  2. Understand - Explain ideas or concepts")
    print("  3. Apply - Use information in new situations")
    print("  4. Analyze - Draw connections among ideas")
    print("  5. Evaluate - Justify a stand or decision")
    print("  6. Create - Produce new or original work")
    print()
    print("EXAMPLE INPUT:")
    print("  'The goal is for learners to know the supplies needed for each emergency procedure'")
    print()
    print("EXAMPLE OUTPUT:")
    print("  1.0.0. Layout the supplies needed for each emergency procedure. (apply)")
    print("     1.1.0. List the supplies needed for each emergency procedure. (remember)")
    print("         1.1.1. Explain the purpose of each supply item. (understand)")
    print()
    print("DIRECT COMMAND LINE USAGE:")
    print("  python3 learning_objectives_generator.py 'your goal here'")
    print("  python3 learning_objectives_generator.py -i  # interactive mode")
    print("  python3 simple_web_server.py  # web interface")
    print()

def main():
    while True:
        print_header()
        print_options()
        
        try:
            choice = input("Enter your choice (1-5): ").strip()
            print()
            
            if choice == '1':
                start_web_interface()
            elif choice == '2':
                start_command_line()
            elif choice == '3':
                start_interactive()
            elif choice == '4':
                show_help()
                input("\nPress Enter to continue...")
                continue
            elif choice == '5':
                print("👋 Goodbye! Thank you for using the Learning Objectives Generator.")
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, 4, or 5.")
                input("Press Enter to continue...")
                continue
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thank you for using the Learning Objectives Generator.")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            input("Press Enter to continue...")
            continue
        
        # Ask if user wants to continue
        print()
        again = input("Would you like to use the tool again? (y/n): ").strip().lower()
        if again not in ['y', 'yes']:
            print("👋 Goodbye! Thank you for using the Learning Objectives Generator.")
            break

if __name__ == "__main__":
    main()