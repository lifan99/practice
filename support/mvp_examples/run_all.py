"""Run the seven provided MVP demonstrations in isolated standard-library processes."""

from pathlib import Path
import subprocess
import sys


EXAMPLES = (
    "protocols.py",
    "quotes.py",
    "concurrency.py",
    "timeouts.py",
    "cancellation.py",
    "http_contract.py",
    "admission.py",
)


def main():
    """Fail on a demonstration error, disabled assertions, or a hung subprocess."""
    if not __debug__:
        raise RuntimeError("Run the demonstrations with assertions enabled")
    directory = Path(__file__).resolve().parent
    for name in EXAMPLES:
        try:
            result = subprocess.run(
                [sys.executable, "-I", "-S", str(directory / name)],
                cwd=directory,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=15,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(f"Demonstration timed out: {name}") from exc
        if result.returncode:
            raise RuntimeError(
                f"Demonstration failed: {name}\n{result.stdout}\n{result.stderr}"
            )
        print(f"PASS {name}")
    print(f"{len(EXAMPLES)} provided demonstrations passed; no live services were called.")


if __name__ == "__main__":
    main()
