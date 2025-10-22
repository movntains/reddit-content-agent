import json

import requests
from django.conf import settings

from . import defaults

BRIGHT_DATA_DATASET_ID = "gd_lvz8ah06191smkebj4"


def get_crawl_headers():
    return {
        "Authorization": f"Bearer {settings.BRIGHT_DATA_API_KEY}",
        "Content-Type": "application/json",
    }


def perform_scrape_snapshot(
    subreddit_url: str,
    num_of_posts: int = 20,
    raw: bool = False,
    use_webhook: bool = True,
    sort_by_time: str = "This Week",
) -> dict | bool:
    url = "https://api.brightdata.com/datasets/v3/trigger"
    headers = get_crawl_headers()
    params = {
        "dataset_id": BRIGHT_DATA_DATASET_ID,
        "notify": "false",
        "include_errors": "true",
        "type": "discover_new",
        "discover_by": "subreddit_url",
        "limit_per_input": "100",
    }

    if use_webhook:
        webhook_params = {
            "auth_header": f"Basic {settings.BRIGHT_DATA_WEBHOOK_HANDLER_SECRET_KEY}",
            "endpoint": f"{settings.CLOUDFLARE_TUNNEL_URL}/webhooks/bright_data/reddit/",
            "notify": f"{settings.CLOUDFLARE_TUNNEL_URL}/webhooks/bright_data/scrape/",
            "format": "json",
            "uncompressed_webhook": "true",
            "force_deliver": "false",
        }

        params.update(webhook_params)

    fields = defaults.BRIGHT_DATA_REDDIT_FIELDS
    ignore_fields = []
    sort_options = ["Today", "This Week", "This Month", "All Time"]

    if sort_by_time not in sort_options:
        sort_by_time = "This Month"

    data = json.dumps(
        {
            "input": [
                {
                    "url": f"{subreddit_url}",
                    "sort_by": "Top",
                    "sort_by_time": f"{sort_by_time}",
                    "num_of_posts": num_of_posts,
                },
            ],
            "custom_output_fields": [x for x in fields if not x in ignore_fields],
        }
    )

    response = requests.post(
        url=url,
        headers=headers,
        params=params,
        data=data,
    )

    response.raise_for_status()

    response_data = response.json()

    if raw:
        return response_data

    return response_data.get("snapshot_id")


def get_snapshot_progress(snapshot_id: str, raw: bool = False) -> dict | bool | None:
    url = f"https://api.brightdata.com/datasets/v3/progress/{snapshot_id}"
    headers = get_crawl_headers()

    try:
        response = requests.get(url=url, headers=headers)

        response.raise_for_status()

        data = response.json()

        if raw:
            return data

        status = data.get("status")

        return status == "ready"

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def download_snapshot(snapshot_id: str) -> dict[str, str] | None:
    url = f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}"
    headers = get_crawl_headers()
    params = {
        "format": "json",
    }

    try:
        response = requests.get(url=url, headers=headers, params=params)

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
