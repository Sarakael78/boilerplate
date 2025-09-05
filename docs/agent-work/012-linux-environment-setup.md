# Linux/WSL Environment Setup

**Date**: December 2024  
**Purpose**: Ensure bash/WSL/Linux is always used instead of PowerShell

## Overview

This document outlines the configuration changes made to ensure Cursor always uses bash/WSL/Linux environment instead of PowerShell.

## Configuration Files Created

### 1. Cursor Rules (`.cursor/rules/08-linux-environment.mdc`)

- Comprehensive rules for Linux/WSL environment
- Terminal configuration preferences
- File system operations guidelines
- Package management rules
- Git configuration standards

### 2. Cursor Settings (`.cursor/settings.json`)

- Terminal profile configuration
- Locale environment variables
- File line ending settings
- Git configuration
- Editor preferences

### 3. Environment Setup Script (`scripts/setup-linux-env.sh`)

- Automated environment setup
- Locale generation and configuration
- Git configuration for Linux
- Verification commands

## Key Changes Made

### Terminal Configuration

- **Default Shell**: Set to bash for Linux and Git Bash for Windows
- **Environment Variables**: Set LC_ALL and LANG to en_US.UTF-8
- **Shell Arguments**: Use login shell (-l) for proper environment

### File System Settings

- **Line Endings**: Force LF line endings
- **File Operations**: Use Linux-style paths and commands
- **Git Configuration**: Disable autocrlf, set eol to lf

### Development Environment

- **Python**: Use system Python interpreter
- **Package Management**: Use Poetry for Python, npm for Node.js
- **Docker**: Use WSL2 backend

## Usage Instructions

### 1. Run Environment Setup

```bash
# Make script executable
chmod +x scripts/setup-linux-env.sh

# Run setup script
./scripts/setup-linux-env.sh
```

### 2. Apply Changes to Current Session

```bash
# Reload bashrc
source ~/.bashrc

# Verify locale
locale

# Test Git
git status
```

### 3. Verify Configuration

```bash
# Check shell
echo $SHELL

# Check locale
locale

# Check Git config
git config --list
```

## Troubleshooting

### Locale Issues

If you still see locale warnings:

```bash
# Generate locale
sudo locale-gen en_US.UTF-8

# Set environment variables
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```

### Shell Issues

If PowerShell is still being used:

```bash
# Switch to bash
bash

# Check current shell
ps -p $$
```

### Git Issues

If Git still shows warnings:

```bash
# Configure Git for Linux
git config --global core.autocrlf false
git config --global core.eol lf
```

## Compliance Checklist

- [x] Cursor rules created for Linux environment
- [x] Settings file configured for bash/WSL
- [x] Environment setup script created
- [x] Locale configuration documented
- [x] Git configuration for Linux
- [x] File system settings configured
- [x] Package management rules established

## Future Maintenance

### Regular Checks

- Verify terminal is using bash
- Check locale settings
- Confirm Git configuration
- Validate file line endings

### Updates

- Keep Cursor rules updated
- Maintain environment setup script
- Update documentation as needed
- Monitor for new PowerShell usage

## Notes

- All terminal operations should use bash
- All file paths should use forward slashes
- All line endings should be LF
- Locale should be en_US.UTF-8
- Git should be configured for Linux
- No PowerShell commands should be used
