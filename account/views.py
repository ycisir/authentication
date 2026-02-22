from django.shortcuts import render, redirect
from account.forms import RegistrationForm, LoginForm, PasswordResetForm, CustomSetPasswordForm
from account.models import User
from django.contrib import messages
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from account.utils import send_activation_mail, password_reset_email
from django.contrib.auth import authenticate, login
from core.utils import assign_permission


# register user 
def register_user(request):
    if request.user.is_authenticated:
        if request.user.is_seller:
            return redirect('seller_dashboard')
        elif request.user.is_customer:
            return redirect('customer_dashboard')
        return redirect('home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active = False

            # role base registration logic here
            role = request.POST.get('role')
            if role == 'seller':
                user.is_seller = True
                user.is_customer = False
            else:
                user.is_seller = False
                user.is_customer = True

            user.save()

            # assign permissions programatically logic here
            assign_permission(user, role)

            # activation mail logic here
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = reverse('activate_account', kwargs={'uidb64': uidb64, 'token': token})
            activation_url = f'{settings.SITE_DOMAIN}{activation_link}'
            send_activation_mail(user.email, activation_url)
            messages.success(request, 'Registration successful! Please check your email to activate your account.')
            return redirect('login_user')
    else:
        form = RegistrationForm()
    return render(request, 'account/register.html', {'form': form})

# activate user 
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if user.is_active:
            messages.warning(request, 'This account has already been activated.')
            return redirect('login_user')
        
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated successfully!')
            return redirect('login_user')
        else:
            messages.error(request, 'The activation link is invalid or has expired.')
            return redirect('login_user')
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, 'Invalid activation link.')
            return redirect('register_user')


# login
def login_user(request):
    form = LoginForm(request.POST or None)
    if request.user.is_authenticated:
        if request.user.is_seller:
            return redirect('seller_dashboard')
        elif request.user.is_customer:
            return redirect('customer_dashboard')
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'Both fields are required.')
            return redirect('login_user')
        
        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return redirect('login_user')
        
        if not user.is_active:
            messages.error(request, 'Your account is inactive, Please activate your account.')
            return redirect('login_user')
        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_seller:
                return redirect('seller_dashboard')
            elif request.user.is_customer:
                return redirect('customer_dashboard')
            else:
                messages.error(request, 'You do not have permission to access this area.')
                return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login_user')


    return render(request, 'account/login.html', {'form': form})




# password reset
def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email=email).first()
            if user:
                # password reset mail logic
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
                absolute_reset_url = request.build_absolute_uri(reset_url)
                password_reset_email(user.email, absolute_reset_url)
                messages.success(request, 'We have sent you a password reset link. Please check your email.')
                return redirect('login_user')

    else:
        form = PasswordResetForm()
    return render(request, 'account/password_reset.html', {'form': form})



# password_reset_confirm
def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if not default_token_generator.check_token(user, token):
            messages.error(request, 'This link has expired or is invalid.')
            return redirect('password_reset')
        
        if request.method == 'POST':
            form = CustomSetPasswordForm(user, request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been successfully reset.')
                return redirect('login_user')
        else:
            form = CustomSetPasswordForm(user)
    
        return render(request, 'account/password_reset_confirm.html', {'form': form})
    
    except (TypeError, OverflowError, User.DoesNotExist):
        messages.error(request, 'An error occured. Please try again later.')
        return redirect('password_reset')

