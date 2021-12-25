from django.contrib import admin

# Register your models here.
from .models import ProfileTest, IsPassedTest
from .models import Responds
from .models import Comment

admin.site.register(ProfileTest)
admin.site.register(Responds)
admin.site.register(Comment)
admin.site.register(IsPassedTest)