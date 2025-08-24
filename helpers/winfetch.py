import os
import platform
import psutil
import winreg
import ctypes
import subprocess
from datetime import datetime

RESET = "\033[0m"
BLUE = "\033[94m"
YELLOW = "\033[93m"

BLOCK = "l" * 15

def ht():
    return platform.node()

def user_host():
    return f"{os.getlogin().upper()}@{platform.node().upper()}"

def os_info():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
        )
        product_name = winreg.QueryValueEx(key, "ProductName")[0]
        release_id = winreg.QueryValueEx(key, "ReleaseId")[0] if "ReleaseId" in [winreg.EnumValue(key, i)[0] for i in range(winreg.QueryInfoKey(key)[1])] else ""
        ubr = winreg.QueryValueEx(key, "UBR")[0]  # build number patch
        arch = "64-bit" if "PROGRAMFILES(X86)" in dict(os.environ) else "32-bit"
        return f"{product_name} {release_id} (Build {ubr}) [{arch}]"
    except Exception:
        return "Unknown OS"

def kernel():
    return platform.version()


def board():
    try:
        class GUID(ctypes.Structure):
            _fields_ = [
                ("Data1", ctypes.c_uint32),
                ("Data2", ctypes.c_uint16),
                ("Data3", ctypes.c_uint16),
                ("Data4", ctypes.c_uint8 * 8),
            ]
        
        kernel32 = ctypes.windll.kernel32
        return "Unknown Baseboard via ctypes"
    except:
        return "Unknown"

def uptime():
    t = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
    h, rem = divmod(int(t.total_seconds()), 3600)
    m, _ = divmod(rem, 60)
    return f"{h} hours {m} minutes"

def packages():
    c = s = 0
    try:
        c = len(subprocess.check_output("choco list --local-only", shell=True).decode().splitlines())
    except: pass
    try:
        s = len(subprocess.check_output("scoop list", shell=True).decode().splitlines())
    except: pass
    return f"{c} (choco), {s} (scoop)"

def shell():
    try:
        out = subprocess.check_output("powershell -Command \"$PSVersionTable.PSVersion\"", shell=True).decode()
        version = out.splitlines()[2].strip()
        return f"PowerShell v{version}"
    except:
        return os.environ.get("COMSPEC", "cmd.exe")

def res():
    try:
        import screeninfo
        m = screeninfo.get_monitors()[0]
        return f"{m.width}x{m.height}"
    except:
        return "Unknown"

def term():
    return "Windows Console"

def cpu():
    output = subprocess.check_output("wmic cpu get Name", shell=True)
    return output.decode().split("\n")[1].strip()

def gpu():
    try:
        out = subprocess.check_output("wmic path win32_VideoController get name", shell=True).decode().splitlines()
        gpus = [x.strip() for x in out if x.strip() and "Name" not in x]
        return ', '.join(gpus)
    except:
        return "Unknown"

def ram():
    m = psutil.virtual_memory()
    used = round(m.used / (1024**3), 2)
    total = round(m.total / (1024**3), 2)
    return f"{used} GiB / {total} GiB ({m.percent}%)"

def disk():
    d = psutil.disk_usage("C:\\")
    used = d.used / (1024**4)
    total = d.total / (1024**4)
    if total >= 1:
        return f"{used:.1f} TiB / {total:.1f} TiB ({d.percent}%)"
    else:
        return f"{round(d.used / (1024**3))} GiB / {round(d.total / (1024**3))} GiB ({d.percent}%)"

def color_bar():
    colors = [
        (30, 97), (31, 91), (32, 92), (33, 93),
        (34, 94), (35, 95), (36, 96), (97, 97)
    ]
    line1 = line2 = ""
    for fg1, fg2 in colors:
        line1 += f"\033[{fg1}m██{RESET}"
        line2 += f"\033[{fg2}m██{RESET}"
    return line1, line2

def winfetch():
    info = {
        "OS": os_info(),
        "Host": platform.node(),
        "Kernel": kernel(),
        "Motherboard": board(),
        "Uptime": uptime(),
        "Packages": packages(),
        "Resolution": res(),
        "Terminal": term(),
        "CPU": cpu(),
        "GPU": gpu(),
        "Memory": ram(),
        "Disk (C:)": disk()
    }

    uh = user_host()
    print(f" {BLUE}{BLOCK}   {BLOCK}  {YELLOW}{uh}{RESET}")
    print(f" {BLUE}{BLOCK}   {BLOCK}  {YELLOW}" + "-"*len(uh) + f"{RESET}")

    for k, v in info.items():
        if k == "Packages":
            print(f"{' '* (len(BLOCK)*2 + 6)}{YELLOW}{k}:{RESET} {v}")
        else:
            print(f" {BLUE}{BLOCK}   {BLOCK}  {YELLOW}{k}:{RESET} {v}")

    line1, line2 = color_bar()
    print(f" {BLUE}{BLOCK}   {BLOCK}  {line1}")
    print(f" {BLUE}{BLOCK}   {BLOCK}  {line2}")

