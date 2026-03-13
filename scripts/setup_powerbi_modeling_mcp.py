from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

repo_root_path = Path(__file__).resolve().parent.parent
if str(repo_root_path) not in sys.path:
    sys.path.insert(0, str(repo_root_path))

from scripts.powerbi_modeling_mcp_common import (
    MCPError,
    discover_server_binary,
    repo_root,
    run_command,
)


def exact_prompt(definition_folder: Path) -> str:
    return f"Open semantic model from PBIP folder '{definition_folder}'"


def ensure_codex_registration(server_path: Path) -> tuple[bool, dict]:
    desired_args = ["--start"]
    get_result = run_command(
        ["codex", "mcp", "get", "powerbi-modeling-mcp", "--json"],
        check=False,
    )
    if get_result.returncode == 0:
        try:
            existing = json.loads(get_result.stdout)
        except json.JSONDecodeError:
            existing = {}
        transport = existing.get("transport", {})
        command = transport.get("command")
        args = transport.get("args", [])
        if command == str(server_path) and args == desired_args:
            return False, existing
        run_command(["codex", "mcp", "remove", "powerbi-modeling-mcp"])
    else:
        missing = "No MCP server named 'powerbi-modeling-mcp' found."
        if missing not in (get_result.stderr or get_result.stdout):
            raise MCPError(get_result.stderr.strip() or get_result.stdout.strip())

    run_command(
        ["codex", "mcp", "add", "powerbi-modeling-mcp", "--", str(server_path), *desired_args]
    )
    registered = json.loads(
        run_command(["codex", "mcp", "get", "powerbi-modeling-mcp", "--json"]).stdout
    )
    return True, registered


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Register the local Power BI Modeling MCP server with Codex and print the PBIP prompt."
    )
    parser.parse_args()

    server_path = discover_server_binary()
    definition_folder = (
        repo_root()
        / "powerbi"
        / "workspaces"
        / "regional-sales-trust-demo"
        / "pbip"
        / "demo_dataset.SemanticModel"
        / "definition"
    )

    run_command(["codex", "--version"])
    changed, registered = ensure_codex_registration(server_path)

    print("Power BI Modeling MCP setup")
    print(f"Server binary : {server_path}")
    print(f"Definition    : {definition_folder}")
    print(f"Codex MCP     : {'registered' if changed else 'already current'}")
    if registered:
        transport = registered.get("transport", {})
        print(f"Command       : {transport.get('command')}")
        print(f"Args          : {transport.get('args')}")
    print()
    print("VS Code / Copilot Chat prompt")
    print(exact_prompt(definition_folder))
    print()
    print("Codex check commands")
    print("codex mcp list")
    print("codex mcp get powerbi-modeling-mcp --json")


if __name__ == "__main__":
    main()
