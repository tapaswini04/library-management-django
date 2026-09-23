from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):

    title = models.CharField(max_length=100)

    author = models.CharField(max_length=100)

    category = models.CharField(max_length=50)

    price = models.FloatField()

    is_borrowed = models.BooleanField(default=False)

    borrowed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    borrowed_date = models.DateField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title