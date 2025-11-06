import winreg
import sys

def remove_cursor_menu(key_path):
    try:
        # Use HKEY_CURRENT_USER\Software\Classes instead of HKEY_CLASSES_ROOT
        # This allows user-specific uninstallation without admin privileges
        full_path = f"Software\\Classes\\{key_path}"
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, f"{full_path}\\Cursor\\command")
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, f"{full_path}\\Cursor")
        print(f"Successfully removed Cursor menu from HKEY_CURRENT_USER\\Software\\Classes\\{key_path}")
    except WindowsError as e:
        print(f"Error removing Cursor menu from {key_path}: {e}")

def main():
    # Remove right-click menu for files
    remove_cursor_menu(r"*\shell")

    # Remove right-click menu for folders
    remove_cursor_menu(r"Directory\shell")

    # Remove right-click menu for folder background
    remove_cursor_menu(r"Directory\Background\shell")

    print("Uninstallation completed. Please restart File Explorer or log out and log back in to Windows for changes to take effect.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
