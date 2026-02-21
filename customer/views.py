from django.shortcuts import render, redirect
from customer.forms import CustomerPasswordChangeForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


@login_required
def customer_dashboard(request):
    return render(request, 'customer/dashboard.html')


@login_required
def customer_password_change(request):
    if request.method == 'POST':
        form = CustomerPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            logout(request)
            messages.success(request, 'Password changes successfully. Please login with your new password.')
            return redirect('login_user')
    else:
        form = CustomerPasswordChangeForm(user=request.user)
    return render(request, 'customer/password_change.html', {'form': form})