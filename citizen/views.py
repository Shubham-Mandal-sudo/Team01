from django.shortcuts import render, redirect
from .models import Post, status
from .forms import PostForm, UserRegistrationForm, LoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.

def loginPage(request):
    # Check if there's a next parameter in the URL or form submission
    next_url = request.GET.get('next', '')
    if not next_url:
        next_url = request.POST.get('next', '')

    # If next_url is empty or not provided, default to home
    if not next_url:
        next_url = 'home'

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                # Check if next_url is a full URL or just a path
                if next_url == 'home' or next_url.startswith('/'):
                    return redirect(next_url)
                else:
                    # If it's not a valid URL pattern, default to home
                    return redirect('home')
            else:
                messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = LoginForm()

    return render(request, 'citizen/login.html', {'form': form, 'next': next_url})

def registerPage(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'citizen/register.html', {'form': form})


def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def grevance(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your grievance has been submitted successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Pre-fill the host field with the current user
        initial_data = {'host': request.user}
        form = PostForm(initial=initial_data)

    context = {'form': form}
    return render(request, 'citizen/grevance_from.html', context)

@login_required(login_url='login')
def post(request,pk):
    post = Post.objects.get(id=pk)
    context = {'post':post}
    return render(request, 'citizen/grevance_show.html', context)

@login_required(login_url='login')
def home(request):
    posts = Post.objects.all()
    context = {'posts':posts}
    return render(request, 'citizen/home.html', context)

@login_required(login_url='/login')
def change_status(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user.is_staff:
        post.status = status.objects.get(name="Resolved")
        post.save()
        messages.success(request, 'Status updated to resolved.')
    else:
        messages.error(request, 'You do not have permission to change the status.')
    return redirect('view_grevance', pk=pk)

