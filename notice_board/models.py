from django.db import models


class Message(models.Model):
    message = models.CharField(max_length=140)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
