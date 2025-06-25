from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review
from django import forms

class ExtendedUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ]
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'star-rating'}),
        label='Ваша оценка'
    )
    
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Напишите ваш отзыв здесь...',
                'class': 'gold-textarea'
            }),
        }
        labels = {
            'text': 'Ваш отзыв',
        }