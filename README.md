Basic Structure: 
      ┌────────────┐
      │  Django     │  (creates employee / triggers task)
      └──────┬──────┘
             │
             ▼
      ┌────────────┐
      │   Redis     │  (acts as Message Broker + Result Backend)
      └──────┬──────┘
             │
   ┌─────────┴─────────┐
   │                   │
   ▼                   ▼
Celery Worker     Celery Beat
(Executes)        (Schedules tasks)



⚙️ PROJECT OVERVIEW

🧱 You have these main parts:

redis_demo_project/
│
├── redis_demo/          ← Django core settings + celery.py (main app)
│
├── cache_app/           ← App containing Employee model + tasks
│
├── db.sqlite3           ← Database
├── celerybeat-schedule  ← Celery Beat schedule metadata


🧩 Redis plays 3 roles here:

Message Broker → passes tasks from Django to Celery worker

Result Backend → stores task results

Cache Backend → used by Django’s cache system (if configured)

🧠 FLOW DIAGRAM — WHAT HAPPENS IN 3 TERMINALS

Let’s say you run:

🪟 Terminal 1 → Django server
python manage.py runserver


💡 Purpose:

Handles web requests (e.g., creating Employee)

Triggers Celery tasks (like send_welcome_email_task.delay("Lokesh"))

Django doesn’t process heavy jobs — it just pushes a message to Redis

💬 Flow:

User adds employee → Django pushes task → Redis broker

🪟 Terminal 2 → Celery Worker
celery -A redis_demo.celery:app worker -l info -P eventlet


💡 Purpose:

Listens to Redis for new jobs (tasks)

Executes tasks from cache_app/tasks.py

Saves results (if configured) to Redis result backend

💬 Flow:

Redis broker → Celery worker picks up task → Executes → Result saved


✅ Example:

Django: send_welcome_email_task.delay("Lokesh")
Redis: stores message queue
Celery Worker: picks it → runs → prints "✅ Email sent to Lokesh"

🪟 Terminal 3 → Celery Beat
celery -A redis_demo.celery:app beat -l info


💡 Purpose:

Works like a cron scheduler

Periodically triggers tasks automatically (e.g., every 1 minute)

💬 Flow:

Celery Beat → Sends scheduled job → Redis → Celery Worker → Executes task


✅ Example:

Every 1 min → Beat sends "generate_1_MINUTE_report"
Redis → Worker executes → Writes CSV file




🧰 FILE RESPONSIBILITY SUMMARY
File	Purpose
redis_demo/celery.py	Celery app setup, broker URLs
cache_app/tasks.py	Background jobs (email, report, etc.)
cache_app/models.py	Employee model (with created_at)
celerybeat-schedule.*	Stores last run time for beat tasks
db.sqlite3	Stores employee data
*.csv	Auto-generated reports
__pycache__/	Compiled Python cache files


🧩 When You Create an Employee (Full Flow)

You save a new Employee via Django view or shell

(Optional) signals.py triggers send_welcome_email_task.delay()

Django sends message → Redis broker

Celery Worker picks up → Sends fake email → Logs success

Every minute, Celery Beat triggers generate_1_MINUTE_report()

Worker executes → Queries DB for new employees → Writes to CSV file
                                        
                                        Author: @Krishnendu Pattadar
