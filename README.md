# CheckChesser Backend

Django REST API for CheckChesser.

---

## Requirements

- Python 3.10+
- pip
- Virtual environment (recommended)
- Internet access (for USCF API requests)

---

## Setup

1. Clone the repository:
   git clone https://github.com/redcomp16/checkchesser.git
   cd checkchesser

2. Create and activate a virtual environment:

   Windows (PowerShell):
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   
   macOS/Linux:
   source venv/bin/activate

4. Install dependencies:
   pip install -r requirements.txt

5. Make migrations (optional, if using the database):
   python manage.py migrate

6. Run the development server:
   python manage.py runserver

Server will run on http://localhost:8000

---

## API Endpoints

### Home
GET /
Returns a simple HTML message indicating the backend is running.

### Players
GET /api/players/
Returns a JSON list of players loaded from players/players.csv.

Optional query parameters:
- name -> filter by first or last name (starts with)
- min_rating -> filter by minimum live rating
- max_rating -> filter by maximum live rating
- school -> filter by school name
- grade -> filter by grade number

Example:
GET /api/players/?name=Smith&min_rating=1500

---

## Notes

- players.csv must be inside the players/ folder.
- Ratings are fetched live from the USCF API, which may slow down requests.
- For production, consider caching ratings or pre-loading them to improve performance.
- Use relative imports within the players app to avoid import errors:
  from .player import Player
  from .uscf_service import USCF_Service
- Always run commands from the repo root (checkchesser/), not inside backend/.
