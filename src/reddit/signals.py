from django.db.models.signals import post_save

from . import services as reddit_db_services
from .models import RedditCommunity


def reddit_community_post_save_receiver(sender, instance, created, *args, **kwargs):
    reddit_db_services.handle_reddit_community_scrape_automation(
        instance=instance,
        created=created,
        force_scrape=False,
        verbose=True,
    )


post_save.connect(receiver=reddit_community_post_save_receiver, sender=RedditCommunity)
