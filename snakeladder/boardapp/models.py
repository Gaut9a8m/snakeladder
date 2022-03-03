from django.db import models

# Create your models here.
def validate_score(value):
    if value > 100:
        raise Exception('Score should not be greater than 100')

class GameMaster(models.Model):
    id = models.AutoField(primary_key=True)
    generated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Game# {self.pk}"
    


class Player(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    overall_score = models.IntegerField(default=0, validators = [validate_score])
    game = models.ForeignKey('GameMaster',on_delete=models.CASCADE,related_name='player')
    generated = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name', 'game')
        ordering  = ['-game']

class ScoreHistory(models.Model):
    id = models.AutoField(primary_key=True)
    player = models.ForeignKey('Player',on_delete=models.CASCADE, related_name='scorehistory')
    score = models.IntegerField(validators = [validate_score])
    generated = models.DateTimeField(auto_now_add=True)
