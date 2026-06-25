#!/bin/bash

extensions=("*.mp3" "*.m4a" "*.ogg" "*.flac" "*.acc" "*.wav" "*.webm" "*.aiff")

mkdir -p ./temp

for ext in "${extensions[@]}"; do
    find "$DOWNLOAD_PATH" -iname "$ext" -exec sh -c '
        input="$1"
        temp="${input}.temp.opus"
        output="${input}.opus"

        ffmpeg -i ${input} -an -c:v copy -frames:v 1 -update 1 -y "./temp/$(basename ${input})cover.jpg" 2>/dev/null

         # Get bitrate in kbps
        br=$(ffprobe -v error -show_entries format=bit_rate -of default=noprint_wrappers=1:nokey=1 "$input")
        br_kbps=$((br / 1000))

        if [ "$br_kbps" -gt 128 ]; then
            target="128k"
        else
            target="${br_kbps}k"
        fi

        if ffmpeg -i "${input}" -c:a libopus -b:a "$target" -map_metadata 0 "$temp" 2>/dev/null; then
            mv -f "$temp" "$output"
            opustags -i -y --set-cover "./temp/$(basename ${input})cover.jpg" "${output}" 2>/dev/null
            rm -f "$input"
            echo "Converted: $input"
        else
            rm -f "$temp"
            echo "Failed: $input"
        fi
    ' _ {} \;

    if [ ! $? -eq 0 ]; then
        exit 1
    fi
done