import os, shutil
import hashlib
import base64

from helpers.print import Print
from helpers.winfetch import winfetch, ht
from helpers.utils import *
from helpers.logging import FileSystem
import subprocess
from webbrowser import open as wop
from helpers.system import OSHelper
from cryptography.fernet import Fernet
from datetime import datetime
from time import sleep
from win10toast import ToastNotifier

def hwid():
    return subprocess.check_output("wmic baseboard get serialnumber", shell=True).decode().splitlines()[1].strip()

toaster = ToastNotifier()
host = ht()
logger = FileSystem()
user = os.getlogin().lower()

def get_user_key():
    hwid_value = hwid()
    user_key = hashlib.sha256(hwid_value.encode()).digest()
    return base64.urlsafe_b64encode(user_key)

def enc(string: str) -> str:
    try:
        fernet = Fernet(get_user_key())
        encrypted = fernet.encrypt(string.encode()).decode()
        return encrypted
    except Exception as e:
        return f"[ERROR] {str(e)}"

def dec(encrypted_text: str) -> str:
    try:
        fernet = Fernet(get_user_key())
        decrypted = fernet.decrypt(encrypted_text.encode()).decode()
        return decrypted
    except Exception as e:
        return f"[ERROR] {str(e)}"

def eps(cmd_str: str) -> str:
    try:
        result = subprocess.run(
            ["powershell", "-Command", cmd_str],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"[ERROR] {e.stderr.strip()}"
    except Exception as e:
        return f"[ERROR] {str(e)}"

def logs():
    try:
        print_divider("LOG CONTENTS")
        with open("main.log", "r", encoding="utf-8") as f:
            for line in f:
                Print.prt(f"  {line.strip()}", "GREEN")
        print_divider()
    except FileNotFoundError:
        print_status("main.log not found", "ERROR")



                                                               
def print_banner():
    banner = """
            ╔═══════════════════════════════════════════════════════════════════════════════╗
            ║                            SCORPION CLI v1.0.0                                ║
            ║                                                                               ║
            ║     ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    ║
            ║     ░░                                                                  ░░    ║
            ║     ░░  ███████╗ ██████╗ ██████╗ ██████╗ ██████╗ ██╗ ██████╗ ███╗   ██╗ ░░    ║
            ║     ░░  ██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗██║██╔═══██╗████╗  ██║ ░░    ║
            ║     ░░  ███████╗██║     ██║   ██║██████╔╝██████╔╝██║██║   ██║██╔██╗ ██║ ░░    ║
            ║     ░░  ╚════██║██║     ██║   ██║██╔══██╗██╔═══╝ ██║██║   ██║██║╚██╗██║ ░░    ║
            ║     ░░  ███████║╚██████╗╚██████╔╝██║  ██║██║     ██║╚██████╔╝██║ ╚████║ ░░    ║
            ║     ░░  ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ░░    ║
            ║     ░░                                                                  ░░    ║
            ║     ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    ║
            ║                                                                               ║
            ║                       Advanced Terminal Interface System                      ║
            ╚═══════════════════════════════════════════════════════════════════════════════╝
    """
    for line in banner.split('\n')[1:-1]:
        Print.prt(line, "GREEN")

def print_divider(text="", char="─", width=40):
    if text:
        Print.prt(f"─── {text} {'─' * max(0, width - len(text) - 5)}", "YELLOW")
    else:
        Print.prt("─" * 40, "YELLOW")

def print_status(text, status="INFO"):
    symbols = {
        "INFO": "ℹ",
        "SUCCESS": "✓",
        "ERROR": "✗",
        "WARNING": "⚠",
        "LOADING": "◐"
    }
    colors = {
        "INFO": "BLUE",
        "SUCCESS": "GREEN", 
        "ERROR": "RED",
        "WARNING": "YELLOW",
        "LOADING": "CYAN"
    }
    Print.prt(f"[{symbols.get(status, '•')}] {text}", colors.get(status, "WHITE"))

COMMANDS = {
    "System Navigation": {
        "github": "Opens the Rescore's GitHub page",
        "portfolio": "Opens Rescore's Portfolio",
        "credits": "Shows developer and build information", 
        "logs": "Displays the contents of main.log",
        "cls / clear": "Clears the console screen",
        "winfetch / neofetch": "Displays system information",
        "exit": "Exits the CLI"
    },
    "File Operations": {
        "dir": "Lists files and directories in current folder",
        "mkdir <folder>": "Creates a new folder with given name", 
        "rm <file/folder>": "Deletes a file or folder (use with caution)",
        "read <file>": "Displays the contents of a file",
        "write <file> <content>": "Writes content to a file (appends if exists)"
    },
    "System Information": {
        "hostname": "Displays the system hostname",
        "whoami": "Shows the current user",
        "ipconfig": "Displays network adapter information", 
        "date": "Displays current date and time"
    },
    "Utilities": {
        "execute <powershell-command>": "Executes a PowerShell command",
        "echo <text>": "Prints the provided text in console",
        "timer <seconds>": "Waits for given seconds then notifies",
        "encrypt <text>": "Encrypts string using HWID-based key",
        "decrypt <encrypted-text>": "Decrypts previously encrypted string",
        "help": "Displays this command reference"
    }
}

def show_help():
    print_divider("COMMANDS")
    for category, commands in COMMANDS.items():
        Print.prt(f"\n{category}:", "CYAN")
        for cmd, desc in commands.items():
            Print.prt(f"  {cmd:<28} {desc}", "GREEN")
    print()

def show_welcome():
    print_banner()
    Print.prt(f"\nSession: {user}@{host} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "CYAN")
    Print.prt(f"This program was specifically made to use some of the helpers and in no ways is a serious program.", "CYAN")
    Print.prt("Type 'help' for available commands\n", "YELLOW")

def animate_loading(text, duration=0.5):
    chars = "◐◓◑◒"
    for _ in range(int(duration * 10)):
        for char in chars:
            print(f"\r[{char}] {text}", end="", flush=True)
            sleep(0.05)
    print(f"\r[✓] {text}")

def main():
    OSHelper.cls()
    show_welcome()
    
    while True:
        try:
            prompt = f"\n┌─[{user}@{host}]─[~]\n└─$ "
            command = input(prompt).strip()
            
            if not command:
                continue
                
            logger.save(command + "\n")
            
            print_divider()
            
            if " " in command:
                cmd_base, cmd_args = command.split(" ", 1)
            else:
                cmd_base, cmd_args = command, ""
            cmd_lower = cmd_base.lower()

            if cmd_lower == "github":
                animate_loading("Opening GitHub repository")
                wop("https://github.com/rescore09")
                print_status("GitHub page opened successfully", "SUCCESS")

            if cmd_lower == "portfolio":
                animate_loading("Opening GitHub repository")
                wop("https://rescore9.vercel.app")
                print_status("Portfolio page opened successfully", "SUCCESS")

            elif cmd_lower == "credits":
                print_divider("CREDITS")
                Print.prt("Developer: rescore", "GREEN")
                Print.prt("Contributions: vision", "GREEN")
                Print.prt("Version: 1.0.0", "GREEN")
                Print.prt(f"Build: {datetime.now().strftime('%m/%d/%Y %I:%M %p')}", "GREEN")
                Print.prt("Compiler: PyInstaller", "GREEN")

            elif cmd_lower == "logs":
                logs()

            elif cmd_lower in ("cls", "clear"):
                OSHelper.cls()
                show_welcome()

            elif cmd_lower in ("winfetch", "neofetch"):
                print_divider("SYSTEM INFO")
                winfetch()
                print_divider()

            elif cmd_lower == "exit":
                print_divider("GOODBYE")
                Print.prt("Shutting down Scorpion CLI...", "YELLOW")
                Print.prt("Thank you for using Scorpion!", "GREEN")
                sleep(1)
                break

            elif cmd_lower == "help":
                show_help()

            elif cmd_lower == "execute":
                if not cmd_args:
                    print_status("No PowerShell command provided", "ERROR")
                else:
                    print_status(f"Executing: {cmd_args}", "LOADING")
                    output = eps(cmd_args)
                    if "[ERROR]" not in output:
                        print_divider("OUTPUT")
                        for line in output.split('\n'):
                            if line.strip():
                                Print.prt(f"  {line}", "GREEN")
                        print_status("Command executed successfully", "SUCCESS")
                    else:
                        print_status(output, "ERROR")

            elif cmd_lower == "dir":
                print_divider("DIRECTORY")
                files = os.listdir()
                if files:
                    for i, f in enumerate(files, 1):
                        icon = "📁" if os.path.isdir(f) else "📄"
                        Print.prt(f"  {i:2d}. {icon} {f}", "GREEN")
                    print_status(f"Total: {len(files)} items", "INFO")
                else:
                    print_status("Directory is empty", "INFO")

            elif cmd_lower == "mkdir":
                if not cmd_args:
                    print_status("No folder name provided", "ERROR")
                else:
                    try:
                        os.makedirs(cmd_args, exist_ok=True)
                        print_status(f"Folder '{cmd_args}' created successfully", "SUCCESS")
                    except Exception as e:
                        print_status(f"Failed to create folder: {str(e)}", "ERROR")

            elif cmd_lower == "rm":
                if not cmd_args:
                    print_status("No file or folder specified", "ERROR")
                else:
                    try:
                        if os.path.isdir(cmd_args):
                            shutil.rmtree(cmd_args)
                            print_status(f"Folder '{cmd_args}' deleted successfully", "SUCCESS")
                        else:
                            os.remove(cmd_args)
                            print_status(f"File '{cmd_args}' deleted successfully", "SUCCESS")
                    except Exception as e:
                        print_status(f"Deletion failed: {str(e)}", "ERROR")

            elif cmd_lower == "read":
                if not cmd_args:
                    print_status("No file specified", "ERROR")
                else:
                    try:
                        print_divider(f"READING: {cmd_args}")
                        with open(cmd_args, "r", encoding="utf-8") as f:
                            lines = f.readlines()
                            for i, line in enumerate(lines, 1):
                                Print.prt(f"  {i:3d} │ {line.rstrip()}", "GREEN")
                            print_status(f"{len(lines)} lines total", "INFO")
                    except Exception as e:
                        print_status(f"Failed to read file: {str(e)}", "ERROR")

            elif cmd_lower == "write":
                parts = cmd_args.split(" ", 1)
                if len(parts) < 2:
                    print_status("Usage: write <file> <content>", "ERROR")
                else:
                    filename, content = parts
                    try:
                        with open(filename, "a", encoding="utf-8") as f:
                            f.write(content + "\n")
                        print_status(f"Content written to '{filename}'", "SUCCESS")
                    except Exception as e:
                        print_status(f"Write failed: {str(e)}", "ERROR")

            elif cmd_lower == "hostname":
                Print.prt(f"Hostname: {host}", "GREEN")

            elif cmd_lower == "whoami":
                Print.prt(f"Current user: {user}", "GREEN")

            elif cmd_lower == "ipconfig":
                print_status("Retrieving network configuration", "LOADING")
                output = eps("ipconfig")
                if "[ERROR]" not in output:
                    print_divider("NETWORK CONFIG")
                    for line in output.split('\n'):
                        if line.strip():
                            Print.prt(f"  {line}", "GREEN")
                    print_divider()
                else:
                    print_status(output, "ERROR")

            elif cmd_lower == "date":
                current_time = datetime.now()
                Print.prt(f"Date: {current_time.strftime('%Y-%m-%d')}", "GREEN")
                Print.prt(f"Time: {current_time.strftime('%H:%M:%S')}", "GREEN")
                Print.prt(f"Full: {current_time.strftime('%A, %B %d, %Y at %I:%M %p')}", "GREEN")

            elif cmd_lower == "echo":
                Print.prt(f"Echo: {cmd_args if cmd_args else ''}", "GREEN")

            elif cmd_lower == "timer":
                if cmd_args.isdigit():
                    seconds = int(cmd_args)
                    print_status(f"Timer set for {seconds} seconds", "INFO")
                    
                    for remaining in range(seconds, 0, -1):
                        print(f"\r[◐] Time remaining: {remaining:02d}s", end="", flush=True)
                        sleep(1)
                    
                    print(f"\r[✓] Timer completed!                    ")
                    toaster.show_toast("Scorpion Timer", f"{seconds} seconds elapsed!", duration=5, threaded=True)
                    print_status("Timer notification sent", "SUCCESS")
                else:
                    print_status("Usage: timer <seconds>", "ERROR")

            elif cmd_lower == "encrypt":
                if not cmd_args:
                    print_status("Usage: encrypt <text>", "ERROR")
                else:
                    print_status("Encrypting data with HWID key", "LOADING")
                    result = enc(cmd_args)
                    if "[ERROR]" not in result:
                        print_divider("ENCRYPTED")
                        Print.prt(f"  {result}", "GREEN")
                        print_status("Encryption successful", "SUCCESS")
                    else:
                        print_status(result, "ERROR")
            
            elif cmd_lower == "decrypt":
                if not cmd_args:
                    print_status("Usage: decrypt <encrypted-text>", "ERROR")
                else:
                    print_status("Decrypting data with HWID key", "LOADING")
                    result = dec(cmd_args)
                    if "[ERROR]" not in result:
                        print_divider("DECRYPTED")
                        Print.prt(f"  {result}", "GREEN")
                        print_status("Decryption successful", "SUCCESS")
                    else:
                        print_status(result, "ERROR")

            else:
                print_status(f"Command '{command}' not recognized", "ERROR")
                Print.prt("Type 'help' to see available commands", "YELLOW")

        except KeyboardInterrupt:
            print("\n")
            print_divider("INTERRUPT")
            Print.prt("Keyboard interrupt detected", "YELLOW")
            Print.prt("Exiting Scorpion CLI...", "YELLOW")
            break

if __name__ == "__main__":
    main()