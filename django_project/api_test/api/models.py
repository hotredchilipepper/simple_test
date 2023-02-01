from django.db import models

class Users(models.Model):
    email = models.EmailField(max_length=254)
    hash_pass = models.CharField(max_length=254)
    timestamp_create = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    email = models.EmailField(max_length=254)
    question = models.TextField(blank=True)
    answer = models.TextField(blank=True)
    timestamp_create = models.DateTimeField(auto_now_add=True)

