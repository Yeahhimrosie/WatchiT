from django.db import models
from django.db.models.fields import EmailField
import re
import bcrypt


class UserManager(models.Manager):
    def registration_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['first_name']) <= 2:
            errors ['first_name'] = "Name is too short"
        if len(reqPOST['last_name']) <= 2:
            errors ['last_name'] = "Name is too short"
        if len(reqPOST['email']) <= 6:
            errors ['email'] = "Email too short"
        if len(reqPOST['password']) <= 8:
            errors['password'] = "Password too short"
        if reqPOST['password'] != reqPOST['password_conf']:
            errors['match'] = "Passwords do not match!"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(reqPOST['email']):
            errors['regex'] = "Email in wrong format"
        users_with_email = User.objects.filter(email=reqPOST['email'])
        if len(users_with_email)>= 1:
            errors['dup'] = "Email taken, please create another!"
        return errors


    def login_validator(self, reqPOST):
        errors = {}
        check = User.objects.filter(email=reqPOST['email'])
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(reqPOST['email']):
            errors['regex'] = "Email in wrong format"
        return errors


class MovieManager(models.Manager):
    def movie_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['title']) < 2:
            errors ['title'] = "Movie title should be at least 2 characters"
        if len(reqPOST['desc']) < 5:
            errors ['desc'] = "Movie description should be at least 5 characters"
        return errors


class User(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.EmailField()
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Movie(models.Model):
    title = models.TextField()
    desc = models.TextField()
    release_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    liked_by = models.ForeignKey(User, related_name='user_that_liked', null=True, on_delete=models.CASCADE)
    watchd = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MovieManager()