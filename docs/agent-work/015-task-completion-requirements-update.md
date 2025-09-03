# Cursor Rules Update: Task Completion Requirements

**Date**: December 2024  
**Purpose**: Update Cursor rules to emphasize trunk linting must be completed before marking work as complete

## 🚨 **Critical Update Summary**

All Cursor rules have been updated to emphasize that **trunk linting must be completed and ALL issues fixed before informing the user that work is complete**.

## ✅ **Updated Rules**

### **1. Code Quality Standards** (04-trunk-usage.mdc)
- **Priority**: Upgraded from High to **Critical**
- **Scope**: Expanded to include shell scripts and markdown files
- **New Requirements**:
  - CRITICAL COMPLETION REQUIREMENT section added
  - Mandatory trunk check before completion
  - Zero tolerance for linting errors
  - Auto-fix and manual fix requirements

### **2. Operational Directives** (05-operational-directives.mdc)
- **Added**: CRITICAL COMPLETION REQUIREMENT section
- **Emphasis**: Non-negotiable trunk linting before completion
- **Scope**: All operational tasks

### **3. Backend General Rules** (01-backend-general.mdc)
- **Added**: CRITICAL COMPLETION REQUIREMENT section
- **Requirement**: Must run trunk check and fix ALL issues
- **Scope**: All backend development work

### **4. Frontend React Rules** (02-frontend-react.mdc)
- **Added**: CRITICAL COMPLETION REQUIREMENT section
- **Requirement**: Must run trunk check and fix ALL issues
- **Scope**: All frontend development work

### **5. New Rule: Task Completion Requirements** (09-task-completion-requirements.mdc)
- **Priority**: Critical
- **Scope**: All task completions
- **Purpose**: Enforce quality standards before completion
- **Always Apply**: true

## 📋 **Mandatory Pre-Completion Checklist**

Before marking ANY work as complete:

1. **Run Trunk Check**: `trunk check` to identify ALL issues
2. **Auto-Fix Issues**: `trunk check --fix` to fix auto-fixable issues
3. **Manual Fixes**: Fix any remaining issues manually
4. **Final Verification**: `trunk check` again to verify zero issues
5. **Zero Tolerance**: Only complete if "No issues" or "0 failures"

## 🚫 **Completion Blockers**

Work MUST NOT be marked complete if:
- Trunk check shows ANY failures, errors, or warnings
- Linting issues exist in any file
- Code formatting is inconsistent
- Unresolved code quality issues remain
- Shell scripts have linting errors
- Documentation has formatting issues

## ✅ **Completion Verification**

Before saying "work is complete", verify:
- ✅ `trunk check` shows "No issues" or "0 failures"
- ✅ All code follows project standards
- ✅ All files are properly formatted
- ✅ No linting errors remain
- ✅ Code quality standards are met

## 📊 **Updated Rule Classification**

### **Always Apply Rules** (5 rules)
1. **Linux Environment Rules** - Critical priority
2. **Security Best Practices** - Critical priority
3. **Code Quality Standards** - Critical priority (upgraded)
4. **Documentation Quality** - High priority
5. **Task Completion Requirements** - Critical priority (new)

### **Intelligent Apply Rules** (5 rules)
1. **Backend General Rules** - Medium priority
2. **Frontend React Rules** - Medium priority
3. **Performance Optimization** - Medium priority
4. **Operational Directives** - Medium priority
5. **Component Templates** - Low priority

## 🎯 **Impact of Changes**

### **Enhanced Quality Control**
- **Zero Tolerance**: No work completion with linting errors
- **Mandatory Checks**: Trunk check required before completion
- **Quality Assurance**: Consistent code quality across all work

### **Improved User Experience**
- **Reliable Deliverables**: All completed work meets quality standards
- **Consistent Standards**: Uniform code quality across the project
- **Professional Output**: Production-ready code every time

### **Better Development Practices**
- **Proactive Quality**: Issues caught and fixed before completion
- **Standardized Process**: Consistent completion workflow
- **Quality Culture**: Quality-first approach to all work

## 📝 **Implementation Notes**

### **Rule Enforcement**
- **Always Apply**: Critical rules enforced in all contexts
- **No Exceptions**: Zero tolerance for quality issues
- **Mandatory Process**: Trunk check required before completion

### **File Coverage**
- **Expanded Scope**: Shell scripts and markdown files included
- **Comprehensive Checks**: All file types covered by trunk
- **Quality Standards**: Consistent standards across all file types

### **Completion Workflow**
1. Complete the requested work
2. Run `trunk check` to identify issues
3. Run `trunk check --fix` to auto-fix issues
4. Manually fix any remaining issues
5. Run `trunk check` again for final verification
6. Only then inform user of completion

## 🚀 **Next Steps**

1. **Test Rule Application**: Verify new rules are enforced
2. **Monitor Compliance**: Ensure trunk checks are always run
3. **Quality Metrics**: Track improvement in code quality
4. **User Feedback**: Monitor user satisfaction with deliverables

## 📋 **Compliance Checklist**

- [x] Code Quality Standards upgraded to Critical priority
- [x] Task Completion Requirements rule created
- [x] All development rules updated with completion requirements
- [x] Rule classification updated
- [x] File coverage expanded to include shell scripts and markdown
- [x] Zero tolerance policy established
- [x] Mandatory pre-completion checklist defined
- [x] Completion verification process documented
