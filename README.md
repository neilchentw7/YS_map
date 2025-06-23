# YS_map

This project provides a Streamlit application for managing construction site locations. Data is now stored in Google Firestore instead of a local SQLite database.

## Setup

1. Create a Firebase service account and download the JSON credentials file. **Keep this file outside of the repository**.
2. Copy `.env.example` to `.env` and update the value to point to your credentials file. The `.env` file is ignored by Git.
3. Load the environment variable before running the app:
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

When the application starts for the first time it will populate Firestore with data from `site_locations.csv` if the collection is empty.
