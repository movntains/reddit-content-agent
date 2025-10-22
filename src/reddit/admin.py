from django.contrib import admin

from .models import RedditCommunity, RedditPost


class RedditPostAdmin(admin.ModelAdmin):
    list_display = ["title", "community_name"]
    list_filter = ["community_name"]


class RedditCommunityAdmin(admin.ModelAdmin):
    list_display = ["name", "subreddit_slug", "member_count"]


admin.site.register(RedditPost, RedditPostAdmin)
admin.site.register(RedditCommunity, RedditCommunityAdmin)
