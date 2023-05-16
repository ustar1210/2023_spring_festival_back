from django.contrib import admin
from .models import *

admin.site.register(Booth)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(CommentReply)

admin.site.register(LogoImage)
admin.site.register(MenuImage)