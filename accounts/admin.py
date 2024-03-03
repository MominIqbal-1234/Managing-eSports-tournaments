  
from django.contrib import admin
from accounts.models import UserInfoURL
from django.contrib.auth.models import User,Group

# Remove Group and User Table in Admin Panel
# admin.site.unregister(User)
# admin.site.unregister(Group)


# View DB Table in Admin Panel
# admin.site.register(URLS)
# ----------------------------------
@admin.register(UserInfoURL)
class UserInfoTable(admin.ModelAdmin):
    list_display =  ['id','id_user']


        