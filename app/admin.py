from django.contrib import admin
from .models import Rooms,Message,Topic,User,Follower
from django.contrib.auth.admin import UserAdmin
from .forms import UserForm
#Register your models here.

admin.site.register(Topic)
admin.site.register(Rooms)
admin.site.register(Message)
class CustomUserAdmin(UserAdmin):
    add_form = UserForm
admin.site.register(User)
admin.site.register(Follower)
