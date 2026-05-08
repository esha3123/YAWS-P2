#!/bin/bash

# Set up logging
LOG_FILE="url_replacement_special.log"
echo "Special URL Replacement Log - $(date)" > "$LOG_FILE"

# Function to replace URLs in files
replace_url() {
    local file="$1"
    local old_url="$2"
    local new_path="$3"
    
    escaped_url=$(echo "$old_url" | sed 's/[\/&]/\\&/g')
    sed -i "s|$escaped_url|{{ url_for('frontend.serve_docs', filepath='$new_path') }}|g" "$file"
    echo "Replaced: $old_url → filepath='$new_path'" | tee -a "$LOG_FILE"
}

# Special case replacements based on our findings
echo "Processing special cases..." | tee -a "$LOG_FILE"

# 1. Academic Calendars
find ./app/templates -type f -exec grep -l "Academic.*Calendar.*2019-20" {} \; | while read -r file; do
    replace_url "$file" "https://saketcollege.edu.in/Docs/Academic/Academic%20Calendar/Academic%20Calendar%202019-20.pdf.*" "academics/calendar/2019-20.pdf"
done

find ./app/templates -type f -exec grep -l "Academic.*Calendar.*2020-21" {} \; | while read -r file; do
    replace_url "$file" "https://saketcollege.edu.in/Docs/Academic/Academic%20Calendar/Academic%20Calendar%202020-21.pdf.*" "academics/calendar/2020-21.pdf"
done

find ./app/templates -type f -exec grep -l "Academic.*Calendar.*2021-22" {} \; | while read -r file; do
    replace_url "$file" "https://saketcollege.edu.in/Docs/Academic/Academic%20Calendar/Academic%20Calendar%202021-22.pdf.*" "academics/calendar/2021-22.pdf"
done

find ./app/templates -type f -exec grep -l "Academic.*Calendar.*2022-23" {} \; | while read -r file; do
    replace_url "$file" "https://saketcollege.edu.in/Docs/Academic/Academic%20Calendar/Academic%20Calendar%202022-23.pdf.*" "academics/calendar/2022-23.pdf"
done

find ./app/templates -type f -exec grep -l "Acadmeic.*Calender.*2024-25" {} \; | while read -r file; do
    replace_url "$file" "https://saketcollege.edu.in/Docs/Academic/Academic%20Calendar/Acadmeic%20Calender%202024-25.pdf.*" "academics/calendar/2024-25.pdf"
done

# 2. Strategic Plan
find ./app/templates -type f -exec grep -l "6.2.1.*Startgic.*plan" {} \; | while read -r file; do
    replace_url "$file" "https://saketcollege.edu.in/Docs/IQAC/6.2.1%20Startgic%20plan.pdf.*" "misc/6.2.1 Startgic plan.pdf"
done

# 3. Banking and Insurance, Accounting and Finance programs
find ./app/templates -type f -exec grep -l "Banking.*Insurance" {} \; | while read -r file; do
    grep -o 'https://saketcollege[^"'\''> ]*Banking[^"'\''> ]*Insurance[^"'\''> ]*' "$file" | while read -r url; do
        # Try to find a matching file
        potential_files=$(find ./app/docs -type f -ipath "*banking*insurance*.pdf")
        if [ -n "$potential_files" ]; then
            first_match=$(echo "$potential_files" | head -n1)
            relative_path=${first_match#./app/docs/}
            replace_url "$file" "$url" "$relative_path"
        else
            echo "No match found for Banking and Insurance: $url" | tee -a "$LOG_FILE"
        fi
    done
done

find ./app/templates -type f -exec grep -l "Accounting.*Finance" {} \; | while read -r file; do
    grep -o 'https://saketcollege[^"'\''> ]*Accounting[^"'\''> ]*Finance[^"'\''> ]*' "$file" | while read -r url; do
        # Try to find a matching file
        potential_files=$(find ./app/docs -type f -ipath "*accounting*finance*.pdf")
        if [ -n "$potential_files" ]; then
            first_match=$(echo "$potential_files" | head -n1)
            relative_path=${first_match#./app/docs/}
            replace_url "$file" "$url" "$relative_path"
        else
            echo "No match found for Accounting and Finance: $url" | tee -a "$LOG_FILE"
        fi
    done
done

# 4. Activity files
for activity in "GreenClub" "SportsActivities" "CulturalEvents"; do
    find ./app/templates -type f -exec grep -l "$activity" {} \; | while read -r file; do
        grep -o "https://saketcollege[^\"'> ]*$activity[^\"'> ]*" "$file" | while read -r url; do
            # Try to find a matching file
            potential_files=$(find ./app/docs -type f -ipath "*$activity*.pdf")
            if [ -n "$potential_files" ]; then
                first_match=$(echo "$potential_files" | head -n1)
                relative_path=${first_match#./app/docs/}
                replace_url "$file" "$url" "$relative_path"
            else
                # Create a placeholder message for missing activities
                echo "No match found for $activity: $url" | tee -a "$LOG_FILE"
            fi
        done
    done
done

echo "Special replacements complete. See $LOG_FILE for details." | tee -a "$LOG_FILE"