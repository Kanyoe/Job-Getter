# Job-Getter

## Setup

1. Clone this repo
2. Create and activate a Python 3.10+ virtual environment
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the server:
   ```
   uvicorn app.main:app --reload
   ```

## Endpoints

- `POST /profile/` → Create user profile
- `POST /resume/{user_id}` → Upload and parse resume PDF
- `POST /preferences/{user_id}` → Save job search preferences