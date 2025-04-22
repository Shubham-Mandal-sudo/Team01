from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def loginPage(request):

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
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
                )
            messages.success(request, 'User created successfully')
            return redirect('login')
        messages.error(request, 'User creation failed. Please try again.')
        form = PostForm()
    return render(request, 'citizen/register.html', {'form': form})
    

def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/login')
def grevance(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
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

