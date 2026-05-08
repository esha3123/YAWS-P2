#!/bin/bash

# Set up logging
LOG_FILE="url_replacement.log"
echo "URL Replacement Log - $(date)" > "$LOG_FILE"

# Function to clean and normalize filenames
clean_filename() {
    local filename="$1"
    # Remove query parameters
    filename=$(echo "$filename" | sed 's/\?.*$//')
    # URL decode using Python
    decoded_filename=$(python3 -c "import urllib.parse; print(urllib.parse.unquote('$filename'))")
    echo "$decoded_filename"
}

# Function to search for files with flexible matching
find_file() {
    local filename="$1"
    local base_dir="./app/docs"
    
    # Try exact match first (case insensitive)
    local found_path=$(find "$base_dir" -type f -iname "$filename" 2>/dev/null | head -n 1)
    
    # If not found, try more flexible search by removing special characters
    if [ -z "$found_path" ]; then
        # Get filename without extension
        local basename=$(echo "$filename" | sed 's/\.[^.]*$//')
        local ext=$(echo "$filename" | grep -o '\.[^.]*$')
        
        # Simplify filename by removing special chars for search
        local simple_name=$(echo "$basename" | tr -d ',-')
        
        # Try partial match
        found_path=$(find "$base_dir" -type f -ipath "*$simple_name*$ext" 2>/dev/null | head -n 1)
    fi
    
    echo "$found_path"
}

# Find non-binary files with "https://saketcollege" URLs
find . -type f -print0 | xargs -0 grep -l "https://saketcollege" | xargs grep -I -l "https://saketcollege" | while read -r file; do
    echo "Processing file: $file" | tee -a "$LOG_FILE"
    
    # Create a temporary file for processing
    tmp_file=$(mktemp)
    cp "$file" "$tmp_file"
    
    # Extract URLs from the file
    grep -o 'https://saketcollege[^"'\''> ]*' "$file" | sort | uniq | while read -r url; do
        # Skip URLs without a filename or those ending with slash
        if [[ "$url" =~ /$ ]] || [[ ! "$url" =~ \.[a-zA-Z0-9]+($|\?) ]]; then
            echo "  Skipping URL without filename: $url" | tee -a "$LOG_FILE"
            continue
        fi
        
        # Extract the filename from URL (everything after the last slash)
        raw_filename=$(echo "$url" | sed 's|.*/||')
        
        # Skip empty filenames
        if [ -z "$raw_filename" ]; then
            echo "  Skipping empty filename from URL: $url" | tee -a "$LOG_FILE"
            continue
        fi
        
        # Clean and normalize the filename
        filename=$(clean_filename "$raw_filename")
        
        echo "  Looking for file: '$filename'" | tee -a "$LOG_FILE"
        
        # Find the file in the docs directory
        found_path=$(find_file "$filename")
        
        if [ -n "$found_path" ]; then
            # Extract the relative path from app/docs/
            relative_path=${found_path#./app/docs/}
            
            # Replace the URL in the file with the Flask template
            escaped_url=$(echo "$url" | sed 's/[\/&]/\\&/g') # Escape special chars
            sed -i "s|$escaped_url|{{ url_for('frontend.serve_docs', filepath='$relative_path') }}|g" "$tmp_file"
            
            echo "  SUCCESS: Replaced $url with filepath='$relative_path'" | tee -a "$LOG_FILE"
        else
            echo "  FAILED: No matching file found for: $filename from URL: $url" | tee -a "$LOG_FILE"
            
            # Additional debug info for troubleshooting
            basename=$(echo "$filename" | sed 's/\.[^.]*$//')
            echo "    Try searching manually: find ./app/docs -type f -iname \"*${basename}*\"" | tee -a "$LOG_FILE"
        fi
    done
    
    # Only replace the original file if changes were made
    if ! cmp -s "$file" "$tmp_file"; then
        cp "$tmp_file" "$file"
        echo "  File updated: $file" | tee -a "$LOG_FILE"
    else
        echo "  No changes made to: $file" | tee -a "$LOG_FILE"
    fi
    
    # Clean up
    rm "$tmp_file"
done

echo "Replacement complete. See $LOG_FILE for details."