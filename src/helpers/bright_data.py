import json

import requests
from django.apps import apps
from django.conf import settings

BRIGHT_DATA_DATASET_ID = 'gd_lvz8ah06191smkebj4'


def get_crawl_headers():
    return {
        'Authorization': f"Bearer {settings.BRIGHT_DATA_API_KEY}",
        'Content-Type': 'application/json',
    }


def perform_scrape_snapshot(subreddit_url: str, num_of_posts: int = 20) -> str:
    BrightDataSnapshot = apps.get_model('snapshots', 'BrightDataSnapshot')
    url = 'https://api.brightdata.com/datasets/v3/trigger'
    headers = get_crawl_headers()
    dataset_id = 'gd_lvz8ah06191smkebj4'
    params = {
        'dataset_id': BRIGHT_DATA_DATASET_ID,
        'notify': 'false',
        'include_errors': 'true',
        'type': 'discover_new',
        'discover_by': 'subreddit_url',
        'limit_per_input': '100',
    }
    data = json.dumps({
        'input': [
            {
                'url': f"{subreddit_url}",
                'sort_by': 'Top',
                'sort_by_time': 'Today',
                'num_of_posts': num_of_posts,
            },
        ],
    })

    response = requests.post(
        url=url,
        headers=headers,
        params=params,
        data=data,
    )

    response.raise_for_status()

    data = response.json()
    snapshot_id = data.get('snapshot_id')

    BrightDataSnapshot.objects.create(
        snapshot_id=snapshot_id,
        dataset_id=dataset_id,
        status='Unknown',
        url=subreddit_url,
    )

    return data.get('snapshot_id')


def get_snapshot_progress(snapshot_id: str) -> bool | None:
    BrightDataSnapshot = apps.get_model('snapshots', 'BrightDataSnapshot')
    url = f"https://api.brightdata.com/datasets/v3/progress/{snapshot_id}"
    headers = get_crawl_headers()

    try:
        response = requests.get(url=url, headers=headers)

        response.raise_for_status()

        data = response.json()
        snapshot_id = data.get('snapshot_id')
        dataset_id = data.get('dataset_id')
        status = data.get('status')
        records = data.get('records') or 0

        BrightDataSnapshot.objects.update_or_create(
            snapshot_id=snapshot_id,
            dataset_id=dataset_id,
            defaults={
                'status': status,
                'records': records,
            },
        )

        return status == 'ready'

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def download_snapshot(snapshot_id: str) -> dict[str, str] | None:
    BrightDataSnapshot = apps.get_model('snapshots', 'BrightDataSnapshot')
    url = f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}"
    headers = get_crawl_headers()
    params = {
        'format': 'json',
    }

    try:
        response = requests.get(url=url, headers=headers, params=params)
        message = response.text

        if response.status_code not in range(200, 299):
            query_set = BrightDataSnapshot.objects.filter(
                dataset_id=BRIGHT_DATA_DATASET_ID,
                snapshot_id=snapshot_id,
            )

            query_set.update(error_message=message)

            return {}

        if message.lower() == 'snapshot is empty':
            return {}

        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
