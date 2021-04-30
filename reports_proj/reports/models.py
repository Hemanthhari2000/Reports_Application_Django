from django.db import models
from django.urls import reverse

from profiles.models import Profile


# Create your models here.

class Report(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='reports',blank = True)
    remarks = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.name} by {str(self.author)[11:].upper()}"
    

    def get_absolute_url(self):
        return reverse("reports:detail", kwargs={"pk": self.pk})
    
    # To Order reports in the url `http://127.0.0.1:8000/reports/` in an increasing order.
    class Meta:
        ordering = ('-created',)