from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^listprojectown', views.ProjectListOwn.as_view(), name='listprojectown'),
    url(r'^listprojectjoint', views.ProjectListJoint.as_view() , name='listprojectjoint'),
    url(r'^adduserproject', views.AddUserProject.as_view(), name='adduserproject'),
    url(r'^leaveproject', views.LeaveProject.as_view(), name='leaveproject'),
    url(r'^deleteproject', views.DeleteProject.as_view(), name='deleteproject'),
    url(r'^createproject', views.CreateProject.as_view(), name='createproject'),
    url(r'^listpojectoarticipator', views.ListPojectParticipator.as_view(), name='listpojectoarticipator'),
    ]