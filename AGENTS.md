# 1. Agent Operational Protocol

### A. Core Directives

- **Goal-Oriented Action**: Before any action, state your goal. After completion, confirm the outcome.
- **Tool Utilisation**: You have access to a suite of tools (MCP, terminal). Use the best tool for the job.
- **Problem Decomposition**: For complex requests, break the problem down into a sequence of smaller, verifiable steps. Announce the plan before executing.
- **Code Quality Mandate**: Before completing any task or telling the user you are complete, you MUST run `trunk check --fix` to ensure all linting issues are resolved. Never leave linting errors in the codebase.
- **Documentation Standards**: All documentation files (except README.md) must be placed in the `/docs` folder. This includes API documentation, architectural decisions, setup guides, and any other project documentation.
- **Complete Implementation**: Never leave TODO comments, placeholder functions, or incomplete implementations. Every feature must be fully functional and production-ready.

### B. Filesystem & Terminal Interaction (PowerShell Context)

- **Environment**: Your default terminal is PowerShell on Windows. Use PowerShell-compatible syntax (e.g., `ls` is `Get-ChildItem`, `cat` is `Get-Content`).
- **Python Environment**: Use `poetry run <command>` for all Python operations. Do not use virtual environment activation commands.
- **Code Quality**: Before committing, always run `trunk check --fix` to ensure code quality and consistent formatting.

### C. Trunk Code Quality Workflow

- **Initial Setup**: Run `trunk init` in a git repository with committed files
- **Daily Workflow**:
  1. `trunk check` - identify issues
  2. `trunk check --fix` - auto-fix issues
  3. `trunk fmt` - format code
  4. `trunk check` - verify clean state
- **Pre-Commit**: Always run `trunk check --fix` before completing any task
- **Troubleshooting**: Check `.trunk/out/` for detailed error logs

### D. MCP Tool Setup Protocol

- **Verification**: Before use, verify that the third-party MCP tool server is running locally.
- **Setup (If Not Running)**:
  1.  Announce the need to start the required MCP server.
  2.  Use the terminal to navigate to the designated local directory for MCP tools.
  3.  Clone the designated MCP server repository if it doesn't already exist. A list of required repositories is:
      - **Filesystem**: `https://github.com/example/mcp-filesystem.git`
      - **Memory/KG**: `https://github.com/example/mcp-memory.git`
      - **Sequential Thinking**: `https://github.com/example/mcp-sequential-thinker.git`
      - **WSL Executor**: `https://github.com/example/mcp-wsl.git`
      - **Browser Automation**: `https://github.com/example/mcp-playwright.git`
      - **API Testing**: `https://github.com/example/mcp-postman.git`
  4.  Follow the `README.md` in the repository to install dependencies and start the server.
  5.  Confirm the server is running and accessible before proceeding.

---

# 2. Project Initialisation & Standards

### A. Initial File Creation

If the project is new or missing configuration files, create them in the root directory with the exact content specified in the project's Kickstart Kit.

### B. Code Style & Documentation

- **Linting & Formatting**: Adhere strictly to the rules in `trunk.yaml`, `.prettierrc.json`, and `.eslintrc.json`.
- **Python**: All backend code must be Python 3.10+ with full type hints. Use `snake_case` for variables/functions and `PascalCase` for classes.
- **In-Code Documentation**: All modules, classes, and functions must have clear, descriptive docstrings (Google Python Style) explaining their purpose, arguments, and return values.
- **Documentation Organization**: All documentation files (except README.md) must be placed in the `/docs` folder.

### C. Architecture

- **Core Stack**:
  - **Backend**: FastAPI (Python)
  - **Frontend**: Next.js (React)
  - **Database**: PostgreSQL
  - **Caching**: Redis
- **Extended Stack for Scaling**:
  - **Logging & Search (ELK)**: Elasticsearch, Logstash, Kibana
  - **Async Tasks**: RabbitMQ
  - **Monitoring**: Prometheus & Grafana
- **Data Access**: Follow the repository pattern.
- **User Configurability**: All settings (ports, URLs, keys) must be configurable via environment variables, loaded from a `.env` file, and documented in `.env.example`. Hardcoding variables is forbidden.

### D. Project Management & Documentation

- **README.md**: Maintain a `README.md` with a project overview and setup instructions.
- **Documentation Folder**: Maintain a `docs/` folder for all detailed documentation.
- **Project Plan**: The `docs/` folder must contain `project_plan.md`. This is a living document that you must update with every significant contribution, detailing goals, current status, next steps, and architectural decisions.

### E. Development Workflow

- **Containerisation**: The entire stack must be containerized using Docker and defined in `docker-compose.yml`.
- **Startup Script**: A `run-dev.sh` script must exist to build and launch the full stack.
- **CI/CD**: The CI workflow is defined in `.github/workflows/ci.yml`.
- **Code Quality**: Before completing any task, run `trunk check --fix` to ensure all linting issues are resolved.

### F. Testing & Commits

- **Testing**: Every feature requires tests. Every bug fix requires a regression test.
- **Commit Messages**: Follow the Conventional Commits specification.
