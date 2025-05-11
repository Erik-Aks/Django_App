from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()
from .forms import CustomUserCreationForm, SecurityQuestionsForm
import random
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def auth_choice_view(request):
    if request.method == 'POST' and 'username' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            request.session['verification_code'] = str(random.randint(1000, 9999))
            request.session['verification_user_id'] = user.id
            print(f"Kod weryfikacji: {request.session['verification_code']}")
            return redirect('accounts:verify_code')
        else:
            messages.error(request, 'Nieprawidłowy login lub hasło!')

    return render(request, 'accounts/auth_choice.html')


def register_initial_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            request.session['register_data'] = {
                'username': form.cleaned_data['email'],
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password1'],
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name']
            }
            return redirect('accounts:security_questions')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register_initial.html', {'form': form})


def security_questions_view(request):
    if 'register_data' not in request.session:
        return redirect('accounts:register_initial')

    if request.method == 'POST':
        form = SecurityQuestionsForm(request.POST)
        if form.is_valid():
            # Створюємо користувача з питаннями безпеки
            user = User.objects.create_user(
                username=request.session['register_data']['username'],
                email=request.session['register_data']['email'],
                password=request.session['register_data']['password'],
                first_name=request.session['register_data']['first_name'],
                last_name=request.session['register_data']['last_name'],
                security_answer1=form.cleaned_data['security_answer1'],
                security_answer2=form.cleaned_data['security_answer2'],
                security_answer3=form.cleaned_data['security_answer3'],
                last_login=timezone.now()
            )
            login(request, user)
            del request.session['register_data']
            messages.success(request, 'Rejestracja zakończona pomyślnie!')
            return redirect('accounts:home')
    else:
        form = SecurityQuestionsForm()

    return render(request, 'accounts/register.html', {'form': form})


def verify_code_view(request):
    if 'verification_code' not in request.session:
        return redirect('accounts:auth_choice')

    if request.method == 'POST':
        entered_code = request.POST.get('code', '')
        if entered_code == request.session.get('verification_code'):
            user_id = request.session.get('verification_user_id')
            if user_id:
                user = User.objects.get(id=user_id)
                login(request, user)
                del request.session['verification_code']
                del request.session['verification_user_id']
                return redirect('accounts:home')
        else:
            messages.error(request, 'Nieprawidłowy kod weryfikacyjny!')

    return render(request, 'accounts/verify_code.html')


def home_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:auth_choice')
    return render(request, 'accounts/home.html')


def logout_view(request):
    logout(request)
    return redirect('accounts:auth_choice')


import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

logger = logging.getLogger(__name__)


def send_verification_code(email, code):
    subject = 'Kod podtwierdzenia'

    # HTML и plain text версии
    html_content = render_to_string('accounts/email_verification.html', {'code': code})
    text_content = strip_tags(html_content)

    try:
        msg = EmailMultiAlternatives(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,  # Используем email из настроек
            [email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        logger.info(f"Kod jest wysłany do {email}")
        return True

    except Exception as e:
        logger.error(f"Błęd wysłany email na {email}: {str(e)}")
        return False

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            verification_code = str(random.randint(1000, 9999))
            request.session['verification_code'] = verification_code
            request.session['verification_user_id'] = user.id

            # Пытаемся отправить email
            try:
                if not send_verification_code(user.email, verification_code):
                    messages.error(request, 'Nie udało się wysłać kod potwierdzenia')
                    return redirect('accounts:login')
            except Exception as e:
                messages.error(request, f'Błęd wysłania: {str(e)}')
                return redirect('accounts:login')

            return redirect('accounts:verify_code')
        else:
            messages.error(request, 'Nieprawidłowy login czy hasło!')

    return render(request, 'accounts/login.html')

