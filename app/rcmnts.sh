#!/bin/bash
# filepath: remove_comments.sh

# Check if directory path is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <directory_path>"
  exit 1
fi

DIR_PATH="$1"

# Process HTML files (<!-- comment -->)
find "$DIR_PATH" -name "*.html" -type f | while read file; do
  echo "Processing HTML file: $file"
  # Remove HTML comments (Note: This simple approach may have limitations with multi-line comments)
  sed -i '/<!--.*-->/d' "$file"
  # Normalize newlines: convert multiple empty lines to single newline
  sed -i '/^$/N;/^\n$/D' "$file"
done

# Process CSS files (/* comment */)
find "$DIR_PATH" -name "*.css" -type f | while read file; do
  echo "Processing CSS file: $file"
  # Remove single-line CSS comments
  sed -i '/\/\*.*\*\//d' "$file"
  # Normalize newlines
  sed -i '/^$/N;/^\n$/D' "$file"
done

# Process JavaScript files (// comment and /* comment */)
find "$DIR_PATH" -name "*.js" -type f | while read file; do
  echo "Processing JavaScript file: $file"
  # Remove JS single-line comments with //
  sed -i '/\/\/.*/d' "$file"
  # Remove JS single-line comments with /* */
  sed -i '/\/\*.*\*\//d' "$file"
  # Normalize newlines
  sed -i '/^$/N;/^\n$/D' "$file"
done

# Process Python files (# comment)
find "$DIR_PATH" -name "*.py" -type f | while read file; do
  echo "Processing Python file: $file"
  # Remove Python single-line comments
  sed -i '/^\s*#.*/d' "$file"
  # Normalize newlines
  sed -i '/^$/N;/^\n$/D' "$file"
done

echo "Comment removal and newline normalization complete!"