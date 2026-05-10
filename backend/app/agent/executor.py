import subprocess
import asyncio
from typing import List

ALLOWED_COMMANDS = {
    "top": ["top", "-b", "-n", "1"],
    "df": ["df", "-h"],
    "free": ["free", "-h"],
    "uptime": ["uptime"],
    "ps": ["ps", "aux"],
    "vmstat": ["vmstat", "1", "3"],
    "iostat": ["iostat", "-x", "1", "2"],
    "netstat": ["netstat", "-tuln"],
    "ss": ["ss", "-tuln"],
    "lsof": ["lsof", "-i"],
    "dmesg": ["dmesg", "--level=err,warn", "-n"],
    "who": ["who"],
    "uname": ["uname", "-a"],
}

class CommandExecutor:
    async def execute(self, command_name: str) -> dict:
        if command_name not in ALLOWED_COMMANDS:
            return {"command": command_name, "status": "error", "output": f"Command '{command_name}' is not in the allowed list."}
        cmd = ALLOWED_COMMANDS[command_name]
        try:
            proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await proc.communicate()
            return {
                "command": command_name, "status": "success" if proc.returncode == 0 else "error",
                "output": stdout.decode("utf-8", errors="replace"),
                "error": stderr.decode("utf-8", errors="replace"),
                "return_code": proc.returncode,
            }
        except Exception as e:
            return {"command": command_name, "status": "error", "output": f"Execution failed: {str(e)}"}
