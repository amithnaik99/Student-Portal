from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('announcements/', views.announcements, name='announcements'),
    path('attendance/', views.attendance, name='attendance'),
    path('marks/', views.marks, name='marks'),
    path('timetable/', views.timetable, name='timetable'),
    path('upload-students/', views.upload_students, name='upload_students'),  # ← NEW
]