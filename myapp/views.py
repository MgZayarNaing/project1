from django.shortcuts import render,redirect,get_object_or_404
from .models import Task
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def login_views(request):
    if request.method =="GET":
        return render(request,'login.html')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request, "You are now logged in as "+ username )
            return redirect('/myapp/task_list/')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
        
def logout_view(request):
    logout(request)
    return redirect('/login/')

def task_list(request):
    tasks = Task.objects.all().order_by('-id')
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required(login_url='login')
def task_create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        is_completed = request.POST.get('is_completed') == 'on'

        task = Task(title=title, description=description, due_date=due_date, is_completed=is_completed)
        task.save()
        messages.success(request, 'Task created successfully')
        return redirect('task_list')
    return render(request, 'task_form.html')


@login_required(login_url='login')
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task delete successfully')
        return redirect('task_list')

    return render(request, 'delete_task.html', {'task': task})


@login_required(login_url='login')
def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.due_date = request.POST.get('due_date')
        task.is_completed = request.POST.get('is_completed') == 'on'
        
        task.save()
        messages.success(request, 'Task updated successfully')
        return redirect('task_list')

    return render(request, 'task_form.html', {'task': task})


@login_required(login_url='login')
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'task_detail.html', {'task': task})