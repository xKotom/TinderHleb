from django import forms
from .models import Profile, Feedback


class RegisterForm(forms.Form):
    nickname = forms.CharField(
        max_length=100,
        label='Имя / Псевдоним',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ваше имя или псевдоним'})
    )
    email = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'example@mail.ru'})
    )
    card_number = forms.CharField(
        max_length=20,
        label='Номер клубной карты',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Номер карты «Тёплого хлеба»'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Придумайте пароль'}),
        label='Пароль'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Повторите пароль'}),
        label='Подтверждение пароля'
    )

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Пароли не совпадают')
        return cleaned_data


class LoginForm(forms.Form):
    card_number = forms.CharField(
        max_length=20,
        label='Номер клубной карты',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Номер карты'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Пароль'}),
        label='Пароль'
    )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'avatar', 'gender', 'birth_date', 'age', 'about',
                  'keywords', 'favorite_item', 'search_mode', 'looking_for_gender']
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-input'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'age': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Ваш возраст'}),
            'about': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Расскажите о себе...'}),
            'keywords': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'музыка, книги, кофе...'}),
            'favorite_item': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'круассан, чиабатта, багет...'}),
            'search_mode': forms.Select(attrs={'class': 'form-select'}),
            'looking_for_gender': forms.Select(attrs={'class': 'form-select'}),
            'avatar': forms.FileInput(attrs={'class': 'form-input'}),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 5,
                'placeholder': 'Напишите ваш отзыв...'
            })
        }
