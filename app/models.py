
from django.db import models
from django.contrib.auth.models import User

class CreateTournament(models.Model):   
    tournament_name = models.CharField(max_length=255)
    organizer_name = models.CharField(max_length=255)
    battle_type = models.CharField(max_length=255)
    number_of_team = models.CharField(max_length=255)
    maximum_player_per_team = models.CharField(max_length=255)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    class Meta:  
        db_table = "CreateTournament"
    def __str__(self):
        return self.tournament_name

class CreateTeam(models.Model):   
    team_name = models.CharField(max_length=255)
    createtournament = models.ForeignKey(CreateTournament,on_delete=models.CASCADE,null=True)
    class Meta:  
        db_table = "CreateTeam"
    def __str__(self):
        return self.team_name

class TempEnterResult(models.Model):   
    team_name = models.CharField(max_length=255)
    place_points = models.CharField(max_length=255)
    kill = models.CharField(max_length=255)
    total = models.CharField(max_length=255)
    match = models.CharField(max_length=255)
    # user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    # team_id = models.ForeignKey(CreateTeam,on_delete=models.CASCADE,null=True)
    tourament_id = models.ForeignKey(CreateTournament,on_delete=models.CASCADE,null=True)
    class Meta:  
        db_table = "TempEnterResult"
    def __str__(self):
        return self.team_name

class Result(models.Model):   
    team_name = models.CharField(max_length=255)
    place_points = models.CharField(max_length=255)
    kill = models.CharField(max_length=255)
    total = models.CharField(max_length=255)
    match = models.CharField(max_length=255)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    # team_id = models.ForeignKey(CreateTeam,on_delete=models.CASCADE,null=True)
    tourament_id = models.ForeignKey(CreateTournament,on_delete=models.CASCADE,null=True)
    class Meta:  
        db_table = "Result"
    def __str__(self):
        return self.team_name
        


class PlacePoints(models.Model):   
    place  = models.CharField(max_length=255)
    points = models.CharField(max_length=255)
    class Meta:  
        db_table = "PlacePoints"
    def __str__(self):
        return self.place


class PlacePointsImage(models.Model):   
    # counter_number  = models.CharField(max_length=255)
    width  = models.CharField(max_length=255)
    height = models.CharField(max_length=255)
    class Meta:  
        db_table = "PlacePointsImage"
    def __str__(self):
        return self.width
        
        