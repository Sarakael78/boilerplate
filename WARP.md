# Project Rules Reference

This file explains where to find the full set of development rules and standards for this project.

## ⚠️ IMPORTANT: Purpose of This File

**This WARP.md file is ONLY a directory and reference guide. It must NOT be used as a source of individual development rules or standards.**

**Purpose**: Direct agents to the correct rule files in `.cursor/rules/`
**Not for**: Actual development standards, coding guidelines, or task requirements

All specific rules, standards, and requirements are located in the individual `.mdc` files in `.cursor/rules/`. Agents must consult those files directly for actual implementation guidance.

## 🚨 CRITICAL: ALWAYS-APPLY COMPLETION REQUIREMENTS

**These requirements apply to EVERY task completion:**

### **MANDATORY PRE-COMPLETION CHECKLIST**

Before informing the user that ANY work is complete, you MUST:

1. **Run Trunk Check**: Execute `trunk check --no-progress --ci` to identify ALL issues
2. **Auto-Fix Issues**: Run `trunk check --fix --no-progress --ci` to fix all fixable issues
3. **Final Verification**: Run `trunk check --no-progress --ci` again to verify ALL issues resolved
4. **Update Project Plan**: Update `docs/PROJECT_PLAN.md` with completion details
5. **Create Completion Summary**: Create numbered summary in `/docs/agent-work/`
6. **Update Documentation**: Amend README.md if changes affect setup/features
7. **Verify Rule Compliance**: Confirm ALL applicable rules were followed

### **COMPLETION CHECKPOINT QUESTIONS (MANDATORY)**

Before ANY completion statement, you MUST answer these questions:

1. ❓ Have I run `trunk check --no-progress --ci` and verified zero issues?
2. ❓ Have I created a numbered completion summary in `/docs/agent-work/`?
3. ❓ Have I updated `docs/PROJECT_PLAN.md` with completion details?
4. ❓ Have I updated README.md if the changes affect setup/features?
5. ❓ Have I verified all code quality standards are met?
6. ❓ **Have I confirmed that ALL critical rules (always-apply) were followed?**
7. ❓ **Have I identified and applied all relevant context-specific rules?**

**If ANY answer is NO, you CANNOT declare completion.**

### **RULE COMPLIANCE VERIFICATION**

**Critical Rules (Must ALWAYS be applied):**

- ✅ **Rule Classification** (00): Used proper rule application strategy
- ✅ **Documentation Quality** (03): All docs properly formatted and updated
- ✅ **Trunk Usage** (04): All code quality checks passed
- ✅ **Security Best Practices** (06): Security standards followed
- ✅ **Linux Environment** (08): Linux-compatible commands and practices used
- ✅ **Task Completion Requirements** (09): This checklist followed
- ✅ **Agent Operational Protocol** (10): Proper workflow followed
- ✅ **Rule File Standards** (11): Any rule modifications follow metadata standards

**Context-Specific Rules (Applied based on task type):**

- 🔍 **Backend General** (01): Applied if backend development work
- 🔍 **Frontend React** (02): Applied if frontend development work
- 🔍 **Operational Directives** (05): Applied if deployment/operational work
- 🔍 **Performance Optimization** (07): Applied if performance-related work
- 🔍 **Templates**: Applied if creating new components

### **COMPLETION TRIGGERS**

These words/phrases AUTOMATICALLY trigger the mandatory completion workflow:

- "completed" / "complete" / "finished" / "done"
- "task is complete" / "work is finished" / "successfully completed"
- Any variant indicating task completion

### **MANDATORY COMPLETION TEMPLATE**

Only use this format after ALL requirements are verified:

```
✅ MANDATORY COMPLETION CHECKPOINT PASSED

Pre-completion verification:
- ✅ Trunk check: No issues found
- ✅ Documentation: Completion summary created (XXX-filename.md)
- ✅ Project plan: Updated with completion timestamp
- ✅ README: Updated with relevant changes (if applicable)
- ✅ Quality standards: All requirements met

Rule compliance verification:
- ✅ Critical rules: All 8 always-apply rules followed
- ✅ Context rules: [List specific rules applied for this task]
- ✅ Standards: All applicable coding/documentation standards met
- ✅ Verification: Manually confirmed rule compliance

Task completed successfully!
```

## 📁 Rule Location

All comprehensive development rules are located in:

```text
.cursor/rules/
```

## 📋 Rule Files Overview

### Critical Priority Rules (Always Apply - 8 rules)

- **`00-rule-classification.mdc`** - Master rule classification and decision matrix
- **`03-documentation-quality.mdc`** - Documentation standards and project plan requirements
- **`04-trunk-usage.mdc`** - Code quality tools and linting standards
- **`06-security-best-practices.mdc`** - Security requirements and best practices
- **`08-linux-environment.mdc`** - Linux/WSL environment configuration
- **`09-task-completion-requirements.mdc`** - Quality gates before task completion
- **`10-agent-operational-protocol.mdc`** - Agent workflow and operational standards
- **`11-rule-file-standards.mdc`** - Rule file creation and metadata standards

### Context-Specific Rules (Apply When Relevant - 4 rules)

- **`01-backend-general.mdc`** - FastAPI, Python, SQLAlchemy, Poetry standards
- **`02-frontend-react.mdc`** - Next.js, React, TypeScript, Tailwind standards
- **`05-operational-directives.mdc`** - Deployment, monitoring, DevOps practices
- **`07-performance-optimization.mdc`** - Performance standards and optimization

### Templates (2 templates)

- **`python-service-template.mdc`** - Python service creation template
- **`react-component-template.mdc`** - React component creation template

## 🎯 Rule Application Strategy

### Always Applied (8 rules)

Critical rules that apply to every interaction and code change to ensure:

- Consistent Linux environment
- Security compliance
- Code quality standards
- Documentation requirements
- Proper task completion
- Proper operational protocol
- Rule file standards

### Intelligently Applied (4 rules + 2 templates)

Context-specific rules that apply based on the task:

- Backend development → Backend rules (01)
- Frontend development → Frontend rules (02)
- Deployment/Operations → Operational rules (05)
- Performance work → Performance rules (07)
- Component creation → Appropriate template

## 📚 How to Use

1. **For comprehensive standards**: Check the specific rule files in `.cursor/rules/`
2. **For rule decisions**: Start with `00-rule-classification.mdc`
3. **For task completion**: Always reference `09-task-completion-requirements.mdc`
4. **For new components**: Use appropriate template files
5. **Before completion**: Verify ALL applicable rules were followed

## 🔧 Essential Commands

### Non-Interactive Code Quality

```bash
# Identify issues
trunk check --no-progress --ci

# Auto-fix issues
trunk check --fix --no-progress --ci

# Format code
trunk fmt --no-progress --ci
```

### Environment Setup

```bash
# Start development environment
./run-dev.sh

# Set up environment
cp env.example .env
```

## ⚠️ Important

- Work is only complete when `trunk check --no-progress --ci` shows zero issues
- All rules in `.cursor/rules/` are automatically applied by compatible IDEs
- Refer to individual rule files for detailed requirements and standards
- **CRITICAL**: The completion requirements above apply to every single task
- **MANDATORY**: Verify rule compliance before declaring completion
