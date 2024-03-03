  
from django.contrib import admin
from app.models import CreateTournament,PlacePoints,TempEnterResult,CreateTeam,PlacePointsImage,Result
from django.contrib.auth.models import User,Group

# Remove Group and User Table in Admin Panel
# admin.site.unregister(User)
# admin.site.unregister(Group)


# View DB Table in Admin Panel
admin.site.register(CreateTournament)
admin.site.register(PlacePoints)
admin.site.register(TempEnterResult)
admin.site.register(CreateTeam)
admin.site.register(Result)
admin.site.register(PlacePointsImage)
# ----------------------------------
# @admin.register(MyTableName)
# class MyTableName(admin.ModelAdmin):
#     list_display =  ['id','name']
        