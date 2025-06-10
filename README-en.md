# PhpStorm Protocol Handler

A Python tool to handle `phpstorm://` URL protocol and automatically open files in PhpStorm IDE.

> 🇺🇸 **English Documentation** | 📖 **[Tài liệu tiếng Việt](README.md)**

## 🚀 Features

- ✅ **Auto-detect PhpStorm**: Search PhpStorm from multiple sources
- ✅ **Registry Checker**: Verify and update Windows Registry configuration
- ✅ **Registry File Generator**: Auto-generate `.reg` files with correct paths
- ✅ **Multi-location Support**: Program Files, AppData, Toolbox Apps, PATH
- ✅ **URL Protocol Handler**: Open files directly from `phpstorm://` URLs

## 📋 Requirements

- **Python 3.6+**
- **Windows OS**
- **PhpStorm IDE** installed

## 🛠️ Installation

1. **Clone or download project**:
   ```bash
   git clone https://github.com/yourusername/phpstorm-protocol.git
   cd phpstorm-protocol
   ```

2. **Check PhpStorm installation**:
   ```bash
   python main.py --check-registry
   ```

## 📖 Usage Guide

### 1. Check Registry Configuration

```bash
python main.py --check-registry
```

**Output**:
- Shows current PhpStorm path
- Compares with Registry configuration
- Suggests updates if needed

### 2. Generate Registry File Automatically

```bash
python main.py --generate-reg
```

**Output**:
- Creates `setupReg-auto.reg` with correct PhpStorm path
- Ready to import to Windows Registry

### 3. Open Files via URL Protocol

```bash
python main.py "phpstorm://open?file=C:\path\to\file.php"
python main.py "phpstorm://open?file=C:\path\to\file.php&line=25"
```

### 4. Import Registry (run once)

**Method 1**: Using auto-generated file
```bash
# Generate registry file
python main.py --generate-reg

# Import file (requires Administrator privileges)
reg import setupReg-auto.reg
```

**Method 2**: Direct update via Python
```bash
# Run with Administrator privileges
python main.py --check-registry
# Choose 'y' when prompted for update
```

## 🔧 Advanced Configuration

### Environment Variables

You can set custom PhpStorm path:

```powershell
$env:PHPSTORM_PATH = "C:\custom\path\to\phpstorm64.exe"
```

### PhpStorm Search Order

1. **PATH Environment** - `where phpstorm64.exe`
2. **Program Files** - `C:\Program Files\JetBrains\PhpStorm*`
3. **Program Files (x86)** - `C:\Program Files (x86)\JetBrains\PhpStorm*`
4. **AppData Local** - JetBrains Toolbox Apps
5. **Custom Environment** - `PHPSTORM_PATH`

## 🌐 Using URL Protocol

After configuring Registry, you can:

### From web browser
```
phpstorm://open?file=C:\xampp\htdocs\project\index.php&line=10
```

### From other applications
```python
import webbrowser
webbrowser.open("phpstorm://open?file=C:\\project\\file.php")
```

### From HTML
```html
<a href="phpstorm://open?file=C:\project\file.php&line=25">
    Open in PhpStorm
</a>
```

## 📁 Project Structure

```
phpstorm-protocol/
├── main.py                 # Main script
├── setupReg.reg           # Manual registry file (optional)
├── setupReg-auto.reg      # Auto-generated registry file
├── README.md              # English documentation
├── README-vi.md           # Vietnamese documentation
└── LICENSE                # License file
```

## 🔍 Supported URL Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `file` | Path to file | `file=C:\project\index.php` |
| `line` | Line number (optional) | `line=25` |
| `column` | Column number (optional) | `column=10` |

**Full example**:
```
phpstorm://open?file=C:\xampp\htdocs\myproject\src\Controller.php&line=50&column=15
```

## 🐛 Troubleshooting

### PhpStorm not found

1. **Check installation**:
   ```bash
   where phpstorm64.exe
   ```

2. **Add to PATH** or set environment variable:
   ```powershell
   $env:PHPSTORM_PATH = "C:\path\to\phpstorm64.exe"
   ```

### Registry not working

1. **Check Administrator privileges**:
   - Run PowerShell/CMD as Administrator
   - Import `.reg` file or run Python script

2. **Check Registry manually**:
   ```
   regedit → HKEY_CLASSES_ROOT\phpstorm\shell\open\command
   ```

### URL doesn't open PhpStorm

1. **Test directly**:
   ```bash
   python main.py "phpstorm://open?file=C:\test.php"
   ```

2. **Check Registry**:
   ```bash
   python main.py --check-registry
   ```

## 📝 Real-world Examples

### Integration with Laravel Error Pages

```php
// In blade template or error handler
$file = str_replace('/', '\\', $exception->getFile());
$line = $exception->getLine();
$url = "phpstorm://open?file={$file}&line={$line}";

echo "<a href='{$url}'>Open in PhpStorm</a>";
```

### Integration with VS Code Extension

```javascript
// In VS Code extension
const uri = `phpstorm://open?file=${filePath}&line=${lineNumber}`;
vscode.env.openExternal(vscode.Uri.parse(uri));
```

### Chrome Extension

```javascript
// Content script for error pages
document.querySelectorAll('.error-file-path').forEach(element => {
    const filePath = element.textContent;
    const link = document.createElement('a');
    link.href = `phpstorm://open?file=${filePath}`;
    link.textContent = '📝 Open in PhpStorm';
    element.appendChild(link);
});
```

## 🚀 Quick Start

1. **One-command setup**:
   ```bash
   python main.py --check-registry
   ```

2. **Test the protocol**:
   ```bash
   python main.py "phpstorm://open?file=C:\Windows\System32\drivers\etc\hosts"
   ```

3. **Use in browser**: Paste this in address bar:
   ```
   phpstorm://open?file=C:\Windows\System32\drivers\etc\hosts
   ```

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

Developed to improve PhpStorm IDE workflow and productivity.

## 🙏 Acknowledgments

- JetBrains for PhpStorm IDE
- Python community for excellent libraries
- Contributors and testers

---

**💡 Pro Tip**: After installation, you can create browser bookmarklets to quickly open files from error pages or stack traces!

## 📚 Additional Resources

- [PhpStorm Documentation](https://www.jetbrains.com/help/phpstorm/)
- [Windows Registry Guide](https://docs.microsoft.com/en-us/windows/win32/sysinfo/registry)
- [URL Protocol Handler Reference](https://docs.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/platform-apis/aa767914(v=vs.85))

## 🔗 Related Projects

- [JetBrains Toolbox](https://www.jetbrains.com/toolbox-app/)
- [PhpStorm Plugins](https://plugins.jetbrains.com/phpstorm)
