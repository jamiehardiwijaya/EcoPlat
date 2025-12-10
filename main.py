# main.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from views.auth_view import show_auth_menu

def main():
    print("=" * 40)
    print("    Ecoplat - Your Eco-Friendly Platform    ")
    print("=" * 40)
    
    while True:
        show_auth_menu()

if __name__ == "__main__":
    main()