# Letterboxd Geographic Analyzer

A Python script that analyzes your exported Letterboxd data and categorizes every movie you've watched by its production country using the TMDB API.

## Features

- Bypasses Letterboxd's Pro-paywall for geographic statistics.
- Fixes BOM (`utf-8-sig`) encoding issues native to Letterboxd CSV exports.
- Secure execution: Prompts for API key at runtime to prevent accidental leaks.
- Real-time fetching with API rate-limit protections.

## Prerequisites

1. Python 3.x installed.
2. `requests` library installed:
   ```bash
   pip install requests
   ```
3. A free TMDB API Key (v3 auth).
