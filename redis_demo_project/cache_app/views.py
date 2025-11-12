from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
import datetime
from .models import Employee


def cache_demo(request):
    current_time = cache.get('current_time')

    if not current_time:
        current_time = str(datetime.datetime.now())
        cache.set('current_time', current_time, 30)  # cache for 30 sec
        msg = "⏱ Cache miss → Stored new value!"
    else:
        msg = "✅ Cache hit → Loaded from Redis!"

    return HttpResponse(f"{msg}<br>Current Time: {current_time}")


def get_employee_list(request):
    cache_key = "employee_list"
    data = cache.get(cache_key)

    # Cache miss → Query DB
    if not data:
        print("🟡 Fetching from Database...")
        employees = list(Employee.objects.values('id', 'name', 'department', 'role'))
        data = {"employees": employees}

        # Store in cache for 10 minutes (600 seconds)
        cache.set(cache_key, data, timeout=600)
        massage = "⏱ Data fetched from DB and cached!"

    else:
        print("🟢 Loding from Redis Cache...")
        massage = "✅ Data loaded from Cache!"

    data['status'] = massage
    return JsonResponse(data)
