from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    
    def validateUser(self, name, alias, email, password, password_confirm, dob):
        errors = []

        if len(name) < 1:
            errors.append("Name is required")
        elif len(name) < 1:
            errors.append("Name must be longer than 3 char")


        if len(alias) < 1:
            errors.append("Alias is required")
        elif len(alias) < 3:
            errors.append("Alias must be longer than 3 char")


        if len(email) < 1:
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(email):
            errors.append("invalid email")
        else:
            user = User.objects.filter(email=email.lower())
            if len(user)> 0:
                errors.append("Email already in use")


        if len(password) < 1:
            errors.append("Password is required")
        elif len(password) < 8:
            errors.append("Password must be longer than 8 char")


        if len(password_confirm) < 1:
            errors.append("Confirm password is required")
        elif password_confirm != password:
            errors.append("Password and Confirm Password must match")


        if len(dob) < 1:
            errors.append("dob is required")
        elif str(dob) > str(datetime.now()):
            errors.append("Birthday must be in the past!")

        if len(errors)> 0: 
            print errors
            return (False, errors)
        else :
            user = User.objects.create(name=name, alias=alias, email=email.lower(), password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()), dob=dob)
            return (True,user)

    def validateLogin(self, login_email, login_password):
        errors = []
        if len(login_email) < 1:
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(login_email):
            errors.append('Email is invalid')

        if len(login_password) < 1:
            errors.append('Password is required')
        else:
            user = User.objects.filter(email=login_email.lower())
            if len(user) == 0:
                errors.append("Email is not found in database")
            else:

                print user  # <QuerySet [<User: User object>]> this is a valid user print 
                print user[0]  # User object
                if bcrypt.checkpw(login_password.encode(), user[0].password.encode()):
                    return (True, user[0])
                else:
                    errors.append('Password is incorrect')
        if len(errors) > 0:
            print
            return (False, errors)


class ProductManager(models.Manager):
    def validateProduct(self, name, price, seller, buyer):
        Product.objects.create(product=name, amount=price,seller=seller, buyer=buyer )
        return ()
    def createProduct(self, product, amount, seller, buyer):
        Product.objects.seller = post_data['seller']
    def buy(self, post_data, pid, uid):
        product = Product.objects.get(id=pid)
        product  = post_data['buyer']
        

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    dob = models.DateField(auto_now=False, auto_now_add=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_sold = models.DateTimeField(auto_now_add=True)
    objects = UserManager()



class Product(models.Model):
    product = models.CharField(max_length=255)
    amount = models.IntegerField()
    seller = models.ForeignKey(User, related_name='products')
    buyer = models.ForeignKey(User, related_name='bought_products')
    Posted_at = models.DateTimeField(auto_now_add=True)
    bought_at = models.DateTimeField(auto_now=True)
    objects = ProductManager()


# Create a 