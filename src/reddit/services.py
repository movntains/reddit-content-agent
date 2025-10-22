from datetime import timedelta
from functools import lru_cache

from django.utils import timezone

import helpers.bright_data
from snapshots.tasks import perform_reddit_scrape_task
from .models import RedditCommunity, RedditPost


@lru_cache
def get_valid_reddit_post_fields() -> list[str]:
    model_field_names = [field.name for field in RedditPost._meta.get_fields()]
    skip_fields = ["id", "post_id", "url"]
    valid_fields = [x for x in model_field_names if x not in skip_fields]

    return valid_fields


def handle_reddit_thread_results(reddit_results: list = []) -> list[str]:
    valid_fields = get_valid_reddit_post_fields()
    ids = []

    print(reddit_results)

    for thread in reddit_results:
        post_id = thread.get("post_id")
        url = thread.get("url")

        if not all([url, post_id]):
            continue

        update_data = {k: v for k, v in thread.items() if k in valid_fields}

        instance, _ = RedditPost.objects.update_or_create(
            post_id=post_id,
            url=url,
            defaults=update_data,
        )

        ids.append(instance.id)

    return ids


def handle_reddit_community_scrape_automation(
    instance, created: bool = False, force_scrape: bool = False, verbose: bool = False
):
    url = instance.url
    active = instance.active

    if not active and not force_scrape:
        return

    now = timezone.now()
    last_scrape_event = instance.last_scrape_event
    min_last_event_delta = timedelta(minutes=5)

    if last_scrape_event is not None:
        last_event_delta = now - last_scrape_event
        scrape_ready = last_event_delta > min_last_event_delta
    else:
        scrape_ready = True

    if force_scrape:
        scrape_ready = True

    if verbose:
        print("Ready to scrape", scrape_ready, instance.url)
        print("Was just created", created)

    query_set = RedditCommunity.objects.filter(pk=instance.pk)

    query_set.update(last_scrape_event=now)

    if scrape_ready and not created:
        if verbose:
            print("Trigger Reddit community post scrape update")

        perform_reddit_scrape_task.delay(
            subreddit_url=url,
            num_of_posts=5,
            progress_countdown=300,
            sort_by_time="This Week",
        )

    if created:
        if verbose:
            print("First pass Reddit Community run")

        for sort_by in helpers.bright_data.BRIGHT_DATA_SCRAPE_SORT_OPTIONS:
            perform_reddit_scrape_task.delay(
                subreddit_url=url,
                num_of_posts=5,
                progress_countdown=300,
                sort_by_time=sort_by,
            )

    if verbose:
        print("--- DONE ---\n")
