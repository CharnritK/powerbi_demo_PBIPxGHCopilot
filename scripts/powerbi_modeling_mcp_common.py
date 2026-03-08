from __future__ import annotations

import json
import platform
import queue
import re
import subprocess
import threading
import time
from pathlib import Path
from typing import Any


class MCPError(RuntimeError):
    pass


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def server_executable_name() -> str:
    system = platform.system().lower()
    if system == "windows":
        return "powerbi-modeling-mcp.exe"
    if system in {"linux", "darwin"}:
        return "powerbi-modeling-mcp"
    raise MCPError(f"Unsupported platform: {platform.system()}")


def discover_server_binary() -> Path:
    extensions_dir = Path.home() / ".vscode" / "extensions"
    pattern = "analysis-services.powerbi-modeling-mcp-*"
    candidates = []
    for extension_dir in extensions_dir.glob(pattern):
        server_path = extension_dir / "server" / server_executable_name()
        if server_path.exists():
            candidates.append(server_path)
    if not candidates:
        raise MCPError(
            "Power BI Modeling MCP server binary was not found under ~/.vscode/extensions. "
            "Install the 'analysis-services.powerbi-modeling-mcp' VS Code extension first."
        )
    return max(candidates, key=lambda path: path.stat().st_mtime)


def run_command(args: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        check=False,
    )
    if check and completed.returncode != 0:
        output = completed.stderr.strip() or completed.stdout.strip()
        raise MCPError(f"Command failed: {' '.join(args)}\n{output}")
    return completed


def parse_json_text_content(response: dict[str, Any]) -> list[dict[str, Any]]:
    contents = response.get("result", {}).get("content", [])
    parsed: list[dict[str, Any]] = []
    for item in contents:
        if item.get("type") != "text":
            continue
        parsed.append(json.loads(item["text"]))
    return parsed


def extract_resources(response: dict[str, Any]) -> list[dict[str, Any]]:
    contents = response.get("result", {}).get("content", [])
    return [item["resource"] for item in contents if item.get("type") == "resource"]


class PowerBIModelingMCPClient:
    def __init__(self, server_path: Path, args: list[str] | None = None) -> None:
        self.server_path = server_path
        self.args = args or ["--start"]
        self._process: subprocess.Popen[str] | None = None
        self._stdout_queue: queue.Queue[str] = queue.Queue()
        self._stderr_lines: list[str] = []
        self._next_id = 1

    def __enter__(self) -> "PowerBIModelingMCPClient":
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def start(self) -> None:
        if self._process is not None:
            return
        self._process = subprocess.Popen(
            [str(self.server_path), *self.args],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        assert self._process.stdout is not None
        assert self._process.stderr is not None
        threading.Thread(target=self._pump_stdout, daemon=True).start()
        threading.Thread(target=self._pump_stderr, daemon=True).start()
        self.initialize()

    def close(self) -> None:
        if self._process is None:
            return
        if self._process.poll() is None:
            self._process.kill()
            try:
                self._process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                pass
        self._process = None

    def initialize(self) -> None:
        self.request(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "powerbi-demo-script", "version": "1.0"},
            },
        )
        self.notify("notifications/initialized", {})

    def notify(self, method: str, params: dict[str, Any]) -> None:
        self._send({"jsonrpc": "2.0", "method": method, "params": params})

    def request(self, method: str, params: dict[str, Any], timeout_seconds: int = 60) -> dict[str, Any]:
        message_id = self._next_id
        self._next_id += 1
        self._send({"jsonrpc": "2.0", "id": message_id, "method": method, "params": params})
        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            try:
                raw = self._stdout_queue.get(timeout=0.5)
            except queue.Empty:
                self._raise_if_exited()
                continue
            payload = json.loads(raw)
            if payload.get("id") == message_id:
                return payload
        raise MCPError(f"MCP request timed out for method '{method}'.\n{self.stderr_tail()}")

    def call_tool(self, name: str, arguments: dict[str, Any], timeout_seconds: int = 60) -> dict[str, Any]:
        response = self.request(
            "tools/call",
            {"name": name, "arguments": arguments},
            timeout_seconds=timeout_seconds,
        )
        if response.get("result", {}).get("isError"):
            raise MCPError(f"Tool '{name}' failed.\n{json.dumps(response, indent=2)}")
        return response

    def stderr_tail(self, max_lines: int = 20) -> str:
        lines = self._stderr_lines[-max_lines:]
        return "\n".join(lines)

    def _send(self, payload: dict[str, Any]) -> None:
        if self._process is None or self._process.stdin is None:
            raise MCPError("MCP process is not running.")
        self._process.stdin.write(json.dumps(payload) + "\n")
        self._process.stdin.flush()

    def _raise_if_exited(self) -> None:
        if self._process is None:
            raise MCPError("MCP process is not running.")
        if self._process.poll() is not None:
            raise MCPError(
                f"MCP process exited with code {self._process.returncode}.\n{self.stderr_tail()}"
            )

    def _pump_stdout(self) -> None:
        assert self._process is not None and self._process.stdout is not None
        for line in self._process.stdout:
            stripped = line.rstrip("\r\n")
            if stripped:
                self._stdout_queue.put(stripped)

    def _pump_stderr(self) -> None:
        assert self._process is not None and self._process.stderr is not None
        for line in self._process.stderr:
            stripped = line.rstrip("\r\n")
            if stripped:
                self._stderr_lines.append(stripped)


def find_power_bi_desktop_exe() -> Path:
    running = run_command(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            "(Get-Process -Name PBIDesktop -ErrorAction SilentlyContinue | "
            "Select-Object -First 1 -ExpandProperty Path)",
        ],
        check=False,
    ).stdout.strip()
    if running:
        path = Path(running)
        if path.exists():
            return path

    install_location = run_command(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            "(Get-AppxPackage -Name Microsoft.MicrosoftPowerBIDesktop | "
            "Select-Object -First 1 -ExpandProperty InstallLocation)",
        ],
        check=False,
    ).stdout.strip()
    if install_location:
        path = Path(install_location) / "bin" / "PBIDesktop.exe"
        if path.exists():
            return path

    known_paths = [
        Path(r"C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe"),
        Path(r"C:\Program Files\Microsoft Power BI Desktop RS\bin\PBIDesktop.exe"),
    ]
    for path in known_paths:
        if path.exists():
            return path

    raise MCPError("Power BI Desktop executable was not found.")


def normalize_windows_slashes(value: str) -> str:
    return re.sub(r"[\\/]+", r"\\", value)


def close_power_bi_desktop_window(window_title: str) -> None:
    run_command(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            "Get-Process -Name PBIDesktop -ErrorAction SilentlyContinue | "
            f"Where-Object {{ $_.MainWindowTitle -eq '{window_title}' }} | "
            "ForEach-Object { Stop-Process -Id $_.Id -Force }",
        ],
        check=False,
    )
