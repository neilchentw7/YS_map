# YS_map

This project provides a Streamlit application for managing construction site locations. Data is stored in a Google Sheet rather than a local database.

## Setup

1. Create a Google service account and share your spreadsheet with the service account email.
2. Copy `.env.example` to `.env` and add your service account JSON and spreadsheet ID. The `.env` file is ignored by Git.
3. Load the environment variables before running the app:
   ```bash
   export $(cat .env | xargs)
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

When the application starts for the first time it populates the Google Sheet with data from `site_locations.csv` if the sheet is empty.

### Streamlit Cloud

On Streamlit Cloud, store the credentials and spreadsheet ID as secrets so the service account file is not committed to the repository:

```
[gcp]
gcp_service_account = "{...service account JSON...}"
spreadsheet_id = "<your spreadsheet id>"
```

The application will read this secret at runtime.
