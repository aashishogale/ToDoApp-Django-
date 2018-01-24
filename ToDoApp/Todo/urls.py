from django.urls import path
from Todo import views
from django.conf.urls import url, include

app_name="Todo"
urlpatterns=[
    
    path('userregister',views.UserRegisterView.as_view(),name='userregister'),
    path('userlogin',views.UserLoginView.as_view(),name='userlogin'),
    ]
