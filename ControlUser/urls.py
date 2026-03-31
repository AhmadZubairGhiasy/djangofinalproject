from django.urls import path
from . import views
from .routes import resumetool

urlpatterns = [
    path('u/',views.get_user),
    path('user/',views.get_user_publicly),
    path('all/',views.getallusers),
    path('register/',views.register_user),
    path('login/',views.login_user),
    path('setphoto/',views.setuserphoto),
    path('setresume/',resumetool.setuserresume),
    path('photo/',views.getuserphoto),
    path('coverphoto/',views.getusercoverphoto),
    path('setcoverphoto/',views.setusercoverphoto),
    path('resume/',resumetool.getuserresume),
    path('gendata/',resumetool.gendata),
    path('logout/',views.logout_user),
]