from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ten email jest już zarejestrowany")
        return email

class SecurityQuestionsForm(forms.Form):
    security_answer1 = forms.CharField(
        label="1. Imię pierwszego zwierzaka",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'input-field'})
    )
    security_answer2 = forms.CharField(
        label="2. Ulubione jedzenie",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'input-field'})
    )
    security_answer3 = forms.CharField(
        label="3. Miejsce urodzenia",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'input-field'})
    )