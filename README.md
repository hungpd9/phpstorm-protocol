# PhpStorm Protocol Handler

Một công cụ Python để xử lý URL protocol `phpstorm://` và tự động mở file trong PhpStorm IDE.

> 📖 **[English Documentation](README-en.md)** | 🇻🇳 **Tài liệu tiếng Việt**

## 🚀 Tính năng

- ✅ **Tự động phát hiện PhpStorm**: Tìm kiếm PhpStorm từ nhiều nguồn khác nhau
- ✅ **Kiểm tra Registry**: Xác minh và cập nhật cấu hình Windows Registry
- ✅ **Tạo file Registry**: Tự động sinh file `.reg` với đường dẫn đúng
- ✅ **Hỗ trợ đa vị trí**: Program Files, AppData, Toolbox Apps, PATH
- ✅ **Xử lý URL Protocol**: Mở file trực tiếp từ URL `phpstorm://`

## 📋 Yêu cầu

- **Python 3.6+**
- **Windows OS**
- **PhpStorm IDE** đã được cài đặt

## 🛠️ Cài đặt

1. **Clone hoặc download project**:
   ```bash
   git clone <repository-url>
   cd phpstorm-protocal
   ```

2. **Kiểm tra PhpStorm đã được cài đặt**:
   ```bash
   python main.py --check-registry
   ```

## 📖 Hướng dẫn sử dụng

### 1. Kiểm tra cấu hình Registry

```bash
python main.py --check-registry
```

**Kết quả**:
- Hiển thị đường dẫn PhpStorm hiện tại
- So sánh với cấu hình Registry
- Đề xuất cập nhật nếu cần thiết

### 2. Tạo file Registry tự động

```bash
python main.py --generate-reg
```

**Kết quả**:
- Tạo file `setupReg-auto.reg` với đường dẫn PhpStorm đúng
- Sẵn sàng để import vào Windows Registry

### 3. Mở file qua URL Protocol

```bash
python main.py "phpstorm://open?file=C:\path\to\file.php"
python main.py "phpstorm://open?file=C:\path\to\file.php&line=25"
```

### 4. Import Registry (chạy một lần)

**Cách 1**: Sử dụng file tự động tạo
```bash
# Tạo file registry
python main.py --generate-reg

# Import file (cần quyền Administrator)
reg import setupReg-auto.reg
```

**Cách 2**: Cập nhật trực tiếp qua Python
```bash
# Chạy với quyền Administrator
python main.py --check-registry
# Chọn 'y' khi được hỏi cập nhật
```

## 🔧 Cấu hình nâng cao

### Biến môi trường

Bạn có thể đặt đường dẫn PhpStorm tùy chỉnh:

```powershell
$env:PHPSTORM_PATH = "C:\custom\path\to\phpstorm64.exe"
```

### Thứ tự tìm kiếm PhpStorm

1. **PATH Environment** - `where phpstorm64.exe`
2. **Program Files** - `C:\Program Files\JetBrains\PhpStorm*`
3. **Program Files (x86)** - `C:\Program Files (x86)\JetBrains\PhpStorm*`
4. **AppData Local** - JetBrains Toolbox Apps
5. **Custom Environment** - `PHPSTORM_PATH`

## 🌐 Cách sử dụng URL Protocol

Sau khi cấu hình Registry, bạn có thể:

### Từ trình duyệt web
```
phpstorm://open?file=C:\xampp\htdocs\project\index.php&line=10
```

### Từ ứng dụng khác
```python
import webbrowser
webbrowser.open("phpstorm://open?file=C:\\project\\file.php")
```

### Từ HTML
```html
<a href="phpstorm://open?file=C:\project\file.php&line=25">
    Mở trong PhpStorm
</a>
```

## 📁 Cấu trúc project

```
phpstorm-protocal/
├── main.py                 # Script chính
├── setupReg.reg           # File registry thủ công (tùy chọn)
├── setupReg-auto.reg      # File registry tự động tạo
└── README.md              # Tài liệu này
```

## 🔍 Các tham số URL được hỗ trợ

| Tham số | Mô tả | Ví dụ |
|---------|-------|-------|
| `file` | Đường dẫn đến file | `file=C:\project\index.php` |
| `line` | Số dòng (tùy chọn) | `line=25` |
| `column` | Số cột (tùy chọn) | `column=10` |

**Ví dụ đầy đủ**:
```
phpstorm://open?file=C:\xampp\htdocs\myproject\src\Controller.php&line=50&column=15
```

## 🐛 Xử lý sự cố

### PhpStorm không được tìm thấy

1. **Kiểm tra cài đặt**:
   ```bash
   where phpstorm64.exe
   ```

2. **Thêm vào PATH** hoặc đặt biến môi trường:
   ```powershell
   $env:PHPSTORM_PATH = "C:\path\to\phpstorm64.exe"
   ```

### Registry không hoạt động

1. **Kiểm tra quyền Administrator**:
   - Chạy PowerShell/CMD với quyền Administrator
   - Import file `.reg` hoặc chạy script Python

2. **Kiểm tra Registry thủ công**:
   ```
   regedit → HKEY_CLASSES_ROOT\phpstorm\shell\open\command
   ```

### URL không mở PhpStorm

1. **Test trực tiếp**:
   ```bash
   python main.py "phpstorm://open?file=C:\test.php"
   ```

2. **Kiểm tra Registry**:
   ```bash
   python main.py --check-registry
   ```

## 📝 Ví dụ thực tế

### Tích hợp với Laravel Error Pages

```php
// Trong blade template hoặc error handler
$file = str_replace('/', '\\', $exception->getFile());
$line = $exception->getLine();
$url = "phpstorm://open?file={$file}&line={$line}";

echo "<a href='{$url}'>Mở trong PhpStorm</a>";
```

### Tích hợp với VS Code Extension

```javascript
// Trong VS Code extension
const uri = `phpstorm://open?file=${filePath}&line=${lineNumber}`;
vscode.env.openExternal(vscode.Uri.parse(uri));
```

## 🤝 Đóng góp

1. Fork project
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## 📄 License

MIT License - xem file LICENSE để biết thêm chi tiết.

## 👨‍💻 Tác giả

Được phát triển để cải thiện workflow làm việc với PhpStorm IDE.

---

**💡 Tip**: Sau khi cài đặt, bạn có thể tạo bookmarklet trong trình duyệt để nhanh chóng mở file từ các error pages hoặc stack traces!
