from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
import uuid


app_name="users"

class User(AbstractUser):
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    def __str__(self):
        return self.username