# VaultBurn 🔒🔥

VaultBurn is a comprehensive secure file management application that combines **secure file deletion** with **military-grade encryption/decryption** capabilities. Built with PyQt5, it provides a modern, user-friendly interface for permanently destroying sensitive data and protecting files with AES-256 encryption.

## ✨ Features

### 🗂️ Secure File Deletion
- **3-Pass Overwrite**: Military-standard secure deletion with random data overwrites
- **Batch Processing**: Delete multiple files or entire directories recursively
- **Progress Tracking**: Real-time progress bars for long operations
- **Drag & Drop Support**: Simply drag files/folders into the application
- **Confirmation Dialogs**: Prevents accidental deletions with clear warnings

### 🔐 File Encryption & Decryption
- **AES-256 Encryption**: Industry-standard Fernet encryption (AES-128 in CBC mode)
- **Secure Key Generation**: Automatic generation of cryptographically secure keys
- **Key Validation**: Built-in validation to prevent invalid key usage
- **One-Click Operations**: Simple encrypt/decrypt with progress feedback
- **Key Management**: Copy encryption keys to clipboard for secure sharing

### 🎨 Modern User Interface
- **Tabbed Interface**: Organized sections for deletion, encryption, and logs
- **Dark Theme**: Professional dark UI with custom styling
- **Responsive Design**: Adapts to different screen sizes
- **Real-time Feedback**: Status updates and progress indicators
- **Cross-platform**: Works on Windows, macOS, and Linux

### 🛡️ Security & Validation
- **Input Validation**: Comprehensive checks for file existence, permissions, and key formats
- **Error Handling**: Graceful error messages with detailed feedback
- **Threading**: Background processing prevents UI freezing during operations
- **Logging**: Complete operation logs for audit trails

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- PyQt5 (automatically installed via requirements.txt)

### Quick Start
```bash
# Clone the repository
git clone https://github.com/MohamedEl-Amine/VaultBurn.git
cd VaultBurn

# Create virtual environment (recommended)
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## 📖 Usage

### Graphical Interface

#### File Deletion Tab
1. **Add Files**: Click "Add Files" or "Add Directory" to select files/folders
2. **Drag & Drop**: Drag files/folders directly into the application window
3. **Select & Delete**: Choose files from the list and click "Secure Delete Selected"
4. **Batch Delete**: Use "Secure Delete All" for complete list deletion
5. **Monitor Progress**: Watch real-time progress during deletion operations

#### Encryption Tab
1. **Select File**: Click "Select File to Encrypt" to choose a file
2. **Encrypt**: Click "Encrypt & Generate Key" to create encrypted version
3. **Copy Key**: Use "Copy Key to Clipboard" to securely share the encryption key
4. **⚠️ Important**: Keep the key safe - lost keys cannot be recovered!

#### Decryption Tab
1. **Select Encrypted File**: Choose the encrypted file
2. **Enter Key**: Paste the encryption key provided during encryption
3. **Decrypt**: Click "Decrypt File" to restore the original file
4. **Validation**: The app validates keys before attempting decryption

#### Logs Tab
- **Real-time Logs**: View all operations and their results
- **Refresh**: Click "Refresh Logs" to update the log display
- **Audit Trail**: Complete record of all file operations

### Command Line Interface
VaultBurn also supports command-line usage for scripting:

```bash
# Delete specific files with custom passes
python main.py file1.txt file2.txt --passes 5

# Delete directory recursively
python main.py /path/to/directory --recursive --passes 3
```

**Options:**
- `files`: Files or directories to delete
- `--passes`: Number of overwrite passes (default: 3)
- `--recursive`: Include subdirectories

## 🔒 Security Features

### Secure Deletion
- **3-Pass Overwrite**: Random data patterns ensure data irrecoverability
- **Complete Removal**: Files are physically deleted after overwriting
- **No Recovery**: Professional data recovery tools cannot restore overwritten data

### Encryption Security
- **AES-256 Equivalent**: Uses Fernet encryption (AES-128 CBC with HMAC)
- **Secure Keys**: 32-byte cryptographically secure random keys
- **Key Validation**: Prevents decryption attempts with invalid keys
- **Isolated Operations**: Encryption/decryption run in separate threads

## ⚠️ Important Warnings

- **Irreversible Operations**: Deleted files cannot be recovered
- **Key Management**: Lost encryption keys mean permanent data loss
- **Legal Compliance**: Ensure usage complies with local laws and regulations
- **Backup First**: Always backup important data before operations

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest

# Check code style
flake8 .
```

## 📋 Requirements

- **Python**: 3.8+
- **PyQt5**: For GUI components
- **cryptography**: For encryption operations
- **Operating System**: Windows 10+, macOS 10.12+, Ubuntu 18.04+

## 🐛 Troubleshooting

### Common Issues
- **Application won't start**: Ensure Python 3.8+ and all dependencies are installed
- **Permission errors**: Run as administrator or ensure file access permissions
- **UI not responding**: Operations run in background threads - wait for completion
- **Decryption fails**: Verify the exact key was copied (including all characters)

### Getting Help
- Check the **logs tab** for detailed error information
- Ensure **file paths** are accessible and files aren't locked by other applications
- Verify **encryption keys** are copied exactly (no extra spaces or characters)

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with **PyQt5** for the modern GUI
- Uses **cryptography** library for secure encryption
- Inspired by secure deletion best practices
- Community contributions and feedback

---

**⚠️ Disclaimer**: This software is provided "as is" without warranty. Users are responsible for their data and compliance with applicable laws. Always backup important files before deletion or encryption operations.