# Cursor Rules Update: Documentation and Project Plan Requirements

**Date**: December 2024  
**Purpose**: Update Cursor rules to ensure project plan updates and documentation amendments before completion

## 🚨 **Critical Update Summary**

All Cursor rules have been updated to ensure that **the project plan is updated after each successful agent completion** and **README.md and other documentation are amended before informing the user that work is complete**.

## ✅ **Updated Rules**

### **1. Task Completion Requirements** (09-task-completion-requirements.mdc)
- **Added**: Documentation update requirements section
- **New Requirements**:
  - Update project plan with completion details
  - Amend README.md with relevant changes
  - Update other documentation as needed
  - Verify all documentation is current

### **2. Documentation Quality** (03-documentation-quality.mdc)
- **Priority**: Upgraded from High to **Critical**
- **Added**: CRITICAL COMPLETION REQUIREMENT section
- **Scope**: Expanded to include project plan updates
- **New Requirements**:
  - Update project plan after completion
  - Amend README.md with changes
  - Update relevant documentation
  - Ensure documentation reflects current state

## 📋 **Mandatory Pre-Completion Checklist**

Before marking ANY work as complete:

1. **Run Trunk Check**: `trunk check` to identify ALL issues
2. **Auto-Fix Issues**: `trunk check --fix` to fix auto-fixable issues
3. **Manual Fixes**: Fix any remaining issues manually
4. **Final Verification**: `trunk check` again to verify zero issues
5. **Update Project Plan**: Update `docs/agent-work/project_plan.md` with completion details
6. **Update Documentation**: Amend README.md and any other relevant documentation
7. **Zero Tolerance**: Only complete if all requirements are met

## 📝 **Documentation Update Requirements**

### **Project Plan Updates** (`docs/agent-work/project_plan.md`)
- Add completion timestamp
- Update task status to "Completed"
- Add summary of what was accomplished
- Update progress indicators
- Add any new tasks discovered during work

### **README.md Updates**
- Update any relevant sections
- Add new features or capabilities
- Update version information if applicable
- Ensure all links and references are current
- Update installation or setup instructions if needed

### **Other Documentation Updates**
- Update any API documentation
- Amend setup guides if changed
- Update architecture documentation if modified
- Ensure all documentation reflects current state

## ✅ **Completion Verification**

Before saying "work is complete", verify:
- ✅ `trunk check` shows "No issues" or "0 failures"
- ✅ All code follows project standards
- ✅ All files are properly formatted
- ✅ No linting errors remain
- ✅ Code quality standards are met
- ✅ Project plan has been updated with completion details
- ✅ README.md has been amended if needed
- ✅ All relevant documentation is current and accurate

## 📊 **Updated Rule Classification**

### **Always Apply Rules** (5 rules)
1. **Linux Environment Rules** - Critical priority
2. **Security Best Practices** - Critical priority
3. **Code Quality Standards** - Critical priority
4. **Documentation Quality** - Critical priority (upgraded)
5. **Task Completion Requirements** - Critical priority

### **Intelligent Apply Rules** (5 rules)
1. **Backend General Rules** - Medium priority
2. **Frontend React Rules** - Medium priority
3. **Performance Optimization** - Medium priority
4. **Operational Directives** - Medium priority
5. **Component Templates** - Low priority

## 🎯 **Impact of Changes**

### **Enhanced Project Tracking**
- **Progress Visibility**: Clear tracking of completed tasks
- **Historical Record**: Complete history of agent work
- **Task Discovery**: New tasks identified during work
- **Timeline Tracking**: Completion timestamps for all work

### **Improved Documentation**
- **Current State**: All documentation reflects current project state
- **User Experience**: README.md always up-to-date
- **Consistency**: Documentation matches actual implementation
- **Completeness**: No outdated or missing documentation

### **Better Project Management**
- **Task Accountability**: Clear record of what was completed
- **Progress Monitoring**: Easy to track project progress
- **Quality Assurance**: Documentation quality maintained
- **Professional Standards**: Production-ready documentation

## 📝 **Implementation Notes**

### **Project Plan Structure**
- **Completion Timestamps**: When work was completed
- **Task Status**: Marked as "Completed"
- **Accomplishments**: Summary of what was done
- **Progress Updates**: Current project status
- **New Tasks**: Any tasks discovered during work

### **README.md Updates**
- **Feature Updates**: New capabilities added
- **Version Updates**: Version information if changed
- **Link Updates**: Ensure all links work
- **Instruction Updates**: Setup/installation changes
- **Content Accuracy**: Reflect current project state

### **Documentation Standards**
- **Consistency**: All docs reflect current state
- **Completeness**: No missing or outdated information
- **Accuracy**: Documentation matches implementation
- **Professional Quality**: Production-ready documentation

## 🚀 **Next Steps**

1. **Test Rule Application**: Verify project plan updates are made
2. **Monitor Documentation**: Ensure README.md stays current
3. **Quality Metrics**: Track documentation quality improvements
4. **User Feedback**: Monitor satisfaction with documentation

## 📋 **Compliance Checklist**

- [x] Task Completion Requirements updated with documentation requirements
- [x] Documentation Quality upgraded to Critical priority
- [x] Project plan update requirements defined
- [x] README.md update requirements defined
- [x] Other documentation update requirements defined
- [x] Rule classification updated
- [x] Completion verification process updated
- [x] Mandatory pre-completion checklist updated
- [x] Documentation standards established
