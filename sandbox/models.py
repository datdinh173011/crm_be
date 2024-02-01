from django.db import models

# Create your models here.


class Profile(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.first_name
