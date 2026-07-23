# AstraSim Mobile — Clean Rebuild

This is a clean, mobile-first Streamlit deployment package.

## Included files

- `app.py` — mobile-friendly interface
- `rocket_model.pkl` — saved XGBoost preprocessing and prediction pipeline
- `model_metadata.json` — variable ranges and dropdown options
- `requirements.txt` — deployment dependencies

## Deploy from scratch

1. Create a **new GitHub repository** named `AstraSim-Mobile`.
2. Upload all four files listed above directly to the repository.
3. Open Streamlit Community Cloud and create a new app.
4. Select the new repository.
5. Enter `app.py` as the main file path.
6. Deploy.

The app keeps the main variables easy to reach on a phone, places advanced variables in one expandable section, and displays the rocket animation immediately after the test button.
