"""Run a GitHub CLI or Git command with a GitHub App installation token."""

import argparse
import base64
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


def encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def sign(message: bytes, key: Path) -> bytes:
    return subprocess.run(
        ["openssl", "dgst", "-sha256", "-sign", str(key)],
        input=message,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=True,
    ).stdout


def create_jwt(app_id: str, key: Path) -> str:
    now = int(time.time())
    header = encode(b'{"alg":"RS256","typ":"JWT"}')
    claims = json.dumps(
        {"iat": now - 60, "exp": now + 540, "iss": app_id}, separators=(",", ":")
    )
    unsigned = f"{header}.{encode(claims.encode())}"
    return f"{unsigned}.{encode(sign(unsigned.encode(), key))}"


def installation_token(jwt: str, installation_id: str) -> str:
    request = urllib.request.Request(
        f"https://api.github.com/app/installations/{installation_id}/access_tokens",
        data=b"{}",
        headers={
            "Authorization": f"Bearer {jwt}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "github-app-wrapper",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        result = json.loads(response.read())
    token = result.get("token") if isinstance(result, dict) else None
    if not isinstance(token, str) or not token:
        raise ValueError("GitHub returned an invalid installation token")
    return token


def child_environment(tool: str, token: str) -> dict[str, str]:
    env = os.environ.copy()
    for name in (
        "GH_TOKEN",
        "GITHUB_TOKEN",
        "GH_ENTERPRISE_TOKEN",
        "GITHUB_ENTERPRISE_TOKEN",
    ):
        env.pop(name, None)
    if tool == "gh":
        env["GH_TOKEN"] = token
        env["GH_HOST"] = "github.com"
    else:
        credential = base64.b64encode(f"x-access-token:{token}".encode()).decode(
            "ascii"
        )
        env["GIT_CONFIG_COUNT"] = "1"
        env["GIT_CONFIG_KEY_0"] = "http.https://github.com/.extraheader"
        env["GIT_CONFIG_VALUE_0"] = f"AUTHORIZATION: basic {credential}"
        env["GIT_TERMINAL_PROMPT"] = "0"
    return env


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app-id", default=os.environ.get("GITHUB_APP_ID", "5708654"))
    parser.add_argument(
        "--installation-id",
        default=os.environ.get("GITHUB_APP_INSTALLATION_ID", "180787526"),
    )
    parser.add_argument(
        "--key",
        type=Path,
        default=Path(
            os.environ.get(
                "GITHUB_APP_KEY", "~/.config/kai-codex-agent/private-key.pem"
            )
        ).expanduser(),
    )
    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="Command: gh or git followed by its arguments",
    )
    args = parser.parse_args()
    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command or command[0] not in ("gh", "git"):
        parser.error("command must start with gh or git")
    if not args.app_id.isdecimal() or not args.installation_id.isdecimal():
        parser.error("app ID and installation ID must be numeric")
    try:
        jwt = create_jwt(args.app_id, args.key.expanduser())
        token = installation_token(jwt, args.installation_id)
        return subprocess.run(
            command, env=child_environment(command[0], token), check=False
        ).returncode
    except (
        OSError,
        subprocess.CalledProcessError,
        urllib.error.URLError,
        ValueError,
    ) as error:
        print(f"GitHub App access failed: {type(error).__name__}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
