from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    views_qty = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Report(models.Model):
    user_email = models.EmailField()
    text = models.TextField(blank=False)
    responded = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text