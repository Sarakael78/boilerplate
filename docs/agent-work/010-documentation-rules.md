# Documentation Rules for Agent/LLM Work

## File Naming Convention

All documentation created by agents or LLMs must follow this naming pattern:

````text
docs/agent-work/XXX-descriptive-name.md
```text

Where:

- `XXX` is a 3-digit sequential number (001, 002, 003, etc.)
- `descriptive-name` is a kebab-case description of the document content
- `.md` extension for markdown files

## Directory Structure

```text
docs/
├── agent-work/           # All agent/LLM generated documentation
│   ├── 001-improvements-analysis.md
│   ├── 002-poetry-migration-guide.md
│   ├── 003-critical-analysis-summary.md
│   └── ...
├── architecture/         # Architecture documentation
├── setup/               # Setup guides
├── deployment/          # Deployment guides
└── api/                 # API documentation
```text

## Document Headers

Each document must include a header with:

```markdown
# Document Title

**Date**: YYYY-MM-DD
**Agent**: [Agent Name]
**Purpose**: Brief description of the document's purpose

## Overview

[Document content...]
```text

## Progress Tracking

For implementation documents, include:

- [ ] Task 1
- [x] Completed task
- [ ] Task 3

## Version Control

- Each document should be versioned with clear timestamps
- Major changes should create new numbered documents
- Keep historical documents for reference

## Quality Standards

- Clear, concise writing
- Proper markdown formatting
- Include code examples where relevant
- Link to related documents
- Update progress indicators regularly
````
