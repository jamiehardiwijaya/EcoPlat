# main.py
import sys
import os
from utils.helper import Utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# from views.auth_view import show_auth_menu
from views.dashboard_view import show_dashboard

def main():
    Utils.print_header("Food Waste Manager")
    
    # while True:
    #     show_auth_menu()
    show_dashboard()

if __name__ == "__main__":
    main()