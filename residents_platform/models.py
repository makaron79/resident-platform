from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Topic(models.Model):
    """Temat poznawany przez użytkownika."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    #image = models.ImageField(upload_to='home/')

    # @property
    def __str__(self):
        """Zwraca reprezentację modelu w postaci ciągu tekstowego."""
        return self.text


class Entry(models.Model):
    """Konkretne informacje."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Zwraca reprezentację modelu w postaci ciągu tekstowego."""
        return f"{self.text[:50]}..."
