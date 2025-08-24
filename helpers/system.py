from pathlib import Path
from datetime import datetime
from subprocess import getoutput
from os import system, name
from platform import release, machine, python_version

class OSHelper:
    @staticmethod
    def make_dir(path):
        Path(path).mkdir(parents=True, exist_ok=True)
        return Path(path)

    @staticmethod
    def write_file(path, content, override=False, encoding="utf-8"):
        p = Path(path)
        OSHelper.make_dir(p.parent)
        lines = []
        if p.exists():
            with open(p, "r", encoding=encoding) as f:
                lines = f.read().splitlines()
        if override:
            if lines:
                lines[0] = content
            else:
                lines.append(content)
        else:
            lines.append(content)
        with open(p, "w", encoding=encoding) as f:
            f.write("\n".join(lines) + "\n")

    @staticmethod
    def read_file(path, encoding="utf-8"):
        p = Path(path)
        if not p.exists():
            return ""
        with open(p, "r", encoding=encoding) as f:
            return "\n".join(f.read().splitlines())

    @staticmethod
    def file_exists(path):
        return Path(path).exists()

    @staticmethod
    def delete_file(path):
        p = Path(path)
        if p.exists():
            p.unlink()

    @staticmethod
    def list_dir(path):
        p = Path(path)
        return list(p.iterdir()) if p.exists() else []

    @staticmethod
    def get_timestamp(fmt="%Y-%m-%d %H:%M:%S"):
        return datetime.now().strftime(fmt)

    @staticmethod
    def cmd(command):
        system(command)

    @staticmethod
    def cls():
        system("cls")

    @staticmethod
    def ping(host="127.0.0.1", count=1):
        system(f"ping {host} -n {count}" if name == "nt" else f"ping -c {count} {host}")

    @staticmethod
    def whoami():
        system("whoami")

    @staticmethod
    def list_processes():
        system("tasklist" if name == "nt" else "ps aux")

class HWID:
    @staticmethod
    def get_hwid():
        return getoutput("wmic baseboard get serialnumber").split("\n")[1].strip()
