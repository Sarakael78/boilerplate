# Non-Interactive Git Operations

Git has been configured to run without interactive prompts by:

- Disabling trunk git hooks via core.hookspath = /dev/null
- Configuring trunk.yaml to disable all interactive actions
- Setting repo.interactive = false in trunk configuration

This ensures all git operations run autonomously without requiring user approval.
