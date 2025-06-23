# YS_map

This project provides a Streamlit application for managing construction site locations. Data is stored in a Google Sheet rather than a local database.

## Setup

1. Create a Google service account and share your spreadsheet with the service account email.
2. Create a `secrets.toml` (or `.streamlit/secrets.toml` on Streamlit Cloud) containing your service account JSON and spreadsheet ID:
   ```toml
   [gcp]
   gcp_service_account = "{...service account JSON...}"
   spreadsheet_id = "<your spreadsheet id>"
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
