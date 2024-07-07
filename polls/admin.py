from django.contrib import admin
from .models import Poll
from .models import Vote

# Register your models here.
admin.site.register(Poll)
admin.site.register(Vote)