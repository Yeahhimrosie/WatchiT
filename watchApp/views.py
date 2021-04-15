from django.shortcuts import redirect, render
import bcrypt
from django.contrib import messages
from .models import *

def index(request):
    return render(request, 'index.html')


def user_id(request, user_id):
    context = {
        'one_user': User.objects.get(id=user_id)
    }
    return render(request, 'index.html', context)


def create_user(request):
    if request.method =='POST':
        errors = User.objects.registration_validator(request.POST)
        if len(errors)> 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            print(pw_hash)
            user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
            request.session['user_id'] = user.id
            return redirect('/user/success')
    return redirect('/')




def login(request):
    if request.method == 'POST':
        users_with_email = User.objects.filter(email=request.POST['email'])
        errors = User.objects.login_validator(request.POST)
        if users_with_email:
            user = users_with_email[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                print(request.method)
                request.session['user_id'] = user.id
                return redirect('/user/success')
        messages.error(request, "Email or Password incorrect")
    return redirect('/')


def logout(request):
    request.session.flush()
    return redirect('/')

# def movie_id(request, movie_id):
#     context = {
#         current_movie: Movie.objects.get(id=movie_id)
#     }    
#     return render(request, 'dashboard.html', context)

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'dashboard.html', context)


def add_movie(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method =='POST':
        errors = Movie.objects.movie_validator(request.POST)
        if len(errors)> 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/dashboard')
        else:
            Movie.objects.create(title=request.POST['title'], desc=request.POST['desc'], release_date=request.POST['release_date'], liked_by=User.objects.get(id=request.session['user_id']))
            return redirect('/dashboard')
    return redirect('/dashboard')

def watchd(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return redirect('/dashboard')


def edit(request, movie_id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        'current_movie': Movie.objects.get(id=movie_id),
    }
    return render(request, 'edit.html', context)


def delete(request):
    if 'user_id' not in request.session:
        return redirect('/')
    movie_to_delete = Movie.objects.get(id=movie_id)
    movie_to_delete.delete()
    return redirect('/dashboard')


def love(request, movie_id):
    if 'user_id' not in request.session:
        return redirect('/')
    # if request.method == "POST":
    current_user = User.objects.get(id=request.session['user_id'])
    current_movie = Movie.objects.get(id=movie_id)
    current_movie.liked_by.add(current_user)
    return redirect('/dashboard')



def unlove(request, movie_id):
    if 'user_id' not in request.session:
        return redirect('/')
    current_user = User.objects.get(id=request.session['user_id'])
    current_movie = Movie.objects.get(id=movie_id)
    current_movie.liked_by.remove(current_user)
    return redirect('/dashboard')


    #    return redirect(f'/dashboard/{movie_id}')