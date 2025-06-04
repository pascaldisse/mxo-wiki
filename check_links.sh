#\!/bin/bash

# Initialize counters
total_links=0
working_links=0
broken_links=0
declare -A broken_link_counts
declare -A broken_files
declare -A broken_dirs

# Find all markdown files
while IFS= read -r file; do
    # Extract markdown links [text](path)
    grep -oE '\[([^\]]+)\]\(([^)]+)\)' "$file" | while IFS= read -r match; do
        # Extract the link path
        link=$(echo "$match" | sed -E 's/\[[^\]]+\]\(([^)]+)\)/\1/')
        
        # Skip external links, anchors, and empty links
        if [[ "$link" =~ ^https?:// ]] || [[ "$link" =~ ^# ]] || [[ -z "$link" ]]; then
            continue
        fi
        
        # Remove any anchor from the link
        link=${link%%#*}
        
        # Skip if empty after removing anchor
        if [[ -z "$link" ]]; then
            continue
        fi
        
        total_links=$((total_links + 1))
        
        # Get the directory of the current file
        file_dir=$(dirname "$file")
        
        # Resolve the link path relative to the file location
        if [[ "$link" =~ ^/ ]]; then
            # Absolute path from wiki root
            target="/Users/pascaldisse/mxoemu_forum_scrape/wiki${link}"
        else
            # Relative path
            target="$file_dir/$link"
        fi
        
        # Normalize the path
        target=$(cd "$(dirname "$target")" 2>/dev/null && pwd)/$(basename "$target") 2>/dev/null || echo "$target")
        
        # Check if target exists
        if [[ -e "$target" ]]; then
            working_links=$((working_links + 1))
        else
            broken_links=$((broken_links + 1))
            broken_link_counts["$link"]=$((${broken_link_counts["$link"]:-0} + 1))
            
            # Categorize as file or directory
            if [[ "$link" =~ /$ ]]; then
                broken_dirs["$link"]=$((${broken_dirs["$link"]:-0} + 1))
            else
                broken_files["$link"]=$((${broken_files["$link"]:-0} + 1))
            fi
            
            echo "BROKEN: $file -> $link"
        fi
    done
done < <(find /Users/pascaldisse/mxoemu_forum_scrape/wiki -name "*.md" -type f)

# Generate report
echo -e "\n\n=== LINK VALIDATION REPORT ==="
echo "Total links found: $total_links"
echo "Working links: $working_links"
echo "Broken links: $broken_links"
if [[ $total_links -gt 0 ]]; then
    health=$(echo "scale=1; ($working_links * 100) / $total_links" | bc)
    echo "Wiki health: ${health}%"
fi

echo -e "\n=== BROKEN LINK CATEGORIES ==="
echo "Missing files: ${#broken_files[@]}"
echo "Missing directories: ${#broken_dirs[@]}"

echo -e "\n=== TOP 10 MOST FREQUENTLY BROKEN LINKS ==="
for link in "${\!broken_link_counts[@]}"; do
    echo "${broken_link_counts[$link]} $link"
done | sort -rn | head -10

