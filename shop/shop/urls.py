from django.contrib import admin
from django.urls import path
from Main import views
from django.conf import settings
from django.conf.urls.static import static

Main = views.Main
About = views.About
Contacts = views.Contacts

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Main, name='Main'),
    path('about/', About, name='About'),
    path('contact/', Contacts, name='Contacts'),
    path('Services/', views.Services, name='Services'),
    path('Portfolio/', views.Portfolio, name='Portfolio'),
    path('Staff/', views.Staff, name='Staff'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)