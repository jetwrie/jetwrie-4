from django.urls import path
from .views import RegisterView,Profile,Login,PasswordChange
from django.contrib.auth.views import LogoutView 
urlpatterns =[
	path('register/',RegisterView.as_view(),name="register"),
	path('login/',Login.as_view(),name="login"),
	path('logout/', LogoutView.as_view(next_page='login'),name='logout'),
	path('profile/', Profile.as_view(),name='profile'),
	path('password_change/',PasswordChange.as_view(),name='passwordchange'),
]