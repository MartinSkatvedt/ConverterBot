# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A Discord bot that watches messages for `.webm` attachments (which don't render on Discord mobile) and automatically replies with an `.mp4` conversion. Built on `discord.py` and `moviepy` (ffmpeg under the hood).

## Commands

```bash
# Install dependencies (Python 3.9)
pip install -r src/requirements.txt

# Run the bot locally (requires a .env file at repo root — see .env.example)
cd src && python main.py

# Run via docker-compose (also starts watchtower for auto-updates)
docker-compose up -d
```

There is no test suite, linter, or build step beyond the Docker image.

## Environment

The bot reads three variables from `.env` (loaded via `python-dotenv`):
- `DISCORD_TOKEN` — bot token from the Discord developer portal
- `LOADING_MESSAGE` — text shown while converting
- `COMPLETE_MESSAGE` — text shown on the final converted message

`intents.message_content` is enabled and must also be turned on in the Discord developer portal, or the bot won't see attachments.

## Architecture

Two files in `src/`:

- **`main.py`** — the `ConverterBot(discord.Client)` event loop. On each message it scans attachments for `.webm` in the URL, then runs a three-step UX flow:
  1. `init_conversion` posts a *new* loading message with `assets/loading.gif`.
  2. `convert_webm_to_mp4` (blocking) downloads and transcodes.
  3. `conversion_complete` **edits that loading message in place**, swapping the gif attachment for the finished `.mp4`.
- **`utils.py`** — `convert_webm_to_mp4` downloads the file to `./tmp/<basename>/input.webm`, transcodes to `output.mp4` (`libx264` / `aac`), and returns `(output_path, parent_dir)`. `clean_up_files` then deletes both files and the per-conversion directory.

Key things to know:
- Each conversion gets its own `./tmp/<filename>/` directory, created and torn down per message — relied on for concurrency isolation.
- `convert_webm_to_mp4` is **synchronous and blocking** inside an async handler, so it stalls the event loop during transcode. Keep this in mind before parallelizing or adding features.
- `clean_up_files` assumes the exact `input.webm`/`output.mp4` names; if a conversion fails partway, leftover files in `./tmp/` are not cleaned.

## Deployment

`.github/workflows/main.yml` builds and pushes the Docker image to `ghcr.io/martinskatvedt/converterbot` **on GitHub release publish** (not on push). The compose file pulls `:latest` and uses watchtower (30-min poll) to auto-redeploy when a new image is published.
