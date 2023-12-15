from django.contrib import admin
from .models import Room, Admin, Member, bills, Submission, Task, Announcement, Comment, GroupContrib

admin.site.register(Room)
admin.site.register(Admin)
admin.site.register(Member)
admin.site.register(bills)
admin.site.register(Submission)
admin.site.register(Task)
admin.site.register(Announcement)
admin.site.register(Comment)
admin.site.register(GroupContrib)


# Register your models here.
