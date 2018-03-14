from django.db import models

class MarkovSequence_DBModel(models.Model):
    user_name = models.CharField(max_length=250,default="")
    sequ_name = models.CharField(max_length=250,default="")
    mark_order = models.IntegerField()
    sequ_length = models.IntegerField()
    sequence = models.CharField(max_length=30000)

class DeBruijnSequence_DBModel(models.Model):
    user_name = models.CharField(max_length=250,default="")
    sequ_name = models.CharField(max_length=250,default="")
    db_order = models.IntegerField()
    sequ_length = models.IntegerField()
    sequence = models.CharField(max_length=30000)


class GeneratedSequence(models.Model):
    user_name = models.CharField(max_length=250)
    sequence = models.CharField(max_length=20000)
    sequence_type = models.CharField(max_length=30) ## descriptions, such as "De-Bruijn,..."
    def __str__(self):
        return self.user_name + " " + self.sequence
