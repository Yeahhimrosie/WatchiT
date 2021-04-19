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
            # messages.type = "registration"
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            print(pw_hash)
            user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
            request.session['user_id'] = user.id
            return redirect('/dashboard')
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
                return redirect('/dashboard')
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
# .first() is a method used when the list is potentially empty, it wont break/"index out of range" if there is not index value (null)
        'current_movie': Movie.objects.filter(watchd=False).order_by('-created_at').first(),
        'last_watchd': Movie.objects.filter(watchd=True).order_by('-updated_at').first(),
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
            if 'release_date' not in request.POST:
                release_date = None
            else:
                release_date = request.POST['release_date']
            Movie.objects.create(title=request.POST['title'], desc=request.POST['desc'], release_date=release_date, liked_by=User.objects.get(id=request.session['user_id']), watchd=False)
            return redirect('/dashboard')
    return redirect('/dashboard')

def watchd(request):
    if 'user_id' not in request.session:
        return redirect('/')
    current_movie = Movie.objects.all().filter(watchd=False).order_by('-created_at').first()
    if current_movie != None:
        current_movie.watchd = True
        current_movie.save()
    return redirect('/dashboard')

# ITS OK TO DEFINE FUNCTIONS WITH THE SAME NAME AS LONG AS THEY HAVE A DIFFERENT NUMBER OF PARAMETERS, THIS ONE BELOW STILL WORKS BECUASE OF THE DIFF. NUMBER OF ARGUMENTS BEING PASSED
def watchd(request, movie_id):
    if 'user_id' not in request.session:
        return redirect('/')
    current_movie = Movie.objects.get(id=movie_id)
    print(current_movie.watchd)
    if current_movie:
        current_movie.watchd = True
        current_movie.save()
    return redirect('/dashboard')


def watch_again(request, movie_id):
    if 'user_id' not in request.session:
        return redirect('/')
    current_movie = Movie.objects.get(id=movie_id)
    if current_movie != None:
        current_movie.watchd = False
        current_movie.save()
    return redirect('/watchiT_page')

def edit(request, movie_id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        'current_movie': Movie.objects.get(id=movie_id)
    }
    return render(request, 'edit.html', context)

def save_changes(request, movie_id):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method =='POST':
        errors = Movie.objects.movie_validator(request.POST)
        if len(errors)> 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/edit/{movie_id}')
        else:
            movie = Movie.objects.get(id=movie_id)
            movie.title = request.POST['title']
            movie.desc = request.POST['desc']
            movie.release_date = request.POST['release_date']
            movie.save()
            return redirect('/dashboard')

def delete(request, movie_id):
    if 'user_id' not in request.session:
        return redirect('/')
    movie_to_delete = Movie.objects.get(id=movie_id)
    movie_to_delete.delete()
    print(f"Look here! Movie id =", movie_id)
    return redirect('/dashboard')


def love(request, movie_id):
    if 'user_id' not in request.session:
        return redirect('/')
    # if request.method == "POST":
    current_user = User.objects.get(id=request.session['user_id'])
    current_movie = Movie.objects.get(id=movie_id)
    current_movie.liked_by = current_user
    current_movie.save()
    return redirect('/dashboard')



def unlove(request, movie_id):
    if 'user_id' not in request.session:
        return redirect('/')
    current_user = User.objects.get(id=request.session['user_id'])
    current_movie = Movie.objects.get(id=movie_id)
    # current_movie.liked_by.remove(current_user) (DOESNT NEED THIS SINCE ITS NOT A MANY TO MANY FIELD) NEEDS THIS NONE STATEMENT
    current_movie.liked_by=None
    # print(f'current movie is', current_movie)
    # print(f'current movie is', current_movie.liked_by)
    current_movie.save()
    return redirect('/dashboard')


def watchiT_page(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'all_movies': Movie.objects.all(),
        'watchit_movies': Movie.objects.filter(watchd=False).order_by('updated_at'),
        'current_user': User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'watchiT.html', context)



def watchd_page(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        'all_movies': Movie.objects.all(),
        'watchd_movies': Movie.objects.filter(watchd=True).order_by('-updated_at'),
    }
    return render(request, 'watchd.html', context)

def how_to(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return render(request, 'how_to.html')