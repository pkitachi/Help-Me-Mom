from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from blog.models import Post, Coins
# Create your views here.

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account for {username} has been created Log In!')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html',{'form':form})

@login_required
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST,instance=request.user)
		p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Details saved successfully')
			return redirect('profile')
	else:
		coins = Post.objects.filter(author = request.user).count()*10
		c = Coins(author = request.user,coinNo = coins)
		c.save()
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
	context = {
	'u_form':u_form,
	'p_form':p_form,
	'coins':coins
	}
	return render(request,'users/profile.html', context)

def leaderboard(request):
	# coins = Post.objects.filter(author.username == "hruday")
	# c = Coins.objects.filter(author.username == "hruday")
	# c.update(coinNo = coins)
	# print(c.coinNo)	
	
	return render(request,'users/leaderboard.html')