# Social Weekly Views Viewer

A local Windows desktop app for collecting weekly social media view counts from visible creator dashboards.

The app is designed for general users: they add dashboard and public profile links, open the official platform pages, log in directly in the browser, then let the app read the visible weekly views value or enter it manually.

## Features

- Multi-account weekly views tracker.
- English, Chinese, and French interface.
- Automatic platform and account detection from dashboard/public URLs.
- Opens dashboard and public profile pages in Microsoft Edge.
- Reads visible dashboard values using copied page text or OCR fallback.
- TikTok-specific `Video views` detection to avoid confusing it with `Profile views`.
- Exports reports to CSV and Excel.
- No password prompts and no password storage.

## Security

This app never asks users to enter platform passwords. Users log in only on official social media websites opened in their browser.

Runtime files such as `accounts.json`, `data/`, `exports/`, and logs are ignored by git because they may contain local account links or report data.

## Requirements

- Windows
- Python 3.11 or newer
- Microsoft Edge

Install Python dependencies:

```powershell
pip install -r requirements.txt
```

## Run

```powershell
python social_views_viewer.py
```

On Windows, users can also run:

```powershell
.\run_social_viewer.bat
```

## Account Setup

1. Click `Add account`.
2. Paste the official dashboard/login URL.
3. Paste the public profile URL.
4. The app detects platform and account name automatically.
5. Open the dashboard, log in on the official site, and make the weekly views number visible.
6. Click `Read data`.

If automatic reading fails, type the weekly views value manually.

## Build EXE

```powershell
.\build_exe.bat
```

The build uses PyInstaller.
