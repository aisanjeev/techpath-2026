#!/bin/bash
# file-organizer.sh — Organize files in a folder by type
# Usage: ./file-organizer.sh /path/to/messy-folder
# Example: ./file-organizer.sh ~/Downloads

TARGET="${1:-.}"

if [ ! -d "$TARGET" ]; then
    echo "Error: '$TARGET' is not a valid directory"
    exit 1
fi

echo "Organizing files in: $TARGET"
echo "---"

# Counters
images=0
documents=0
code=0
videos=0
archives=0
audio=0

# Create category folders
mkdir -p "$TARGET/Images" "$TARGET/Documents" "$TARGET/Code" "$TARGET/Videos" "$TARGET/Archives" "$TARGET/Audio"

# Move files by extension
for file in "$TARGET"/*; do
    [ -f "$file" ] || continue

    filename=$(basename "$file")
    ext="${filename##*.}"
    ext_lower=$(echo "$ext" | tr '[:upper:]' '[:lower:]')

    case "$ext_lower" in
        jpg|jpeg|png|gif|svg|webp|bmp)
            mv "$file" "$TARGET/Images/" 2>/dev/null && ((images++))
            ;;
        pdf|doc|docx|xlsx|xls|pptx|ppt|txt|csv)
            mv "$file" "$TARGET/Documents/" 2>/dev/null && ((documents++))
            ;;
        py|js|html|css|java|cpp|c|sh|json|xml|yaml|yml|md)
            mv "$file" "$TARGET/Code/" 2>/dev/null && ((code++))
            ;;
        mp4|mkv|avi|mov|webm)
            mv "$file" "$TARGET/Videos/" 2>/dev/null && ((videos++))
            ;;
        zip|rar|7z|tar|gz)
            mv "$file" "$TARGET/Archives/" 2>/dev/null && ((archives++))
            ;;
        mp3|wav|flac|aac|ogg)
            mv "$file" "$TARGET/Audio/" 2>/dev/null && ((audio++))
            ;;
    esac
done

# Remove empty category folders
for dir in Images Documents Code Videos Archives Audio; do
    rmdir "$TARGET/$dir" 2>/dev/null
done

echo ""
echo "Done! Files organized:"
echo "  Images    : $images"
echo "  Documents : $documents"
echo "  Code      : $code"
echo "  Videos    : $videos"
echo "  Archives  : $archives"
echo "  Audio     : $audio"
echo "  Total     : $((images + documents + code + videos + archives + audio))"
