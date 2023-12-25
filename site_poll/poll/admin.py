from django.contrib import admin
from poll.models import *

from poll.models import User
from poll.models import Poll

# Register your models here.

admin.site.register(User)
admin.site.register(Poll)


