from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


class Todo(models.Model):

    title = models.CharField(max_length=300)
    content = models.TextField()
    priority = models.IntegerField(default=1)
    is_done = models.BooleanField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='todos')

    class Meta:
        db_table = 'todos'
