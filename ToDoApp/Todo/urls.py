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
    path('addimage',views.AddImage.as_view(),name='addimage'),
    path('getimage/<str:owner>',views.GetImage.as_view(),name='getimage'),
    path('collaborator/<str:pk>',views.CollaboratorDetail.as_view(),name='getcollaborator'),
    path('getuser/<str:pk>',views. GetUserView.as_view(),name='getuser'),
    path('getuserbyusername/<str:username>',views. GetUserByUserName.as_view(),name='getuserbyusername'),
    path('deletecollaborator/<str:owner>/<str:note>/<str:shareduser>',views. DeleteCollaborator.as_view(),name='getuserbyusername'),
    path('addlabel',views. LabelCreate.as_view(),name='addlabel'),
    path('getlabel',views. GetAllLabels.as_view(),name='getlabel'),
    path('addlabeltonote/<str:note>/<str:label>',views. AddNoteToLabel.as_view(),name='addlabeltonote'),
    path('getlabelbynote',views. GetAllLabelsFromNote.as_view(),name='getlabelbynote'),
    path('getcollabbynote/<str:note>',views. GetCollabFromNote.as_view(),name='getcollabbynote'),
    ]





