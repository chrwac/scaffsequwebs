from django.db import models

class GeneratedSequence(models.Model):
    user_name = models.CharField(max_length=250)
    sequence = models.CharField(max_length=20000)
    sequence_type = models.CharField(max_length=30) ## descriptions, such as "De-Bruijn,..."
    def __str__(self):
        return self.user_name + " " + self.sequence
