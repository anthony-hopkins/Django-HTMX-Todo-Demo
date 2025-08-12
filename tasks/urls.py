# Import the necessary Django modules
from django.urls import path  # For defining URL patterns
from . import views  # Import our view functions from the same directory

# =============================================================================
# URL PATTERNS - This tells Django which URLs go to which view functions
# =============================================================================
# 'app_name' creates a namespace for our URLs, so we can reference them like 'tasks:index'
app_name = 'tasks'

# This list defines all the URLs that our app handles
# Each 'path()' function takes 3 arguments:
# 1. The URL pattern (what the user types in their browser)
# 2. The view function to call when someone visits that URL
# 3. A name for the URL (so we can reference it in templates)
urlpatterns = [
    # Main page - when someone visits the root URL (/), show the index view
    path('', views.index, name='index'),
    
    # Add task - when someone submits the add task form, send it to add_task view
    # The URL will be something like /add/
    path('add/', views.add_task, name='add_task'),
    
    # Toggle task - when someone clicks a checkbox, toggle the task completion
    # The URL will be something like /toggle/5/ where 5 is the task ID
    # <int:task_id> means "capture a number and call it task_id"
    path('toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),
    
    # Delete task - when someone clicks delete, remove the task
    # The URL will be something like /delete/5/ where 5 is the task ID
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    
    # Edit task - when someone clicks edit, show an edit form
    # The URL will be something like /edit/5/ where 5 is the task ID
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    
    # Get stats - when HTMX needs to update the statistics section
    # The URL will be /stats/
    path('stats/', views.get_stats, name='get_stats'),
]
