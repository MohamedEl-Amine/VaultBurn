# VaultBurn

VaultBurn is a secure file deletion application designed to permanently destroy files and directories by overwriting their data multiple times before deletion. It ensures that sensitive data cannot be recovered using data recovery tools.

## Features

- Secure deletion of files with multiple overwrite passes
- Graphical user interface for easy file selection
- Support for adding individual files or entire directories recursively
- Confirmation dialogs to prevent accidental deletion
- Cross-platform compatibility (Windows, macOS, Linux)

## Installation

1. Ensure you have Python 3.8 or higher installed.
2. Clone the repository: `git clone https://github.com/MohamedEl-Amine/VaultBurn.git`
3. Navigate to the project directory: `cd vaultburn`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the application: `python main.py`

## Usage

### Graphical Interface
1. Launch the application using `python main.py`.
2. Use "Add Files" to select individual files for deletion.
3. Use "Add Directory" to select a directory and add all files within it recursively.
4. Select files from the list and use "Secure Delete Selected" or "Secure Delete All" to permanently destroy them.
5. Confirm the deletion in the dialog box.

### Command Line Interface
VaultBurn also supports command-line usage for scripting and automation:

```bash
python main.py file1.txt file2.txt --passes 5
python main.py /path/to/directory --recursive --passes 3
```

Options:
- `files`: One or more files or directories to delete
- `--passes`: Number of overwrite passes (default: 3)
- `--recursive`: Recursively delete directories and their contents

**Warning:** Deleted files cannot be recovered. Use with caution.

## Security

VaultBurn overwrites file data 3 times with random bytes before deletion, making recovery extremely difficult. However, for highly sensitive data, consider using specialized hardware destruction methods.

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -m 'Add new feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## Disclaimer

This software is provided "as is" without warranty of any kind. The developers are not responsible for any misuse of this application, including but not limited to accidental data loss. Users are solely responsible for ensuring their use complies with applicable laws and regulations.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.