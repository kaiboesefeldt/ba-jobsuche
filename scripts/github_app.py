"""Access the GitHub API or run Git with a GitHub App installation token."""

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

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def sign(message: bytes, key: Path) -> bytes:
    private_key = serialization.load_pem_private_key(key.read_bytes(), password=None)
    if not isinstance(private_key, rsa.RSAPrivateKey):
        raise TypeError("GitHub App key must be an RSA private key")
    return private_key.sign(message, padding.PKCS1v15(), hashes.SHA256())


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
    result = json.loads(open_request(request))
    token = result.get("token") if isinstance(result, dict) else None
    if not isinstance(token, str) or not token:
        raise ValueError("GitHub returned an invalid installation token")
    return token


def open_request(request: urllib.request.Request) -> bytes:
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    with urllib.request.build_opener(NoRedirect).open(request, timeout=20) as response:
        return response.read()


def api_request(token: str, path: str, method: str, data: bytes | None) -> bytes:
    if not path.startswith("/") or path.startswith("//") or "#" in path:
        raise ValueError("API path must be an absolute path on api.github.com")
    request = urllib.request.Request(
        "https://api.github.com" + path,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "github-app-wrapper",
        },
        method=method,
    )
    return open_request(request)


def git_environment(token: str) -> dict[str, str]:
    env = os.environ.copy()
    for name in (
        "GH_TOKEN",
        "GITHUB_TOKEN",
        "GH_ENTERPRISE_TOKEN",
        "GITHUB_ENTERPRISE_TOKEN",
    ):
        env.pop(name, None)
    credential = base64.b64encode(f"x-access-token:{token}".encode()).decode("ascii")
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
    commands = parser.add_subparsers(dest="command", required=True)
    api = commands.add_parser("api", help="Call the GitHub REST API")
    api.add_argument(
        "--method", choices=("GET", "POST", "PATCH", "PUT", "DELETE"), default="GET"
    )
    api.add_argument("--input", type=Path, help="JSON request body file")
    api.add_argument("path", help="Absolute API path, including optional query")
    git = commands.add_parser("git", help="Run Git with the installation token")
    git.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if not args.app_id.isdecimal() or not args.installation_id.isdecimal():
        parser.error("app ID and installation ID must be numeric")
    try:
        jwt = create_jwt(args.app_id, args.key.expanduser())
        token = installation_token(jwt, args.installation_id)
        if args.command == "api":
            data = args.input.read_bytes() if args.input else None
            if data is not None:
                json.loads(data)
            sys.stdout.buffer.write(api_request(token, args.path, args.method, data))
            return 0
        return subprocess.run(
            ["git", *args.arguments], env=git_environment(token), check=False
        ).returncode
    except urllib.error.HTTPError as error:
        print(f"GitHub App access failed: HTTP {error.code}", file=sys.stderr)
        return 1
    except (
        OSError,
        subprocess.CalledProcessError,
        urllib.error.URLError,
        TypeError,
        ValueError,
    ) as error:
        print(f"GitHub App access failed: {type(error).__name__}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
