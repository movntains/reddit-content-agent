from django.db import models


class RedditPost(models.Model):
    post_id = models.CharField(max_length=120, db_index=True)
    url = models.URLField(db_index=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    comments = models.JSONField(null=True, blank=True)
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
