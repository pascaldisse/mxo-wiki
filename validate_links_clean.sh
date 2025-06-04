#!/bin/bash

# Matrix Online Wiki Link Validator (Clean Version)
# This script finds all markdown links and validates them

WIKI_DIR="/Users/pascaldisse/mxoemu_forum_scrape/wiki"
REPORT_FILE="$WIKI_DIR/link_validation_clean_report.txt"
TEMP_LINKS="$WIKI_DIR/temp_all_links_clean.txt"
TEMP_BROKEN="$WIKI_DIR/temp_broken_links_clean.txt"

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

echo "Matrix Online Wiki Link Validation Report (Clean)" > "$REPORT_FILE"
echo "================================================" >> "$REPORT_FILE"
echo "Generated on: $(date)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Find all markdown files, excluding validation reports and temp files
echo "Finding all markdown files..."
md_files=$(find "$WIKI_DIR" -name "*.md" -type f | grep -v "LINK_VALIDATION" | grep -v "link_validation" | grep -v "temp_" | sort)
file_count=$(echo "$md_files" | wc -l)

echo "Found $file_count markdown files to scan" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Extract all markdown links
echo "Extracting all markdown links..."
while IFS= read -r file; do
    # Extract links in format [text](path)
    # This regex captures both file and directory links
    grep -o '\[[^]]*\]([^)]*\.md)' "$file" 2>/dev/null | sed 's/.*](\(.*\))/\1/' | while read -r link; do
        # Skip external links
        if [[ ! "$link" =~ ^https?:// ]] && [[ ! "$link" =~ ^mailto: ]]; then
            echo "$file|$link" >> "$TEMP_LINKS"
        fi
    done
    grep -o '\[[^]]*\]([^)]*/\s*)' "$file" 2>/dev/null | sed 's/.*](\(.*\))/\1/' | sed 's/\s*$//' | while read -r link; do
        # Skip external links
        if [[ ! "$link" =~ ^https?:// ]] && [[ ! "$link" =~ ^mailto: ]]; then
            echo "$file|$link" >> "$TEMP_LINKS"
        fi
    done
done <<< "$md_files"

# Sort and count unique links
total_links=$(wc -l < "$TEMP_LINKS" 2>/dev/null || echo 0)
echo "Total links found: $total_links" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Validate each link
echo "Validating links..."
echo "BROKEN LINKS:" >> "$REPORT_FILE"
echo "=============" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

broken_count=0
while IFS='|' read -r source_file link; do
    # Get the directory of the source file
    source_dir=$(dirname "$source_file")
    
    # Handle absolute vs relative links
    if [[ "$link" =~ ^/ ]]; then
        # Absolute link from wiki root
        full_path="$WIKI_DIR$link"
    else
        # Relative link - resolve from source directory
        # First normalize the path
        normalized_path=$(cd "$source_dir" 2>/dev/null && realpath -m "$link" 2>/dev/null || echo "$source_dir/$link")
        full_path="$normalized_path"
    fi
    
    # Check if target exists
    if [[ -e "$full_path" ]]; then
        ((working_links++))
    else
        ((broken_links++))
        ((broken_count++))
        echo "$link|$source_file" >> "$TEMP_BROKEN"
        
        # Determine if it's a file or directory
        if [[ "$link" =~ \.md$ ]]; then
            ((broken_files++))
            echo "[$broken_count] FILE: $link" >> "$REPORT_FILE"
        else
            ((broken_dirs++))
            echo "[$broken_count] DIR:  $link" >> "$REPORT_FILE"
        fi
        echo "    Source: $(basename "$source_file")" >> "$REPORT_FILE"
        echo "    Full Source Path: $source_file" >> "$REPORT_FILE"
        echo "    Expected Target: $full_path" >> "$REPORT_FILE"
        echo "" >> "$REPORT_FILE"
    fi
done < "$TEMP_LINKS"

# Generate summary
echo "" >> "$REPORT_FILE"
echo "SUMMARY:" >> "$REPORT_FILE"
echo "========" >> "$REPORT_FILE"
echo "Total markdown files scanned: $file_count" >> "$REPORT_FILE"
echo "Total links found: $total_links" >> "$REPORT_FILE"
echo "Working links: $working_links" >> "$REPORT_FILE"
echo "Broken links: $broken_links" >> "$REPORT_FILE"
echo "  - Broken file links (.md): $broken_files" >> "$REPORT_FILE"
echo "  - Broken directory links: $broken_dirs" >> "$REPORT_FILE"
percentage=$((working_links * 100 / (total_links > 0 ? total_links : 1)))
echo "  - Link health: ${percentage}%" >> "$REPORT_FILE"
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
        filename=$(basename "$file")
        dirname=$(basename "$(dirname "$file")")
        echo "  $count broken links in: $dirname/$filename" >> "$REPORT_FILE"
    done
    echo "" >> "$REPORT_FILE"
    
    # Group broken links by directory
    echo "BROKEN LINKS BY DIRECTORY:" >> "$REPORT_FILE"
    echo "==========================" >> "$REPORT_FILE"
    cut -d'|' -f1 "$TEMP_BROKEN" | sed 's|/[^/]*$||' | sort | uniq -c | sort -rn | while read -r count dir; do
        if [[ -n "$dir" ]]; then
            echo "  $count broken links to directory: $dir/" >> "$REPORT_FILE"
        fi
    done
fi

# Clean up temp files
rm -f "$TEMP_LINKS" "$TEMP_BROKEN"

echo ""
echo "Clean report saved to: $REPORT_FILE"
echo "Total files scanned: $file_count"
echo "Total broken links found: $broken_links"