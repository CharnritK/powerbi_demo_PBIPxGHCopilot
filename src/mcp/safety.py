"""OS and local-process helpers for Power BI Desktop workflows."""

from __future__ import annotations

from pathlib import Path
import platform
import re
import subprocess

from src.common.errors import MCPError


def server_executable_name() -> str:
    system = platform.system().lower()
    if system == "windows":
        return "powerbi-modeling-mcp.exe"
    if system in {"linux", "darwin"}:
        return "powerbi-modeling-mcp"
    raise MCPError(f"Unsupported platform: {platform.system()}")


def find_power_bi_desktop_exe() -> Path:
    running = run_command(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            "(Get-Process -Name PBIDesktop -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty Path)",
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
            "(Get-AppxPackage -Name Microsoft.MicrosoftPowerBIDesktop | Select-Object -First 1 -ExpandProperty InstallLocation)",
        ],
        check=False,
    ).stdout.strip()
    if install_location:
        path = Path(install_location) / "bin" / "PBIDesktop.exe"
        if path.exists():
            return path

    for path in (
        Path(r"C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe"),
        Path(r"C:\Program Files\Microsoft Power BI Desktop RS\bin\PBIDesktop.exe"),
    ):
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
