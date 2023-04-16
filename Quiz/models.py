from django.db import models

# Create your models here.
class QuesModel(models.Model):
    question = models.CharField(max_length=200,null=True)
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    ans = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.question
    
class Stats(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    #user=models.ForeignKey()
    name = models.CharField(max_length=200)
    time = models.IntegerField()
    score = models.IntegerField()

    def __str__(self):
        return self.name