# Scorpion CLI v1.0.0

A Python-based command-line interface with advanced terminal features and system utilities.

## Features

- **System Navigation**: Quick access to GitHub, portfolio, and system information
- **File Operations**: Directory management, file reading/writing capabilities
- **System Information**: Network configuration, user details, and system stats
- **Utilities**: PowerShell command execution, encryption/decryption, and timers
- **Enhanced UI**: Colorful output with progress indicators and styled banners

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/rescore09/scorpion-cli
   cd scorpion-cli
   ```

2. Install required dependencies:
   ```bash
   pip install cryptography win10toast
   ```

3. Run the CLI:
   ```bash
   python main.py
   ```

## Commands

### System Navigation
- `github` - Opens the developer's GitHub page
- `portfolio` - Opens the developer's portfolio
- `credits` - Shows developer and build information
- `logs` - Displays the contents of main.log
- `cls / clear` - Clears the console screen
- `winfetch / neofetch` - Displays system information
- `exit` - Exits the CLI

### File Operations
- `dir` - Lists files and directories in current folder
- `mkdir <folder>` - Creates a new folder with given name
- `rm <file/folder>` - Deletes a file or folder (use with caution)
- `read <file>` - Displays the contents of a file
- `write <file> <content>` - Writes content to a file (appends if exists)

### System Information
- `hostname` - Displays the system hostname
- `whoami` - Shows the current user
- `ipconfig` - Displays network adapter information
- `date` - Displays current date and time

### Utilities
- `execute <powershell-command>` - Executes a PowerShell command
- `echo <text>` - Prints the provided text in console
- `timer <seconds>` - Waits for given seconds then notifies
- `encrypt <text>` - Encrypts string using HWID-based key
- `decrypt <encrypted-text>` - Decrypts previously encrypted string
- `help` - Displays the command reference

## Security Features

- **HWID-based Encryption**: Uses hardware ID for generating unique encryption keys
- **Secure File Operations**: Safe file handling with error checking
- **Command Logging**: All commands are logged to main.log for audit purposes

## Requirements

- Python 3.6+
- Windows OS (for HWID functionality and toast notifications)
- Dependencies:
  - `cryptography`
  - `win10toast`

## Usage Examples

```bash
# Display system information
winfetch

# Create a new folder
mkdir my_folder

# Read a file
read example.txt

# Encrypt sensitive text
encrypt "my secret message"

# Set a timer for 30 seconds
timer 30

# Execute PowerShell command
execute Get-Process
```

## Developer

- **Developer**: rescore
- **Contributions**: vision
- **Version**: 1.0.0
- **GitHub**: [rescore09](https://github.com/rescore09)
- **Portfolio**: [rescore9.vercel.app](https://rescore9.vercel.app)

## License

This project is for educational and personal use. Please use responsibly.

## Notes

This program was specifically made to use helper functions and is not intended as a serious production tool. It serves as a demonstration of terminal interface design and utility integration.
