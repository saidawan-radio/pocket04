#!/bin/bash

# Path to your Python script
PYTHON_SCRIPT="./audio_downloader.py"

# Function to get directory size in MB
get_directory_size_mb() {
    local dir="$1"
    # Using du to get size in MB (--apparent-size for accurate file sizes)
    # -b for bytes, then convert to MB
    local size_bytes=$(du -sb "$dir" | cut -f1)
    local size_mb=$((size_bytes / 1024 / 1024))
    echo "$size_mb"
}

# Check if directory exists
if [ ! -d "$DOWNLOAD_PATH" ]; then
    echo "Error: Directory '$DOWNLOAD_PATH' does not exist"
    mkdir -p ./${DOWNLOAD_PATH}
fi

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Error: Python script '$PYTHON_SCRIPT' does not exist"
    exit 1
fi

# Get directory size
DIR_SIZE=$(get_directory_size_mb "$DOWNLOAD_PATH")

echo "Directory size: ${DIR_SIZE}MB"
echo "Threshold: ${DATA_FETCH_SIZE_LIMIT}MB"

# Check if size exceeds threshold
if [ "$DIR_SIZE" -lt "$DATA_FETCH_SIZE_LIMIT" ]; then
    echo "Directory size exceeds ${DATA_FETCH_SIZE_LIMIT}MB. Running Python script twice..."
    
    # Run Python script to download audio twice
    echo "Run 1:"
    python3 "$PYTHON_SCRIPT"
    if [ ! $? -eq 0 ]; then
        exit 1
    fi
    
    echo "Run 2:"
    python3 "$PYTHON_SCRIPT"
    if [ ! $? -eq 0 ]; then
        exit 1
    fi

    echo "Run 3:"
    python3 "$PYTHON_SCRIPT"
    if [ ! $? -eq 0 ]; then
        exit 1
    fi
    
    echo "Script execution completed."
else
    echo "Directory size is within limits. No action taken."
fi
