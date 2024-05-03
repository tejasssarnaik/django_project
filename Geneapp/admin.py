from django.contrib import admin
from .models import UserProfile,Workflow,UserHistory,IDCounter,Project

# Register UserProfile model
admin.site.register(UserProfile)
admin.site.register(Workflow)
admin.site.register(UserHistory)
admin.site.register(IDCounter)
admin.site.register(Project)




