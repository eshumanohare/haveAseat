from django.contrib import admin
from . import models

class UserRoleAdmin(admin.ModelAdmin):
    list_display = ("role", "getUsername")

    def getUsername(self, userRole):
        return userRole.user.username

    getUsername.admin_order_field  = "username"
    getUsername.short_description = "Username"

admin.site.register(models.Branch)
admin.site.register(models.UserRole, UserRoleAdmin)
admin.site.register(models.Department)
admin.site.register(models.Admin)
admin.site.register(models.Student)
admin.site.register(models.DOAA)
admin.site.register(models.Faculty)
admin.site.register(models.Course)
admin.site.register(models.Announcement)