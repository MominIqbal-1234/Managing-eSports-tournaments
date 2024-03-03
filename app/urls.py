

from django.urls import path
from app import views

urlpatterns = [
      path('',views.Home.as_view(),name=''),
      path('create_tornment',views.Createtournament.as_view(),name='create_tornment'),
      path('dashboard',views.Dashboard.as_view(),name='dashboard'),
      path('add-team/<str:id>',views.AddTeam.as_view(),name='add-team'),
      path('add-score/<str:id>',views.AddScore.as_view(),name='add-score'),
      path('result/<str:match>',views.ResultMatch.as_view(),name='result'),
      path('view_match/<str:id>',views.ViewMatch.as_view(),name='view_match'),
      path('view_match_table/<str:id>/<str:match>',views.ViewMatchTable.as_view(),name='view_match_table'),
      path('view_point_table/<str:id>/<str:match>/',views.ViewPointTable.as_view(),name='view_point_table'),
      path('viewpointtableimage/<str:id>/<str:match>/',views.ViewPointTableImage.as_view(),name='viewpointtableimage'),

      # path('updatedata',views.updatedata.as_view(),name='updatedata'),


      path('delete_tornment/<str:id>',views.Delete.as_view(),name='delete_tornment'),
      path('delete_team/<str:id>',views.DeleteTeam.as_view(),name='delete_team'),
      path('delete_result/<str:id>',views.DeleteResult.as_view(),name='delete_result'),
      
      
      # path('create_tornment_2',views.CreateTornment_2.as_view(),name='create_tornment'),
      # path('create_tornment_3',views.CreateTornment_2.as_view(),name='create_tornment'),
      # path('create_tornment_4',views.CreateTornment_2.as_view(),name='create_tornment'),
      
]
        