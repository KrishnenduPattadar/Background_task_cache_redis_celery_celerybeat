# import sys  # <-- Add this import
# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from django.core.cache import cache
# from .models import Employee

# # 👇 Add this print statement right here

# print("✅✅✅ DEBUG: cache_app.signals.py file was imported! Krish ✅✅✅")

# print(r"""
# ██╗ ██╗  ██████╗  ██████╗  ██████╗ ██╗ ██╗
# ██║██╔╝  ██╔══██╗ ╚═╗██╔═╝ ██╔════╝██║ ██╔╝
# ████╔╝   ██████╔╝    ██║  ╚█████╗  ██████╔╝ 
# ██║██╗   ██╔═██╗     ██║  ╚════██║ ██╔═██╗ 
# ██║ ╚██╗ ██║  ██╗ ╔═╝██╚═╗ ██████╔╝██║ ██╗
# ╚═╝  ╚═╝ ╚═╝  ╚═╝ ╚═════╝ ╚═════╝  ╚═╝  ╚═╝""", file=sys.stderr)

# @receiver([post_save, post_delete], sender=Employee)
# def clear_employee_cache(sender, **kwargs):
#     cache.delete('employee_list')
#     # Add file=sys.stderr to this print statement 👇
#     print("🧹 Cache cleared due to Employee DB change!", file=sys.stderr)



# # this for Celery
# # cache_app/signals.py
# import sys
# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from django.core.cache import cache
# from .models import Employee
# from .tasks import send_welcome_email_task  # <-- Import your new task

# print("✅✅✅ DEBUG: cache_app.signals.py file was imported! ✅✅✅", file=sys.stderr)

# @receiver(post_save, sender=Employee)
# def employee_post_save_handler(sender, instance, created, **kwargs):
#     """
#     Handles actions AFTER an Employee is saved.
#     """
#     # 1. Clear the cache every time
#     print("🧹 Cache cleared due to Employee save!", file=sys.stderr)
#     cache.delete('employee_list')
    
#     # 2. If this is a NEW employee, call the background task
#     if created:
#         print("➡️ Sending welcome email task to Celery...", file=sys.stderr)
#         # This .delay() command is INSTANT.
#         # It just adds the job to the Redis queue.
#         send_welcome_email_task.delay(instance.name)

# @receiver(post_delete, sender=Employee)
# def employee_post_delete_handler(sender, instance, **kwargs):
#     """
#     Handles actions AFTER an Employee is deleted.
#     """
#     # 1. Just clear the cache
#     print("🧹 Cache cleared due to Employee delete!", file=sys.stderr)
#     cache.delete('employee_list')




# cache_app/signals.py
import sys
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Employee

# DO NOT import from .tasks here! This is what causes the circular import.

# --- Your Debug Print ---
print("✅✅✅ DEBUG: cache_app.signals.py file was imported! Krish ✅✅✅")
print(r"""
██╗ ██╗  ██████╗  ██████╗  ██████╗ ██╗ ██╗
██║██╔╝  ██╔══██╗ ╚═╗██╔═╝ ██╔════╝██║ ██╔╝
████╔╝   ██████╔╝    ██║  ╚█████╗  ██████╔╝ 
██║██╗   ██╔═██╗     ██║  ╚════██║ ██╔═██╗ 
██║ ╚██╗ ██║  ██╗ ╔═╝██╚═╗ ██████╔╝██║ ██╗
╚═╝  ╚═╝ ╚═╝  ╚═╝ ╚═════╝ ╚═════╝  ╚═╝  ╚═╝""", file=sys.stderr)
# --- End Debug Print ---


# --- NEW CELERY-ENABLED HANDLERS ---

@receiver(post_save, sender=Employee)
def employee_post_save_handler(sender, instance, created, **kwargs):
    """
    Handles actions AFTER an Employee is saved.
    This replaces your old 'clear_employee_cache' function.
    """
    
    # 1. Clear the cache every time
    print("🧹 Cache cleared due to Employee save!", file=sys.stderr)
    cache.delete('employee_list')
    
    # 2. If this is a NEW employee, call the background task
    if created:
        print("➡️ Sending welcome email task to Celery...", file=sys.stderr)
        
        # --- THIS IS THE FIX ---
        # Import the task *inside* the function to avoid the circular import error
        from .tasks import send_welcome_email_task
        # -----------------------

        send_welcome_email_task.delay(instance.name)

@receiver(post_delete, sender=Employee)
def employee_post_delete_handler(sender, instance, **kwargs):
    """
    Handles actions AFTER an Employee is deleted.
    """
    # 1. Just clear the cache
    print("🧹 Cache cleared due to Employee delete!", file=sys.stderr)
    cache.delete('employee_list')
    