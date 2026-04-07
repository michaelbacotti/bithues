# SKILL.md — script-runner

## What it does
Executes Python scripts from the workspace without shell overhead, returning stdout, stderr, and exit code.

## When to use
- Running workspace Python files or one-liners
- Quick Python tasks that don't need full exec tool environment
- Inline Python code execution with stdin support

## When NOT to use
- For shell/CLI commands (use exec tool directly)
- For Python scripts requiring specific environment setup
- For tasks better handled by a direct exec call

## Inputs
- Script path via `--file` flag or inline code via `--code` flag
- Optional stdin input via `--stdin`

## Outputs
- Stdout, stderr, and exit code (truncated at 50KB output)

## Cost / Risk notes
No external calls. Runs Python via python3 in workspace context.
