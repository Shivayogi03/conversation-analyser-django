# Post-Conversation Analysis (Kipps.AI Internship Assignment)

## Overview
Django + DRF app that accepts conversation JSON, analyses conversation using configurable heuristics, stores results in DB, and runs daily automated analysis.

## Setup (SQLite - quick)
1. Clone repo
2. Create virtualenv:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

markdown
Copy code
3. Apply migrations:
python manage.py migrate
python manage.py createsuperuser

markdown
Copy code
4. Run server:
python manage.py runserver

arduino
Copy code

## API
- `POST /api/conversations/` — Upload conversation (JSON)
Example:
```json
{
 "title":"Order chat 1",
 "messages":[
   {"sender":"user","message":"Hi, I need help with my order."},
   {"sender":"ai","message":"Sure, can you please share your order ID?"},
   {"sender":"user","message":"It's 12345."},
   {"sender":"ai","message":"Thanks! Your order has been shipped and will arrive tomorrow."}
 ]
}
POST /api/analyse/<conv_id>/ — Trigger analysis on conversation with id <conv_id> (stores/updates analysis)

GET /api/reports/ — List all conversation analysis results.

Cron job (django-crontab)
Ensure django-crontab is in INSTALLED_APPS and CRONJOBS set in settings.

Add cron jobs:

sql
Copy code
python manage.py crontab add
python manage.py crontab show
To remove:

arduino
Copy code
python manage.py crontab remove
Celery (optional)
Start redis/broker, run celery worker and beat:

nginx
Copy code
celery -A post_conversation_analysis worker -l info
celery -A post_conversation_analysis beat -l info
Notes
The current analysis is heuristic-based; you can replace analysis_utils.perform_analysis with ML models / API calls for better accuracy.

Use PostgreSQL in production — update DATABASES in settings and install psycopg2-binary.

cpp
Copy code

---

# 11 — Test with curl examples

1. Upload conversation:
```bash
curl -X POST http://127.0.0.1:8000/api/conversations/ \
  -H "Content-Type: application/json" \
  -d '{
    "title":"Order chat 1",
    "messages":[
      {"sender":"user","message":"Hi, I need help with my order."},
      {"sender":"ai","message":"Sure, can you please share your order ID?"},
      {"sender":"user","message":"It'\''s 12345."},
      {"sender":"ai","message":"Thanks! Your order has been shipped and will arrive tomorrow."}
    ]
  }'
Trigger analysis (replace 1 with the actual conversation id):

bash
Copy code
curl -X POST http://127.0.0.1:8000/api/analyse/1/
Get reports:

bash
Copy code
curl http://127.0.0.1:8000/api/reports/