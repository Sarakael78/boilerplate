#!/bin/bash

# Environment Setup Script for Linux/WSL
# This script ensures proper locale and shell configuration

set -e

echo "🔧 Setting up Linux/WSL environment..."

# Check if we're in WSL
if grep -qi microsoft /proc/version; then
	echo "✅ WSL detected"
else
	echo "ℹ️  Running on native Linux"
fi

# Generate and set locale
echo "🌍 Setting up locale..."
if ! locale -a | grep -q "en_US.utf8"; then
	echo "Generating en_US.UTF-8 locale..."
	sudo locale-gen en_US.UTF-8
fi

# Set environment variables
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

# Add to .bashrc if not already present
if ! grep -q "export LC_ALL=en_US.UTF-8" ~/.bashrc; then
	echo "export LC_ALL=en_US.UTF-8" >>~/.bashrc
	echo "export LANG=en_US.UTF-8" >>~/.bashrc
	echo "✅ Added locale exports to .bashrc"
fi

# Configure Git for Linux
echo "🔧 Configuring Git..."
git config --global core.autocrlf false
git config --global core.eol lf
git config --global init.defaultBranch main

# Verify shell
echo "🐚 Checking shell configuration..."
echo "Current shell: ${SHELL}"
echo "Current process: $(ps -p $$ -o comm=)"

# Verify locale
echo "🌍 Checking locale..."
locale

# Verify Git configuration
echo "🔧 Checking Git configuration..."
git config --list | grep -E "(core\.|init\.)"

echo "✅ Environment setup complete!"
echo ""
echo "To apply changes to current session, run:"
echo "source ~/.bashrc"
echo ""
echo "To verify everything is working, run:"
echo "git status"
