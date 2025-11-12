from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Employee model.
    """
    
    # Fields to display in the main list view
    list_display = ('name', 'department', 'role')
    
    # Fields that can be edited directly in the list view
    # Note: 'name' is left out as it's the link to the detail page
    list_editable = ('department', 'role')
    
    # Adds a search bar to search these fields
    search_fields = ('name', 'department')
    
    # Adds a filter sidebar for these fields
    list_filter = ('department', 'role')
    
    # How many items to show per page
    list_per_page = 20