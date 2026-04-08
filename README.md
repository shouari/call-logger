# Qualification d'appel SAV

A Streamlit application optimized for wide-screen UI, providing a fast and streamlined form for diagnosing and logging customer service (SAV) calls. It features a dual-column layout for rapid data entry and real-time map address autocompletion via OpenStreetMap.

## Features

- **Streamlined Diagnosis**: Two-column layout with easy-to-use inputs for systems (Audio, Video, Network, etc.), priority, and issues.
- **Address Autocomplete (OSM)**: Employs a custom Streamlit component to retrieve addresses and automatically calculates the billing zone distance based on coordinate proximity.
- **Dynamic Summaries**: Generates a quick text summary of the ticket and allows one-click copying to the clipboard.
- **Progress Tracking**: Tracks how complete the intake form is (progress bar on top).

## Project Structure

- `app.py`: The main Streamlit entry point.
- `osm_component/`: A custom Streamlit component consisting of an HTML interface for the interactive map and autocompletion lookup.
- `.streamlit/`: Contains the theme configurations (`config.toml`) for colors and appearance rules.

## Local Deployment Requirements

Make sure you have Python 3.9+ installed.

1. **Install Dependencies**
   It's recommended to deploy using a virtual environment:
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On Linux/Mac:
   source .venv/bin/activate
   ```
   Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run The Application**
   ```bash
   streamlit run app.py
   ```
   *The app will automatically launch in your default web browser.*
