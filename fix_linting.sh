#!/bin/bash

# Disable all pagers
export PAGER=cat
export LESS=cat
export GIT_PAGER=cat
export TRUNK_PAGER=cat

# Set git pager to cat
git config --global core.pager cat

# Run trunk check and fix
echo "Running trunk check --fix..."
trunk check --fix

# Run trunk check again to verify
echo "Running trunk check to verify..."
trunk check

# Check git status
echo "Git status:"
git status

echo "Done!"
