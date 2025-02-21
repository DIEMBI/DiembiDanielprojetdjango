from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Project
from .forms import ProjectForm
from .forms import TaskForm
from django.shortcuts import render
from django.db.models import Count
from datetime import datetime, timedelta
from .models import Task, TaskCompletion
from django.contrib.auth.models import User
from django.db import models
from .forms import SignUpForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate

def home(request):
    return render(request, 'home.html')  
@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'update_profile.html', {'form': form})
@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})

@login_required(login_url='/accounts/login/')
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_list.html', {'projects': projects})
@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})

@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

def statistics(request):
    # Calculer la date limite pour les statistiques (trimestre et année)
    today = datetime.today()
    start_of_year = today.replace(month=1, day=1)
    start_of_quarter = today - timedelta(days=(today.month - 1) % 3 * 30)  # Premier jour du trimestre

    # Filtrer les tâches complétées dans les délais
    completed_on_time = TaskCompletion.objects.filter(is_completed_on_time=True)

    # Statistiques trimestrielles et annuelles
    quarterly_stats = TaskCompletion.objects.filter(
        completion_date__gte=start_of_quarter
    ).values('user').annotate(
        tasks_completed=Count('task', filter=models.Q(is_completed_on_time=True)),
        total_tasks=Count('task')
    )

    yearly_stats = TaskCompletion.objects.filter(
        completion_date__gte=start_of_year
    ).values('user').annotate(
        tasks_completed=Count('task', filter=models.Q(is_completed_on_time=True)),
        total_tasks=Count('task')
    )

    # Calculer la prime pour chaque utilisateur
    primes = {}
    for user_stat in quarterly_stats:
        tasks_completed = user_stat['tasks_completed']
        total_tasks = user_stat['total_tasks']
        user_id = user_stat['user']
        prime = 0

        if total_tasks > 0:
            completion_percentage = (tasks_completed / total_tasks) * 100
            if completion_percentage >= 90:
                prime = 30000  # Prime de 30K
            if completion_percentage == 100:
                prime = 100000  # Prime de 100K

        primes[user_id] = prime

    # Passer les statistiques et les primes au template
    context = {
        'quarterly_stats': quarterly_stats,
        'yearly_stats': yearly_stats,
        'primes': primes,
    }

    return render(request, 'statistics.html', context)
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['passer'])
            user.save()
            login(request, user)  # Connexion automatique après l'inscription
            return redirect('home')  # Redirection vers la page d'accueil après l'inscription
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("user")
            password = form.cleaned_data.get("passer")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')  # redirection après connexion réussie
            else:
                form.add_error(None, "Identifiants incorrects.")
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})
@login_required
def profile(request):
    return render(request, 'profile.html')
