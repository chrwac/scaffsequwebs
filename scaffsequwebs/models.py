from django.db import models
import datetime

def now():
    return datetime.datetime.now()

class RepetitiveSequence_DBModel(models.Model):
    user_name = models.CharField(max_length=250,default="")
    sequ_name = models.CharField(max_length=250,default="")
    length_of_variable_part = models.IntegerField()
    sequ_length = models.IntegerField()
    sequence = models.CharField(max_length=30000)
    datetime = models.DateTimeField(default=now)
    
class MarkovSequence_DBModel(models.Model):
    user_name = models.CharField(max_length=250,default="")
    sequ_name = models.CharField(max_length=250,default="")
    markov_order = models.IntegerField()
    sequ_length = models.IntegerField()
    sequence = models.CharField(max_length=30000)
    datetime = models.DateTimeField(default=now)

class DeBruijnSequence_DBModel(models.Model):
    user_name = models.CharField(max_length=250,default="")
    sequ_name = models.CharField(max_length=250,default="")
    db_order = models.IntegerField()
    sequ_length = models.IntegerField()
    sequence = models.CharField(max_length=30000)
    datetime = models.DateTimeField(default=now)

class GeneratedSequence(models.Model):
    user_name = models.CharField(max_length=250)
    sequence = models.CharField(max_length=20000)
    sequence_type = models.CharField(max_length=30) ## descriptions, such as "De-Bruijn,..."
    def __str__(self):
        return self.user_name + " " + self.sequence
