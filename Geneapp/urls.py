
from django import views
from django.urls import path
from Geneapp.views import *
from .views import view_file, download_file


urlpatterns = [
    path('index/', index_view),
    path('login/', login_view, name='login'),
    path('register/', register_view),
    path('forgot/', forgot_view),
    path('wes/', wes_view,name='wesdata'),
    path('wgs/', wgs_view,name='wgsdata'),
    path('tngs/', tngs_view,name='tngsdata'),
    path('wesdata/', wesdata_view),
    path('tngsdata/', tngsdata_view),
    path('wgsdata/', wgsdata_view),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='activate'),
    path('reset_password/',reset_password, name='reset_password'),	
    path('reset_password/<str:uidb64>/<str:token>/',reset_password_link, name='reset_password_link'),
    path('',landingpage_view),
    # path('workflow/',workflow_view),
    path('analysis/',analysis_view),
    path('profile/',profile),
    path('user_history/', user_history, name='user_history'),
    path('user_history/<int:project_id>/', user_history, name='user_history_with_project'),
    path('workflow_details/<int:Workflow_ID>/', workflow_details_view, name='workflow_details'),
    path('data_analysis/',data_analysis),
    path('cproject/',create_project),
    path('selectworkflow/',workflow_select,name='selectworkflow'),
    path('runfastqc/', run_fastqc, name='runfastqc'),
    path('runtrimming/', run_trimming, name='runtrimming'), 
    path('dataanalysis/<int:project_id>/', data_analysis_project, name='data_analysis_project'),
    path('upload_to_project/',upload_to_project, name='upload_to_project'),
    path('workflow_details2/<int:Workflow_ID>/', workflow_details_view2, name='workflow_details2'),
    path('download_galog/', download_galog, name='download_galog'),
    path('view-file/<path:file_path>/', view_file, name='view_file'),
    path('download-file/<path:file_path>/', download_file, name='download_file'),
    # path('serve_local_file/', serve_local_file, name='serve_local_file'),
    










    



]

