# 🧠 Conversation-analyser-django/Post Conversation Analysis

This Django project analyzes chat conversations between users and AI agents. It provides:

- API endpoints to upload and analyze conversations  
- Automated daily analysis via cron job or Celery  
- Database integration to store conversations, messages, and analysis results  

---

## ⚡ Features

1. Upload chat conversations via API  
2. Analyse conversations to compute clarity, relevance, sentiment, and more  
3. View analysis reports  
4. Daily automation to analyze new conversations  

---

## 📦 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/post-conversation-analysis.git
cd post-conversation-analysis
2. Create virtual environment
bash
Copy code
python -m venv myenv
myenv\Scripts\activate   # Windows
source myenv/bin/activate  # macOS/Linux
3. Install dependencies
bash
Copy code
pip install -r requirements.txt
4. Run migrations
bash
Copy code
python manage.py migrate
5. Start Django server
bash
Copy code
python manage.py runserver
Open http://127.0.0.1:8000/admin/ to see models in the admin panel.

🚀 API Endpoints
1. Upload Conversation
POST /api/conversations/

Request body:

json
Copy code
{
  "title": "Order chat 1",
  "messages": [
    {"sender": "user", "message": "Hi, I need help with my order."},
    {"sender": "ai", "message": "Sure, can you please share your order ID?"}
  ]
}
Response:

json
Copy code
{
  "id": 3,
  "title": "Order chat 1",
  "raw_json": { ... },
  "created_at": "2025-11-08T17:29:22.196698Z",
  "messages": [ ... ]
}
2. Analyse Conversation
POST /api/analyse/<conv_id>/

Trigger analysis for conversation with ID <conv_id>

Stores or updates ConversationAnalysis

3. View Analysis Reports
GET /api/reports/

Lists all conversation analysis results

4. Cron Job / Daily Task
Using Celery (recommended)
Run in separate terminals:

bash
Copy code
# Terminal 1: Django server
python manage.py runserver

# Terminal 2: Celery worker
celery -A post_conversation_analysis worker -l info

# Terminal 3: Celery Beat (scheduler)
celery -A post_conversation_analysis beat -l info
Using django-crontab (optional)
Add cron jobs in settings.py:

python
Copy code
CRONJOBS = [
    ('0 0 * * *', 'analysis.tasks.daily_analyse_new_conversations'),
]
Add cron jobs:

bash
Copy code
python manage.py crontab add
python manage.py crontab show
Remove cron jobs:

bash
Copy code
python manage.py crontab remove
5. Notes
Current analysis is heuristic-based; replace analysis_utils.perform_analysis with ML models or API calls for better accuracy

Use PostgreSQL in production; update DATABASES in settings and install psycopg2-binary

📌 Example curl commands
Upload conversation:

bash
Copy code
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
Trigger analysis:

bash
Copy code
curl -X POST http://127.0.0.1:8000/api/analyse/3/
Get reports:

bash
Copy code
curl http://127.0.0.1:8000/api/reports/
