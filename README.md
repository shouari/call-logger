# Qualification d'appel SAV

A Streamlit application optimized for wide-screen UI, providing a fast and streamlined form for diagnosing and logging customer service (SAV) calls. It features a dual-column layout for rapid data entry, real-time map address autocompletion via OpenStreetMap, and automated URL parameter-based pre-filling designed for integration with **3CX**.

## Features

- **3CX Integration**: Automatically populates the Caller Name and Phone Number from URL parameters (`?phone=...&name=...`).
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

## Production Deployment (e.g., Streamlit Community Cloud)

1. Connect your GitHub repository to Streamlit Community Cloud.
2. Select your repository, branch, and set the main file path to `app.py`.
3. Advanced Configuration: 
   - No extra environment variables required at this stage.
4. Click **Deploy**. Theme settings will automatically be drawn from `.streamlit/config.toml`.

## Integrations

### 3CX Custom Integration
Configure your 3CX web application or desktop app to launch an external URL on an incoming call:
```text
https://<your-app-domain>/?phone=%CallerNumber%&name=%CallerName%
```
*(Variable names should match your 3CX environment capabilities).*
