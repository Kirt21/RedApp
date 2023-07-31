from django.shortcuts import render,redirect,HttpResponse
#from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from .models import Rooms,Topic,Message,User,Follower
from .forms import RoomForm,UserForm
from random import choice

#l=[
#    {'id':0 , 'name':"science"},
#    {'id':1 , 'name':"math"}
#    ] 

# Create your views here.
# def bar(request):
#     follow_groups=Follower.objects.filter(follower=request.user)
#     f=[]
#     for f1 in follow_groups:
#         f.append(f1.following)      
#     return f

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def loginpage(request):
    #redirect_to = request.GET.get('next', '')
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request, 'User not found!')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            messages.error(request, 'Username or password is incorrect!')

    context={}#'redirect':redirect_to}
    return render(request,"loginpage.html",context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logoutpage(request):
    logout(request)
    return redirect("home",)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def registerpage(request):
    form =UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES)
        if form.is_valid():
            user= form.save()
            user.profile_photo=request.FILES.get('profile_photo')
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else: 
            messages.error(request, 'Error!') 
    context={'form':form}
    return render(request,"registerpage.html",context)


def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    l=Rooms.objects.filter(
        Q(topic__title__icontains=q) |
        Q(title__icontains=q) |
        Q(host__username__icontains=q)
    )
    #count=l.count()
    t=Topic.objects.all()
    g1=groups(request)
    c={}
    for topic in t:
        count=Rooms.objects.filter(topic=topic).count()
        c[topic]=count
    sort=sorted(c.items(), key=lambda x:x[1])
    c=dict(sort)
    
    spot=choice(l)
    context={'l':l,'t':t,'c':c,'spot':spot,'g1':g1}
    return render(request,'home.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def room(request,p):
    l=Rooms.objects.get(id=p)
    messages=Message.objects.filter(room=l).order_by('-created')
    r=Rooms.objects.filter(topic=l.topic)
    fol=False           
    folow=par=gr=g=j=0  
    if request.method=='POST': 
        if request.POST.get('m')=='par':   
            par=1   
        elif request.POST.get('m')=='folow':  
            folow=1      
        elif request.POST.get('m')=='groups':   
            gr=1            
        elif request.user.is_authenticated:          
            message=Message.objects.create(
            user_name=request.user,
            room=l,
            body=request.POST.get('Message')
            )
            l.participants.add(request.user)    
        else:
            return redirect('loginpage')
        
        
    d=1 
    if request.user.is_authenticated: 
        if Follower.objects.filter(follower=request.user,following=l).first():
            fol=True
        else:
            fol=False 

    g=Follower.objects.filter(following=l)
    f=Follower.objects.filter(following=l)
    part=l.participants.all()
    f_count=f.count() 
    m_count=messages.count()
    g1=groups(request) 
    p_count=part.count()
    if l.desc=='':
        d=0       
    context={'l':l,'m':messages,'d':d,'p':part,'f_count':f_count,'p_count':p_count,'fol':fol,'f':f,'par':par,'folow':folow,'r':r,'gr':gr,'g':g,'g1':g1}
    return render(request,'room.html',context)  

@login_required(login_url="loginpage")
def create_room(request):
    if request.method == 'POST':

        topic=request.POST.get('Topic')
        t=0
        try:
            t=Topic.objects.get(title=topic)
            topic_obj=t
        except:    
            if t==0:
                topic_obj=Topic.objects.create(title=topic)

        room=Rooms.objects.create(
        host=request.user,
        topic=topic_obj,
        title=request.POST.get('Title'),
        desc=request.POST.get('Desc'),
        )
       
        room.save()
        return redirect('home')
    g1=groups(request)    
    c=0    
    context={'c':c,'g1':g1}       
    return render(request,'room_form.html',context)    
        
@login_required(login_url="loginpage")
def update_room(request,p):
    room = Rooms.objects.get(id=p)
    if request.user != room.host:
        return HttpResponse("Access denied!")
        # return redirect("room")

    if request.method == 'POST':
        topic=request.POST.get('Topic')
        t=0
        try:
            t=Topic.objects.get(title=topic)
            topic_obj=t
        except:    
            if t == 0:
                topic_obj=Topic.objects.create(title=topic)

        room.host=request.user
        room.topic=topic_obj
        room.title=request.POST.get('Title')
        room.desc=request.POST.get('Desc')  
        room.save()     
        # form = RoomForm(request.POST,instance=room)
        # if form.is_valid():
        #     form.save()
        return redirect('room',room.id)
    c=1        
    context={'room':room,'c':c}        
    return render(request,'room_form.html',context)

@login_required(login_url="loginpage")
def delete_room(request,p):
    room = Rooms.objects.get(id=p)
    # if request.user != room.host:
    #     return HttpResponse("Access denied!")
    if request.method=='POST':
        room.delete()
        return redirect('home')
    context={'obj':room}   
    return render(request,'delete.html',context)

@login_required(login_url="loginpage")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_message(request,p):
    next = request.POST.get('next', '/')
    try:
        message = Message.objects.get(id=p)
    except:
        return redirect(next)  
    if request.method=='POST':
        message.delete()
        return redirect('room',message.room.id)
    g1=groups(request)    
    context={'obj':message,'g1':g1}   
    return render(request,'delete.html',context)

def profile(request,p):
    
    user = User.objects.get(username=p)
    message = Message.objects.filter(user_name_id=user.id)
    rooms = Rooms.objects.filter(host=user.id)
    f=Follower.objects.filter(follower=user.id)
    g1=groups(request)
    hos=fol=0
    if request.method=="POST":
        if request.POST.get('m')=='host':   
            hos=1
        if request.POST.get('m')=='fol':   
            fol=1    
    c=rooms.count()
    fol_count=f.count()
    m=message.count()
    b=user.Bio
    context={'user':user,'rooms':rooms,'c':c,'message':message[:5],'m':m,'b':b,'fol_count':fol_count,'hos':hos,'fol':fol,'f':f,'g1':g1}
    return render(request,'profile.html',context)

def test(request):
    return render(request,"test.html")

@login_required(login_url="loginpage")
def follow(request):
    if request.method == 'POST':
        follower=request.user
        p = request.POST.get('following')
        following=Rooms.objects.get(id=p)
        f=Follower.objects.create(follower=follower,following=following)
        f.save()     
        return redirect('room',p)    
    return redirect('/') 

@login_required(login_url="loginpage")
def unfollow(request):
    if request.method == 'POST':
        follower=request.user
        p = request.POST.get('following')
        following=Rooms.objects.get(id=p)
        f=Follower.objects.get(follower=follower,following=following)
        f.delete()     
        return redirect('room',p)    
    return redirect('/')

def participants(request): 
       part=0
       if request.method == 'POST':
           p = request.POST.get('id')
           part=Rooms.objects.get(id=p)
           context={'part':part}
       return part

def followers(request,id): 
       folow=0
       if request.method == 'POST':
           following=Rooms.objects.get(id=id)
           folow=Follower.objects.get(following=following)
       return folow


def groups(request):
    g=0
    if request.user.is_authenticated:
        g=Follower.objects.filter(follower=request.user)
    return g           




       