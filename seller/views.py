from django.shortcuts import render, redirect
from seller.forms import SellerPasswordChangeForm
from django.contrib import messages
from django.contrib.auth import logout
from core.decorators import login_and_role_required

@login_and_role_required('seller')
def seller_dashboard(request):
    return render(request, 'seller/dashboard.html')


@login_and_role_required('seller')
def seller_password_change(request):
    if request.method == 'POST':
        form = SellerPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            logout(request)
            messages.success(request, 'Password changed successfully. Please login with your new password.')
            return redirect('login_user')
    else:
        form = SellerPasswordChangeForm(user=request.user)
    return render(request, 'seller/password_change.html', {'form': form})