# Cursor Rules Classification Summary

**Date**: December 2024  
**Purpose**: Document the classification of Cursor rules for always vs intelligent application

## 🎯 **ALWAYS APPLY Rules** (Critical & High Priority)

These rules are applied to every interaction and code change:

### 1. **Linux Environment Rules** (08-linux-environment.mdc)
- **Status**: ✅ Always Apply
- **Priority**: Critical
- **Scope**: All terminal operations, file system, environment
- **Impact**: Prevents PowerShell usage, maintains proper locale, ensures Linux paths

### 2. **Security Best Practices** (06-security-best-practices.mdc)
- **Status**: ✅ Always Apply
- **Priority**: Critical
- **Scope**: All code, authentication, authorization, validation
- **Impact**: Prevents vulnerabilities, ensures secure practices

### 3. **Code Quality Standards** (04-trunk-usage.mdc)
- **Status**: ✅ Always Apply
- **Priority**: High
- **Scope**: All code changes, linting, formatting
- **Impact**: Prevents linting errors, ensures formatting standards

### 4. **Documentation Quality** (03-documentation-quality.mdc)
- **Status**: ✅ Always Apply
- **Priority**: High
- **Scope**: All documentation, README files, code comments
- **Impact**: Maintains organized documentation structure

## 🤔 **INTELLIGENTLY APPLY Rules** (Medium Priority)

These rules are applied based on context and task:

### 1. **Backend General Rules** (01-backend-general.mdc)
- **Status**: ❌ Always Apply → ✅ Intelligent Apply
- **Priority**: Medium
- **Context**: Backend development, API endpoints, database operations
- **Triggers**: Backend-related tasks, FastAPI, SQLAlchemy, Poetry

### 2. **Frontend React Rules** (02-frontend-react.mdc)
- **Status**: ❌ Always Apply → ✅ Intelligent Apply
- **Priority**: Medium
- **Context**: Frontend development, React components, Next.js pages
- **Triggers**: Frontend-related tasks, React, TypeScript, Tailwind CSS

### 3. **Performance Optimization** (07-performance-optimization.mdc)
- **Status**: ✅ Intelligent Apply
- **Priority**: Medium
- **Context**: Performance-critical code, database queries, API endpoints
- **Triggers**: Performance-related tasks, optimization work

### 4. **Operational Directives** (05-operational-directives.mdc)
- **Status**: ✅ Intelligent Apply
- **Priority**: Medium
- **Context**: Deployment, monitoring, operational tasks
- **Triggers**: DevOps tasks, deployment-related work

### 5. **Component Templates** (react-component-template.mdc)
- **Status**: ✅ Intelligent Apply
- **Priority**: Low
- **Context**: Component creation, UI development
- **Triggers**: Component creation requests

## 📊 **Implementation Summary**

### **Always Apply Rules** (4 rules)
- **Linux Environment**: Critical for consistent development environment
- **Security**: Non-negotiable security standards
- **Code Quality**: Maintains code quality across all work
- **Documentation**: Ensures organized documentation

### **Intelligent Apply Rules** (5 rules)
- **Backend Rules**: Only when working on backend/API
- **Frontend Rules**: Only when working on frontend/UI
- **Performance**: Only when performance is relevant
- **Operations**: Only for operational tasks
- **Templates**: Only when creating components

## 🔧 **Rule Metadata Configuration**

### Always Apply Rules
```yaml
alwaysApply: true
priority: "critical|high"
globs: ["**/*"]  # Apply to all files
```

### Intelligent Apply Rules
```yaml
alwaysApply: false
priority: "medium|low"
globs: ["**/*.py", "**/*.tsx"]  # Specific file patterns
contextTriggers: ["backend", "frontend", "performance"]
```

## 🎯 **Benefits of This Classification**

### **Always Apply Rules**
- **Consistency**: Ensures consistent environment and practices
- **Security**: Maintains security standards across all work
- **Quality**: Preserves code quality standards
- **Documentation**: Maintains organized documentation

### **Intelligent Apply Rules**
- **Relevance**: Only applies rules when contextually appropriate
- **Efficiency**: Avoids unnecessary rule application
- **Focus**: Keeps responses focused on relevant concerns
- **Flexibility**: Adapts to different types of tasks

## 📋 **Compliance Checklist**

- [x] Linux Environment rule set to always apply
- [x] Security rules set to always apply
- [x] Code Quality rules set to always apply
- [x] Documentation rules set to always apply
- [x] Backend rules set to intelligent apply
- [x] Frontend rules set to intelligent apply
- [x] Performance rules set to intelligent apply
- [x] Operations rules set to intelligent apply
- [x] Component templates set to intelligent apply
- [x] Rule classification document created

## 🚀 **Next Steps**

1. **Test Rule Application**: Verify that always-apply rules are enforced in all contexts
2. **Monitor Performance**: Ensure intelligent rules are applied appropriately
3. **Refine Triggers**: Adjust context triggers based on usage patterns
4. **Update Documentation**: Keep rule classification up to date

## 📝 **Notes**

- Always apply rules ensure fundamental standards are maintained
- Intelligent apply rules prevent rule fatigue and maintain focus
- Context triggers help determine when to apply intelligent rules
- Priority levels help manage rule conflicts and importance
