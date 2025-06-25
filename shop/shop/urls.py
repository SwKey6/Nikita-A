from django.contrib import admin
from django.urls import path
from Main import views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from Main.views import register_view, login_view, logout_view, profile_view, cancel_appointment, reviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Main, name='Main'),
    path('about/', views.About, name='About'),
    path('contact/', views.Contacts, name='Contacts'),
    path('services/', views.Services, name='Services'),
    path('staff/', views.Staff, name='Staff'),

    path('connect/<int:service_id>/', views.Connect, name='Connect'),

    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    path('cancel_appointment/<int:appointment_id>/', cancel_appointment, name='cancel_appointment'),
    path('reviews/', views.reviews, name='reviews'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)