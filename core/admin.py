from django.contrib import admin
from .models import Student, Announcement, Attendance, Marks, Timetable

# Customize how Student appears in admin
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'usn', 'department', 'semester')
    search_fields = ('name', 'usn')

# Customize how Announcement appears in admin
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')

# Customize how Attendance appears in admin
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'percentage')

# Customize how Marks appears in admin
@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'marks')

# Customize how Timetable appears in admin
@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('day', 'subject', 'time')