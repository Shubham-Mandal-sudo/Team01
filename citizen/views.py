from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username not found')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        
        else:
            messages.error(request, "Username and password didn't match")

    return render(request, 'citizen/login.html')

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,"An error occured during registration")

        
    return render(request, 'citizen/register.html', {'form': form})
    

def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/login')
def grevance(request):
    form = PostForm()
    if request.method == 'GET':
        username = request.user.username
        initial_data = {'host':username, 'status':'pending'}
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            messages.error(request, 'There was an error in your submission. Please correct the errors below.')
        
    context = {'form':form}
    return render(request, 'citizen/grevance_from.html', context)

@login_required(login_url='/login')
def post(request,pk):
    post = Post.objects.get(id=pk)
    context = {'post':post}
    return render(request, 'citizen/grevance_show.html', context)

@login_required(login_url='/login')
def home(request):
    posts = Post.objects.all()
    context = {'posts':posts}
    return render(request, 'citizen/home.html', context)

