# YS_map

This project provides a Streamlit application for managing construction site locations. Data is stored in a Google Sheet rather than a local database.

## Setup

1. Create a Google Sheet and set its sharing permissions to **Anyone with the link can edit**.
2. Store the sheet URL in `GSHEET_URL` or add it to `.streamlit/secrets.toml` under `public_gsheet_url`.
   If no URL is provided the app falls back to a read-only sample sheet.
   You can use the example sheet below:
   ```
   https://docs.google.com/spreadsheets/d/1VV2AXV7-ZudWApvRiuKW8gcehXOM1CaPXGyHyFvDPQE/edit?gid=0
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

When the application starts for the first time it populates the Google Sheet with data from `site_locations.csv` if the sheet is empty.

### Streamlit Cloud

On Streamlit Cloud, create `.streamlit/secrets.toml` with the following content so the Sheet URL isn't committed to the repository:

```
public_gsheet_url = "https://docs.google.com/spreadsheets/d/1VV2AXV7-ZudWApvRiuKW8gcehXOM1CaPXGyHyFvDPQE/edit?gid=0"
```

The application will read this secret at runtime.
When the sample sheet is used, write operations are disabled and you'll see a warning.
