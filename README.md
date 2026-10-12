# pocket04

`pocket04` is one storage partition in the Saidawan Radio music library. It holds audio files and related assets for a subset of the collection, and includes Python utilities and GitHub Actions workflows to retrieve audio from Telegram and maintain local metadata.

Repository: https://github.com/saidawan-radio/pocket04

## What this repository does

- Reads the canonical audio catalogue configured by `ORIGIN_DATA_FILE_PATH`.
- Tracks the last downloaded internal audio ID in its local downloaded-data JSON.
- Uses Telethon to retrieve the Telegram message associated with the next internal ID.
- Downloads the message's audio into the configured media directory.
- Adds a public GitHub Raw URL to the metadata so the web player can fetch the file directly.
- In repositories whose downloader includes cover support, also records a public cover-image URL.
- Includes a metadata update script that can copy newer title, performer, caption/message, and edit-date values from the source catalogue.

## Typical contents

| Path/file | Purpose |
|---|---|
| `musics/` | Stored audio files (the exact output format depends on the conversion workflow). |
| `covers/` | Cover images, where enabled. |
| `audio_downloader.py` | Main incremental download entry point. |
| `DownloadAudio.py` | Telegram message retrieval, media download, and GitHub Raw URL helpers. |
| `AudioDetail.py`, `FetchDetail.py` | Shared metadata parsing and JSON helpers, where present. |
| `dataupdate.py` | Updates stored metadata when source metadata is newer. |
| `config.py` | Reads environment-based configuration. |
| `downloaded.json` | Downloaded-track metadata and the last processed internal ID, if configured to this filename. |
| `.github/workflows/` | Automation for downloading tracks and refreshing metadata. |

## Configuration

The Python configuration reads environment variables such as:

- `API_ID`, `API_HASH`, `SESSION_STR`
- `CHANNEL_USERNAME`
- `ORIGIN_DATA_FILE_PATH`
- `DOWNLOADED_DATA_FILE_PATH`
- `DOWNLOAD_PATH`
- `DATE_FORMAT`, `DURATION_LIMIT`, `MIN_MSG_ID`
- `FILENAME_PATTERN`
- `REPO_OWNER`, `REPO_NAME`, `REPO_BRANCH`
- `COVER_PATH_DIR` (in versions with cover-image support)

Use repository/organization Actions secrets for Telegram credentials and session strings. Use variables for non-secret paths and repository settings where practical. Ensure `REPO_OWNER`, `REPO_NAME`, and `REPO_BRANCH` point to this pocket's actual public repository and branch.

## Local development

1. Create a Python virtual environment.
2. Install the packages listed in `requirements.txt`.
3. Set the required environment variables in a local `.env` file (never commit it).
4. Ensure the origin catalogue exists and has the expected `audio_info` and `general_info` structure.
5. Run the downloader only after checking the next internal ID and the configured output directory.

The workflow may also perform conversion, cover extraction, committing, or pushing. Check `.github/workflows/` and the shell scripts in this repository before assuming those steps happen automatically.

## How it connects to the radio

`audio-data` maintains Telegram-derived metadata. A pocket consumes that metadata, downloads media, and exposes it through a `raw.githubusercontent.com` URL. The static site in [`saidawan-radio.github.io`](https://github.com/saidawan-radio/saidawan-radio.github.io) can then play the file in a browser without a dedicated streaming backend.

## Important operational details

- Pockets are independent storage partitions. Keep each repository's download state and target URLs consistent.
- A downloader that processes only `last_downloaded_internal_id + 1` assumes IDs are sequential and that the next ID exists in the source catalogue. Check behavior when an ID is missing.
- Verify that the conversion workflow's output filename matches the URL written to metadata.
- Keep audio and artwork files within GitHub repository/storage limits; do not commit secrets or temporary session files.
- Make sure you have permission to redistribute the audio files.

## Version-specific note

The inspected downloader version for this pocket includes `add_cover_image_url_to_detail`, and its configuration includes `COVER_PATH_DIR`. Confirm the cover workflow and directory names in the current branch before changing them.
