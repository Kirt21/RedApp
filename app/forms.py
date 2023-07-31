from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Rooms,Topic,User
    
class RoomForm(ModelForm):
    class Meta:
        model = Rooms 
        fields = '__all__'
        exclude={'host','topic'}

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = '__all__'

class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model= User
        fields='__all__'
        # {'username','first_name','last_name','profile_photo','email','Bio',}  
        exclude={'last_login','date_joined','is_staff','is_active','is_superuser','password','groups','user_permissions'}


        
