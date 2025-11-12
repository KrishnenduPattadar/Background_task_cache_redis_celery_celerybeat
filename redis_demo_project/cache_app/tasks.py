# cache_app/tasks.py
from celery import shared_task
import time
from .models import Employee
import csv
from datetime import datetime , timedelta
from django.utils import timezone

@shared_task
def send_welcome_email_task(employee_name):
    """
    Simulates a slow task of sending a welcome email.
    This runs in the background on a Celery worker.
    """
    print(f"BACKGROUND TASK: Starting to send email to {employee_name}...")
    
    # Simulate a slow 5-second email connection
    time.sleep(5) 
    
    print(f"✅ BACKGROUND TASK: Email sent successfully to {employee_name}!")
    return f"Email sent to {employee_name}."



#adding new task for genareting employee report in CSV after specific time automatically

# @shared_task
# def generate_employee_report(): #mention in settings.py for report generation every 30 mins
#     """
#     Generates a CSV report of all employees.
#     """
#     print("⏰ (BEAT TASK): Starting employee report generation...")
    
#     # 1. Create a unique filename with a timestamp
#     timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     filename = f"employee_report_{timestamp}.csv"
    
#     # 2. Get the data from the database
#     #    (Using .values_list is efficient)
#     employees = Employee.objects.values_list('name', 'department', 'role')
    
#     # 3. Write to the CSV file
#     try:
#         with open(filename, 'w', newline='') as f:
#             writer = csv.writer(f)
#             # Write the header row
#             writer.writerow(['Name', 'Department', 'Role'])
#             # Write all the employee data
#             writer.writerows(employees)
            
#         print(f"✅ (BEAT TASK): Report generated successfully! Saved as {filename}")
#         return f"Report saved to {filename}"
        
#     except Exception as e:
#         print(f"❌ (BEAT TASK): Error generating report: {e}")
#         return f"Error: {e}"
    


# Django Task ➡️ Message Broker ➡️ Celery Worker ➡️ Result Backend


# Example Usage:

# --- ADD THIS NEW TASK ---

@shared_task
def generate_HOURLY_employee_report():
    """
    Generates a CSV report of employees created in the last 1 minute.
    """
    print("⏰ Generating hourly employee report...")
    now = timezone.now()
    one_minute_ago = now - timedelta(hours=1)

    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"NEW_1_MINUTE_report_{timestamp}.csv"

    # ✅ FIXED QUERY HERE
    employees = Employee.objects.filter(
        created_at__gte=one_minute_ago,
        created_at__lt=now
    ).values_list('name', 'department', 'role', 'created_at')

    try:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Department', 'Role', 'Created At'])
            writer.writerows(employees)

        print(f"✅ (BEAT TASK - 1 MIN): Found {len(employees)} new employees. Report saved! ({filename})")
        return f"Report saved to {filename}"

    except Exception as e:
        print(f"❌ (BEAT TASK - 1 MIN): Error: {e}")
        return f"Error: {e}"