from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

class Employee(models.Model):
    """Модель сотрудника (мастера)"""
    full_name = models.CharField(
        verbose_name='ФИО мастера',
        max_length=100
    )
    photo = models.ImageField(
        verbose_name='Фото мастера',
        upload_to='employees/',
        blank=True,
        null=True
    )
    prof = models.CharField(
        verbose_name='Направление',
        max_length=100,
        null=True
    )
    worked = models.CharField(
        verbose_name='Опыт работы(в годах)',
        max_length=100,
        null=True
    )
    do = models.CharField(
        verbose_name='Что умеет',
        max_length=100,
        null=True
    )

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'

    def __str__(self):
        return self.full_name


class Service(models.Model):
    title = models.CharField(
        verbose_name='Название услуги',
        max_length=100
    )
    description = models.TextField(
        verbose_name='Описание услуги',
        blank=True
    )
    price = models.DecimalField(
        verbose_name='Цена (руб)',
        max_digits=10,
        decimal_places=2,
        default=0
    )
    image = models.ImageField(
        verbose_name='Изображение услуги',
        upload_to='services/',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.title


class Appointment(models.Model):
    """Модель записи клиента"""
    phone_regex = RegexValidator(
        regex=r'^(\+7|8)\d{10}$',
        message="Номер телефона должен быть в формате: '+79991234567' или '89991234567'"
    )

    client_name = models.CharField(
        verbose_name='ФИО клиента',
        max_length=100
    )
    phone = models.CharField(
        verbose_name='Телефон',
        max_length=12,
        validators=[phone_regex]
    )
    date_time = models.DateTimeField(
        verbose_name='Дата и время записи'
    )
    master = models.ForeignKey(
        Employee,
        verbose_name='Мастер',
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    service = models.ForeignKey(
        Service,
        verbose_name='Услуга',
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания записи',
        auto_now_add=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['-date_time']

    def __str__(self):
        return f"{self.client_name} → {self.service.title} ({self.date_time})"

class ClientAppointment(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    master = models.ForeignKey('Employee', on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    date_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointments'
    )
    
    class Meta:
        verbose_name = 'Запись клиента'
        verbose_name_plural = 'Записи клиентов'
        ordering = ['-date_time']
    
    def __str__(self):
        return f'Запись {self.client_name} на {self.date_time}'

User = get_user_model()

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)