from django.db import models


class RedditPost(models.Model):
    post_id = models.CharField(max_length=120, db_index=True)
    url = models.URLField(db_index=True)
    title = models.CharField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    comments = models.JSONField(null=True, blank=True)
    related_posts = models.JSONField(null=True, blank=True)
    community_name = models.CharField(max_length=250, null=True, blank=True)
    num_upvotes = models.IntegerField(null=True, blank=True)
    num_comments = models.IntegerField(null=True, blank=True)
    date_posted = models.DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
    )

    def __str__(self):
        if not self.title:
            return f"{self.url}"

        return f"{self.title}"


class RedditCommunity(models.Model):
    url = models.URLField(
        db_index=True, help_text="The complete URL of the Reddit community"
    )
    name = models.TextField(
        null=True, blank=True, help_text="Formatted name for Reddit"
    )
    subreddit_slug = models.CharField(
        max_length=400,
        null=True,
        blank=True,
        help_text="The slug of the subreddit, such as r/Python, r/web, or r/trending",
    )
    member_count = models.IntegerField(
        null=True, blank=True, help_text="Current member count, if available"
    )
    active = models.BooleanField(default=True, help_text="Is this searchable?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
