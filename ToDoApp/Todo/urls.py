from django.urls import path
from Todo import views
from django.conf.urls import url, include

app_name="Todo"
urlpatterns=[
    path ('',views.startlogin,name='startlogin'),
    path('userregister',views.UserRegisterView.as_view(),name='userregister'),
    path('userlogin',views.UserLoginView.as_view(),name='userlogin'),
    path('userlogout',views.UserLogoutView.as_view(),name='userlogout'),
    path('verifytoken/<str:token>',views.VerifyToken.as_view(),name='verifytoken'),
    path('generateOTP',views.GenerateOTP.as_view(),name='generateOTP'),
    path('checkOTP',views.CheckOTP.as_view(),name='checkOTP'),
    path('changepassword',views.ChangePassword.as_view(),name='changepassword'),
    path('notes',views.NoteList.as_view(),name='notes'),
    path('createnote',views.CreateNote.as_view(),name='createnote'),
    path('note/<str:pk>',views.NoteDetail.as_view(),name='note'),
    path('collaborator',views. CreateListCollaborator.as_view(),name='collaborator'),
    path('collaborator/<str:pk>',views. CreateListCollaborator.as_view(),name='getcollaborator'),
    path('getuser/<str:pk>',views. GetUserView.as_view(),name='getuser'),
    path('getuserbyusername/<str:username>',views. GetUserByUserName.as_view(),name='getuserbyusername'),
    ]
