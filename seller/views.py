from django.shortcuts import render, redirect
from seller.forms import SellerPasswordChangeForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required
def seller_dashboard(request):
    return render(request, 'seller/dashboard.html')


@login_required
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