from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserInfoURL(models.Model):   
    id_user = models.CharField(max_length=255)
    picture_url = models.CharField(max_length=255)
    user_auth = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)

    class Meta:  
        db_table = "UserInfo"
    def __str__(self):
        return self.picture_url