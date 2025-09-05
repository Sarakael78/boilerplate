#!/bin/bash
# Extract all "alwaysApply: true" rules for inclusion in external context

set -e

RULES_DIR=".cursor/rules"
OUTPUT_FILE="always-apply-rules.json"

echo "Extracting always-apply rules..."

# Find all .mdc files with alwaysApply: true
ALWAYS_APPLY_FILES=$(find "$RULES_DIR" -name "*.mdc" -exec grep -l "alwaysApply: true" {} \;)

# Start JSON structure
echo '[' >"$OUTPUT_FILE"

FIRST=true
for rule_file in $ALWAYS_APPLY_FILES; do
	if [ "$FIRST" = false ]; then
		echo ',' >>"$OUTPUT_FILE"
	fi
	FIRST=false

	# Get full path
	FULL_PATH=$(realpath "$rule_file")

	# Extract content
	CONTENT=$(cat "$rule_file" | jq -Rs .)

	# Add to JSON
	cat >>"$OUTPUT_FILE" <<JSON_BLOCK
  {
    "document_type": "RULE",
    "document_id": "$FULL_PATH",
    "rule_content": $CONTENT
  }
JSON_BLOCK
done

echo ']' >>"$OUTPUT_FILE"

echo "Always-apply rules extracted to: $OUTPUT_FILE"
echo "Found rules:"
echo "$ALWAYS_APPLY_FILES"
