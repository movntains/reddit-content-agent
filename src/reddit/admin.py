from django.contrib import admin

from .models import RedditPost


class RedditPostAdmin(admin.ModelAdmin):
    list_display = ["title", "community_name"]
    list_filter = ["community_name"]


admin.site.register(RedditPost, RedditPostAdmin)
