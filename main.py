import sys
import urllib.parse
import os
import subprocess
import glob
import winreg
from pathlib import Path

def find_phpstorm_executable():
    """Tìm phpstorm64.exe từ nhiều nguồn khác nhau"""
    
    # 1. Kiểm tra biến môi trường PATH
    try:
        result = subprocess.run(['where', 'phpstorm64.exe'], 
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            path = result.stdout.strip().split('\n')[0]
            if os.path.exists(path):
                print(f"Tìm thấy PhpStorm trong PATH: {path}")
                return path
    except:
        pass
    
    # 2. Kiểm tra trong Program Files
    program_files_paths = [
        os.environ.get('PROGRAMFILES', r'C:\Program Files'),
        os.environ.get('PROGRAMFILES(X86)', r'C:\Program Files (x86)')
    ]
    
    for program_files in program_files_paths:
        jetbrains_path = os.path.join(program_files, 'JetBrains')
        if os.path.exists(jetbrains_path):
            # Tìm tất cả thư mục PhpStorm
            phpstorm_dirs = glob.glob(os.path.join(jetbrains_path, 'PhpStorm*'))
            for phpstorm_dir in sorted(phpstorm_dirs, reverse=True):  # Sắp xếp để lấy phiên bản mới nhất
                executable = os.path.join(phpstorm_dir, 'bin', 'phpstorm64.exe')
                if os.path.exists(executable):
                    print(f"Tìm thấy PhpStorm trong Program Files: {executable}")
                    return executable
    
    # 3. Kiểm tra trong AppData (cho Toolbox Apps)
    appdata = os.environ.get('LOCALAPPDATA', '')
    if appdata:
        toolbox_paths = [
            os.path.join(appdata, 'JetBrains', 'Toolbox', 'apps', 'PhpStorm', 'ch-0', '*', 'bin', 'phpstorm64.exe'),
            os.path.join(appdata, 'Programs', 'PhpStorm*', 'bin', 'phpstorm64.exe')
        ]
        
        for pattern in toolbox_paths:
            matches = glob.glob(pattern)
            if matches:
                # Lấy phiên bản mới nhất
                latest = max(matches, key=os.path.getctime)
                print(f"Tìm thấy PhpStorm trong AppData: {latest}")
                return latest
    
    # 4. Kiểm tra biến môi trường PhpStorm
    phpstorm_env = os.environ.get('PHPSTORM_PATH')
    if phpstorm_env and os.path.exists(phpstorm_env):
        print(f"Tìm thấy PhpStorm từ biến môi trường PHPSTORM_PATH: {phpstorm_env}")
        return phpstorm_env
    
    return None

def open_in_phpstorm(url):
    # Tự động tìm đường dẫn PhpStorm
    phpstorm_path = find_phpstorm_executable()
    
    if not phpstorm_path:
        print("Không tìm thấy phpstorm64.exe!")
        print("Hãy đảm bảo PhpStorm đã được cài đặt hoặc thêm vào PATH")
        return
    
    # Tạo lệnh mở tệp trong PhpStorm
    command = f'"{phpstorm_path}" "{url}"'
    
    # Thực thi lệnh
    try:
        subprocess.run(command, shell=True)
        print(f"Đã mở URL trong PhpStorm: {url}")
    except Exception as e:
        print(f"Lỗi khi mở PhpStorm: {e}")

def check_registry_configuration():
    """Kiểm tra cấu hình registry hiện tại"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"phpstorm\shell\open\command")
        current_command, _ = winreg.QueryValueEx(key, "")
        winreg.CloseKey(key)
        print(f"Cấu hình registry hiện tại: {current_command}")
        return current_command
    except FileNotFoundError:
        print("Không tìm thấy registry key cho phpstorm protocol")
        return None
    except Exception as e:
        print(f"Lỗi khi đọc registry: {e}")
        return None

def update_registry_configuration(phpstorm_path):
    """Cập nhật cấu hình registry với đường dẫn PhpStorm đúng"""
    try:
        # Tạo hoặc mở key
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"phpstorm")
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "URL:PhpStorm Protocol")
        winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, "")
        winreg.CloseKey(key)
        
        # Tạo shell key
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"phpstorm\shell")
        winreg.CloseKey(key)
        
        # Tạo open key
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"phpstorm\shell\open")
        winreg.CloseKey(key)
        
        # Cập nhật command key
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"phpstorm\shell\open\command")
        command_value = f'"{phpstorm_path}" "%1"'
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, command_value)
        winreg.CloseKey(key)
        
        print(f"✅ Đã cập nhật registry thành công: {command_value}")
        return True
    except Exception as e:
        print(f"❌ Lỗi khi cập nhật registry: {e}")
        print("Hãy chạy script với quyền Administrator")
        return False

def verify_and_update_registry():
    """Kiểm tra và cập nhật registry nếu cần"""
    print("🔍 Đang kiểm tra cấu hình registry...")
    
    # Tìm PhpStorm
    phpstorm_path = find_phpstorm_executable()
    if not phpstorm_path:
        print("❌ Không tìm thấy PhpStorm, không thể cập nhật registry")
        return False
    
    # Kiểm tra registry hiện tại
    current_command = check_registry_configuration()
    expected_command = f'"{phpstorm_path}" "%1"'
    
    print(f"\n📋 So sánh cấu hình:")
    print(f"Hiện tại: {current_command}")
    print(f"Mong muốn: {expected_command}")
    
    if current_command == expected_command:
        print("✅ Registry đã được cấu hình đúng!")
        return True
    else:
        print("\n⚠️  Registry cần được cập nhật")
        response = input("Bạn có muốn cập nhật registry không? (y/N): ")
        if response.lower() in ['y', 'yes']:
            return update_registry_configuration(phpstorm_path)
        else:
            print("Bỏ qua việc cập nhật registry")
            return False

def generate_registry_file():
    """Tạo file .reg với cấu hình đúng"""
    phpstorm_path = find_phpstorm_executable()
    if not phpstorm_path:
        print("❌ Không tìm thấy PhpStorm")
        return
    
    # Escape backslashes cho file .reg
    escaped_path = phpstorm_path.replace('\\', '\\\\')
    
    reg_content = f'''Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\\phpstorm]
@="URL:PhpStorm Protocol"
"URL Protocol"="")

[HKEY_CLASSES_ROOT\\phpstorm\\shell]

[HKEY_CLASSES_ROOT\\phpstorm\\shell\\open]

[HKEY_CLASSES_ROOT\\phpstorm\\shell\\open\\command]
@="\\"{escaped_path}\\" \\"%1\\""
'''
    
    reg_file_path = os.path.join(os.path.dirname(__file__), "setupReg-auto.reg")
    with open(reg_file_path, 'w', encoding='utf-8') as f:
        f.write(reg_content)
    
    print(f"✅ Đã tạo file registry: {reg_file_path}")
    print(f"📝 Nội dung file:")
    print(reg_content)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--check-registry":
            verify_and_update_registry()
        elif command == "--generate-reg":
            generate_registry_file()
        elif command.startswith("phpstorm://"):
            open_in_phpstorm(command)
        else:
            # Assume it's a URL
            open_in_phpstorm(command)
    else:
        print("📖 Cách sử dụng:")
        print("  python main.py 'phpstorm://open?file=...'  - Mở URL trong PhpStorm")
        print("  python main.py --check-registry           - Kiểm tra và cập nhật registry")
        print("  python main.py --generate-reg             - Tạo file .reg tự động")