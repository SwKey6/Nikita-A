from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.timezone import make_aware
from datetime import datetime
from .models import Service, Employee, Appointment
from .models import ClientAppointment
from .forms import ExtendedUserCreationForm
from .forms import ReviewForm
from .models import Review

def Main(request):
    return render(request, 'Main/index.html')

def About(request):
    services = Service.objects.all()
    return render(request, 'Main/about.html', {'services': services})

def Contacts(request):
    return render(request, 'Main/contacts.html')

def Services(request):
    services = Service.objects.all()
    return render(request, 'Main/services.html', {'services': services})

def Staff(request):
    employees = Employee.objects.all()
    return render(request, 'Main/staff.html', {'employees': employees})

def Portfolio(request):
    return render(request, 'Main/portfolio.html')

def Connect(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    employees = Employee.objects.all()
    
    if request.method == 'POST':
        try:
            master_id = request.POST.get('master')
            client_name = request.POST.get('client_name')
            phone = request.POST.get('phone')
            datetime_str = request.POST.get('datetime')
            
            if not all([master_id, client_name, phone, datetime_str]):
                messages.error(request, "Все поля обязательны для заполнения")
                return redirect('Connect', service_id=service_id)
            
            naive_datetime = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
            aware_datetime = make_aware(naive_datetime)
            
            Appointment.objects.create(
                service=service,
                master_id=master_id,
                client_name=client_name,
                phone=phone,
                date_time=aware_datetime,
                user=request.user if request.user.is_authenticated else None  # Сохраняем пользователя
            )
            
            messages.success(request, 'Вы успешно записаны!')
            return redirect('Main')
            
        except ValueError as e:
            messages.error(request, f'Некорректный формат даты: {str(e)}')
        except Exception as e:
            messages.error(request, f'Ошибка при создании записи: {str(e)}')
    
    return render(request, 'Main/connect.html', {
        'service': service,
        'employees': employees
    })

def register_view(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = ExtendedUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('Main')

@login_required
def profile_view(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'registration/profile.html', {'appointments': appointments})
    
@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
    
    if request.method == 'POST':
        appointment.delete()
        return redirect('profile')
    
    return redirect('profile')

@login_required
def reviews(request):
    if request.method == 'POST':
        try:
            text = request.POST.get('text', '').strip()
            rating = request.POST.get('rating', '5')
            
            if not text:
                messages.error(request, "Текст отзыва не может быть пустым")
                return redirect('reviews')
            
            if not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
                messages.error(request, "Некорректная оценка")
                return redirect('reviews')
            
            Review.objects.create(
                text=text,
                rating=int(rating),
                user=request.user
            )
            
            messages.success(request, 'Ваш отзыв успешно добавлен!')
            return redirect('reviews')
            
        except Exception as e:
            messages.error(request, f'Ошибка: {str(e)}')
            return redirect('reviews')
    
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'Main/portfolio.html', {
        'reviews': reviews,
    })