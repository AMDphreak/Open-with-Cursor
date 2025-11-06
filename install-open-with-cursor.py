import winreg
import os
import sys
import locale

def add_cursor_menu(key_path, cursor_path):
    try:
        # Use HKEY_CURRENT_USER\Software\Classes instead of HKEY_CLASSES_ROOT
        # This allows user-specific installation without admin privileges
        full_path = f"Software\\Classes\\{key_path}"
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, full_path)
        cursor_key = winreg.CreateKey(key, "Cursor")
        
        # Detect system default language
        system_language = locale.getdefaultlocale()[0]
        menu_text = "通过 Cursor 打开" if system_language.startswith("zh_") else "Open with Cursor"
        
        winreg.SetValue(cursor_key, "", winreg.REG_SZ, menu_text)
        winreg.SetValueEx(cursor_key, "Icon", 0, winreg.REG_SZ, cursor_path)
        
        command_key = winreg.CreateKey(cursor_key, "command")
        winreg.SetValue(command_key, "", winreg.REG_SZ, f'"{cursor_path}" "%V"')
        
        print(f"Successfully added Cursor menu to HKEY_CURRENT_USER\\Software\\Classes\\{key_path}")
    except WindowsError as e:
        print(f"Error adding Cursor menu to {key_path}: {e}")

def main():
    # Get the path to Cursor.exe
    cursor_path = os.path.expandvars(r"%LOCALAPPDATA%\Programs\Cursor\Cursor.exe")
    
    if not os.path.exists(cursor_path):
        print("Cursor.exe not found. Please ensure Cursor editor is properly installed.")
        return

    # Add right-click menu for files
    add_cursor_menu(r"*\shell", cursor_path)

    # Add right-click menu for folders
    add_cursor_menu(r"Directory\shell", cursor_path)

    # Add right-click menu for folder background
    add_cursor_menu(r"Directory\Background\shell", cursor_path)

    print("Operation completed. Please restart File Explorer or log out and log back in to Windows for changes to take effect.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()