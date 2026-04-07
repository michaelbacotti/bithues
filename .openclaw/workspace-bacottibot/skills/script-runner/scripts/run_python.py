#!/usr/bin/env python3
"""
Script Runner — execute Python scripts from the workspace.
Usage:
  python3 run_python.py --file <path>     Run a Python file
  python3 run_python.py --code <code>     Run inline Python code
  python3 run_python.py --stdin           Run code from stdin
"""

import sys
import argparse
import io
import contextlib

MAX_OUTPUT = 50 * 1024  # 50KB


def run_code(code: str) -> tuple[str, str, int]:
    """Execute Python code and capture stdout/stderr."""
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()

    try:
        with contextlib.redirect_stdout(stdout_buf), contextlib.redirect_stderr(stderr_buf):
            exec(code, {"__name__": "__main__"})
        return stdout_buf.getvalue(), stderr_buf.getvalue(), 0
    except SystemExit as e:
        return stdout_buf.getvalue(), stderr_buf.getvalue(), e.code if e.code is not None else 0
    except Exception as e:
        stderr_buf.write(f"{type(e).__name__}: {e}")
        return stdout_buf.getvalue(), stderr_buf.getvalue(), 1


def main():
    parser = argparse.ArgumentParser(description="Run Python scripts from workspace")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", "-f", help="Path to Python file to execute")
    group.add_argument("--code", "-c", help="Inline Python code to execute")
    group.add_argument("--stdin", "-s", action="store_true", help="Read code from stdin")
    args = parser.parse_args()

    if args.stdin:
        code = sys.stdin.read()
    elif args.file:
        with open(args.file, "r") as f:
            code = f.read()
    else:
        code = args.code

    stdout, stderr, code = run_code(code)

    if stdout:
        sys.stdout.write(stdout[:MAX_OUTPUT])
    if stderr:
        sys.stderr.write(stderr[:MAX_OUTPUT])

    sys.exit(code)


if __name__ == "__main__":
    main()
