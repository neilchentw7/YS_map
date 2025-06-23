# YS_map

This project provides a Streamlit application for managing construction site locations. Data is now stored in Google Firestore instead of a local SQLite database.

## Setup

1. Create a Firebase service account and download the JSON credentials file. **Keep this file outside of the repository**.
2. Copy `.env.example` to `.env` and update the value to point to your credentials file. The `.env` file is ignored by Git.
3. Load the environment variables before running the app:
   ```bash
   export $(cat .env | xargs)
   ```
4. (Optional) Instead of a file, you can set `FIREBASE_CREDENTIALS_B64` with a base64 encoded service account JSON.
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

When the application starts for the first time it will populate Firestore with data from `site_locations.csv` if the collection is empty.

### Streamlit Cloud

On Streamlit Cloud, add the following secret so the credential is not stored in the repository:

```
[general]
firebase_credentials_b64 = "<base64 of service account JSON>"
```

You can generate the base64 value with:

```bash
base64 -w0 /path/to/serviceAccountKey.json
```

The application will decode this secret at runtime.
