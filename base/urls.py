from django.urls import path
from . import views
# urls.py
from django.conf import Settings

urlpatterns = [
    path('', views.main, name='main'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('room/<str:room_id>/policy/', views.website_policy, name='website_policy'),

    path('services/', views.services, name='services'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('create/', views.create_room, name="create-room"),
    path('join/', views.join_room, name="join-room"),
    path('dorms/', views.view_all_rooms, name='view-rooms'),
    path('room/<str:room_id>/', views.home, name='room-home'),
    path('room/<str:room_id>/bills/new/', views.post_bills, name='post-bills'),
    path('room/<str:room_id>/bills/', views.view_bills, name='view-bills'),
    # path('room/<str:room_id>/bills/remarks/', views.view_bills, name='remark'),
    # path('room/<str:room_id>/bills/view-remarks/', views.view_bills, name='view-remark'),


    path('room/<str:room_id>/bills/<str:bills_slug>/', views.view_member_bills, name='view-member-bills'),
    
    path('room/<str:room_id>/bills/<str:bills_slug>/delete/', views.delete_submission_api, name='delete-submission'),
    path('room/<str:room_id>/bills/<str:bills_slug>/proof/<int:mem_id>', views.view_submitted_proof, name='view-submitted-proof'),

    path('room/<str:room_id>/ToDoList/', views.to_do_list, name='todolist'),
    path('room/<str:room_id>/update_task/<str:pk>', views.updateTask, name='updateTask'),
    path('room/<str:room_id>/delete/<str:pk>', views.deleteTask, name='delete'),


    path('room/<str:room_id>/members/', views.members, name='members'),
    path('room/<str:room_id>/profile/<int:user_id>/', views.profile_view, name='profile_view'),

    path('room/<str:room_id>/announcement/', views.announcement_detail, name='announcement'),
    path('room/<str:room_id>/announcement/<int:announcement_id>/', views.announcement_view, name='announcement_view'),
    path('room/<str:room_id>/announcement/<int:announcement_id>/create_comment/', views.create_comment, name='create_comment'),


    path('room/<str:room_id>/create_announcement/', views.create_announcement, name='create_announcement'),
    path('room/<str:room_id>/groupcontrib/', views.group_contrib_view, name='groupcontrib'),
    path('room/<str:room_id>/groupcontrib/new/', views.create_group_contrib, name='create_group_contrib'),
    path('room/<str:room_id>/dashboard/', views.dashboards, name='dashboard')


        

]

#path('dashboard/<str:room_id>/', views.home, name='room-home')
# path('room/<str:room_id>/bills/', views.view_member_bills, name='view-member-bills'),
# path('room/<str:room_id>/bills/<str:bills_slug>/', views.view_bills, name='view-bills'),
# path('room/<str:room_id>/bills/<str:bills_slug>/', views.delete_submission_api, name='delete-submission'),
    