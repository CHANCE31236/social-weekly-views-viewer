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
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run

```powershell
.\.venv\Scripts\python.exe social_views_viewer.py
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

The build uses the same local `.venv`, installs `requirements-dev.txt`, runs the regression suite, and builds with PyInstaller. A failed install or test stops the build.

## Validation and local data

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

GitHub Actions runs these tests on Windows. The tests cover account loading and renaming, saved-data preservation, URL detection, numeric/date validation, and literal text in CSV/Excel exports. OCR accuracy and live dashboard reading require manual validation with the relevant platform.

An explicitly empty account list stays empty on restart. Malformed account or saved-view files produce a startup error so they can be corrected without replacing the existing data. Configuration writes use a temporary file followed by a replace.

CSV exports prefix formula-like text with an apostrophe; Excel exports store text as strings. Entered view counts must be non-negative, and the two report dates must be valid and ordered.
