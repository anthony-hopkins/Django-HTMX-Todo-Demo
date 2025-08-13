# Import the necessary Django modules
from django.shortcuts import render  # For rendering HTML templates
from django.http import HttpResponse  # For sending HTTP responses

import json  # For handling JSON data (though we're not using it much in this simple example)

# =============================================================================
# DATA STORAGE - In a real app, you'd use a database
# =============================================================================
# This is a simple list stored in memory (RAM). When you restart the server, 
# all tasks will disappear! This is just for learning purposes.
tasks_list = [
    {"id": 1, "text": "Learn HTMX basics", "completed": False},
    {"id": 2, "text": "Build a simple to-do app", "completed": True},
    {"id": 3, "text": "Understand Django + HTMX integration", "completed": False},
]

# Keep track of the next available ID for new tasks
# In a real app, the database would handle this automatically
next_id = 4

# =============================================================================
# VIEW FUNCTIONS - These handle HTTP requests and return responses
# =============================================================================

def index(request):
    """
    This is the main page view function.
    
    When someone visits your website, Django calls this function.
    The 'request' parameter contains information about the HTTP request.
    
    This function renders the 'index.html' template and passes the tasks list to it.
    """
    # 'render' takes 3 arguments:
    # 1. the request object
    # 2. the template name (looks in tasks/templates/tasks/index.html)
    # 3. a dictionary of data to pass to the template
    return render(request, 'tasks/index.html', {'tasks': tasks_list})

def add_task(request):
    """
    This function handles adding new tasks via HTMX.
    
    HTMX sends a POST request to this URL when someone submits the add task form.
    We extract the task text from the form data and create a new task.
    """
    global next_id  # We need to modify the global variable
    
    # Check if this is a POST request (form submission)
    if request.method == 'POST':
        # Get the task text from the form data
        # 'request.POST' contains all the form fields
        # 'get()' safely gets the value, with an empty string as default if not found
        task_text = request.POST.get('task_text', '').strip()
        
        # Only create a task if there's actual text (not just spaces)
        if task_text:
            # Create a new task dictionary
            new_task = {
                "id": next_id,           # Give it a unique ID
                "text": task_text,       # The actual task text
                "completed": False       # New tasks start as incomplete
            }
            
            # Add the new task to our list
            tasks_list.append(new_task)
            
            # Increment the ID counter for the next task
            next_id += 1
            
            # Return the HTML for just the new task item
            # HTMX will insert this into the page without refreshing
            return render(request, 'tasks/task_item.html', {'task': new_task})
    
    # If it's not a POST request or no text was provided, return nothing
    return HttpResponse("")

def toggle_task(request, task_id):
    """
    This function toggles a task between completed and incomplete.
    
    When someone clicks a checkbox, HTMX sends a POST request here.
    We find the task by ID and flip its completed status.
    """
    # Loop through all tasks to find the one with the matching ID
    for task in tasks_list:
        if task["id"] == task_id:
            # Flip the completed status (True becomes False, False becomes True)
            task["completed"] = not task["completed"]
            
            # Return the updated task HTML so HTMX can update the page
            return render(request, 'tasks/task_item.html', {'task': task})
    
    # If no task was found, return nothing
    return HttpResponse("")

def delete_task(request, task_id):
    """
    This function deletes a task.
    
    When someone clicks the delete button, HTMX sends a POST request here.
    We remove the task from our list and return nothing (which removes it from the page).
    """
    global tasks_list  # We need to modify the global variable
    
    # Filter out the task with the matching ID
    # This creates a new list with all tasks EXCEPT the one we want to delete
    tasks_list = [task for task in tasks_list if task["id"] != task_id]
    
    # Return an empty response
    # Since we're targeting the task item with hx-target, and returning nothing,
    # HTMX will effectively remove that element from the page
    return HttpResponse("")

def edit_task(request, task_id):
    """
    This function handles editing tasks.
    
    It does two things:
    1. GET request: Shows an edit form
    2. POST request: Saves the edited text
    
    This is a bit more complex because we need to handle two different types of requests.
    """
    if request.method == "GET":
        # Someone clicked the edit button - show them an edit form
        # Find the task they want to edit
        for task in tasks_list:
            if task["id"] == task_id:
                # Return the edit form template
                return render(request, 'tasks/edit_form.html', {'task': task})
    
    elif request.method == "POST":
        # Someone submitted the edit form - save the changes
        # Get the new text from the form
        new_text = request.POST.get('task_text', '').strip()
        
        if new_text:  # Only save if there's actual text
            # Find and update the task
            for task in tasks_list:
                if task["id"] == task_id:
                    task["text"] = new_text  # Update the text
                    
                    # Return the updated task item HTML
                    return render(request, 'tasks/task_item.html', {'task': task})
    
    # If we get here, something went wrong - return nothing
    return HttpResponse("")

def get_stats(request):
    """
    This function returns just the statistics section.
    
    Instead of updating the entire page, HTMX can update just one part.
    This function returns only the stats HTML, which gets inserted into the page.
    """
    # Return just the stats template with the current task data
    return render(request, 'tasks/stats.html', {'tasks': tasks_list})
