#!/bin/bash

# Matrix Online Wiki Link Validator
# This script finds all markdown links and validates them

WIKI_DIR="/Users/pascaldisse/mxoemu_forum_scrape/wiki"
REPORT_FILE="$WIKI_DIR/link_validation_report.txt"
TEMP_LINKS="$WIKI_DIR/temp_all_links.txt"
TEMP_BROKEN="$WIKI_DIR/temp_broken_links.txt"

# Initialize counters
total_links=0
working_links=0
broken_links=0
broken_files=0
broken_dirs=0

# Clear temp files
> "$TEMP_LINKS"
> "$TEMP_BROKEN"
> "$REPORT_FILE"

echo "Matrix Online Wiki Link Validation Report" > "$REPORT_FILE"
echo "========================================" >> "$REPORT_FILE"
echo "Generated on: $(date)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Find all markdown files
echo "Finding all markdown files..."
md_files=$(find "$WIKI_DIR" -name "*.md" -type f | grep -v "temp_" | sort)
file_count=$(echo "$md_files" | wc -l)

echo "Found $file_count markdown files to scan" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Extract all markdown links
echo "Extracting all markdown links..."
while IFS= read -r file; do
    # Extract links in format [text](path)
    # This regex captures both file and directory links
    grep -o '\[[^]]*\]([^)]*\.md)' "$file" | sed 's/.*](\(.*\))/\1/' | while read -r link; do
        echo "$file|$link" >> "$TEMP_LINKS"
    done
    grep -o '\[[^]]*\]([^)]*/)' "$file" | sed 's/.*](\(.*\))/\1/' | while read -r link; do
        echo "$file|$link" >> "$TEMP_LINKS"
    done
done <<< "$md_files"

# Sort and count unique links
total_links=$(wc -l < "$TEMP_LINKS")
echo "Total links found: $total_links" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Validate each link
echo "Validating links..."
echo "BROKEN LINKS:" >> "$REPORT_FILE"
echo "=============" >> "$REPORT_FILE"

while IFS='|' read -r source_file link; do
    # Skip external links
    if [[ "$link" =~ ^https?:// ]] || [[ "$link" =~ ^mailto: ]]; then
        continue
    fi
    
    # Get the directory of the source file
    source_dir=$(dirname "$source_file")
    
    # Handle absolute vs relative links
    if [[ "$link" =~ ^/ ]]; then
        # Absolute link from wiki root
        full_path="$WIKI_DIR$link"
    else
        # Relative link
        full_path="$source_dir/$link"
    fi
    
    # Normalize path (resolve .. and .)
    full_path=$(cd "$source_dir" 2>/dev/null && cd "$(dirname "$full_path")" 2>/dev/null && pwd)/$(basename "$full_path")
    
    # Check if target exists
    if [[ -e "$full_path" ]]; then
        ((working_links++))
    else
        ((broken_links++))
        echo "$link|$source_file" >> "$TEMP_BROKEN"
        
        # Determine if it's a file or directory
        if [[ "$link" =~ \.md$ ]]; then
            ((broken_files++))
            echo "FILE: $link" >> "$REPORT_FILE"
            echo "  Source: $source_file" >> "$REPORT_FILE"
            echo "  Target: $full_path" >> "$REPORT_FILE"
        else
            ((broken_dirs++))
            echo "DIR:  $link" >> "$REPORT_FILE"
            echo "  Source: $source_file" >> "$REPORT_FILE"
            echo "  Target: $full_path" >> "$REPORT_FILE"
        fi
        echo "" >> "$REPORT_FILE"
    fi
done < "$TEMP_LINKS"

# Generate summary
echo "" >> "$REPORT_FILE"
echo "SUMMARY:" >> "$REPORT_FILE"
echo "========" >> "$REPORT_FILE"
echo "Total links scanned: $total_links" >> "$REPORT_FILE"
echo "Working links: $working_links" >> "$REPORT_FILE"
echo "Broken links: $broken_links" >> "$REPORT_FILE"
echo "  - Broken files (.md): $broken_files" >> "$REPORT_FILE"
echo "  - Broken directories: $broken_dirs" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Find most frequently broken links
if [[ -s "$TEMP_BROKEN" ]]; then
    echo "TOP 10 MOST FREQUENTLY BROKEN LINKS:" >> "$REPORT_FILE"
    echo "====================================" >> "$REPORT_FILE"
    cut -d'|' -f1 "$TEMP_BROKEN" | sort | uniq -c | sort -rn | head -10 | while read -r count link; do
        echo "  $count occurrences: $link" >> "$REPORT_FILE"
    done
    echo "" >> "$REPORT_FILE"
    
    # List files with most broken links
    echo "FILES WITH MOST BROKEN LINKS:" >> "$REPORT_FILE"
    echo "=============================" >> "$REPORT_FILE"
    cut -d'|' -f2 "$TEMP_BROKEN" | sort | uniq -c | sort -rn | head -10 | while read -r count file; do
        echo "  $count broken links in: $(basename "$file")" >> "$REPORT_FILE"
    done
fi

# Clean up temp files
rm -f "$TEMP_LINKS" "$TEMP_BROKEN"

echo ""
echo "Report saved to: $REPORT_FILE"