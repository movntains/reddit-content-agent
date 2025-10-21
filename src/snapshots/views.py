import json

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import helpers.bright_data
from reddit import services as reddit_db_services
from .models import BrightDataSnapshot
from .tasks import get_snapshot_instance_progress_task


@csrf_exempt
def snapshot_webhook_handler(request):
    if request.method != 'POST':
        # Intentionally not indicating that a POST request is required for security reasons
        return HttpResponse('OK')

    auth = request.headers.get('Authorization')

    if auth.startswith('Basic '):
        token = auth.split(' ')[1]

        if token == f"{settings.BRIGHT_DATA_WEBHOOK_HANDLER_SECRET_KEY}":
            data = {}

            try:
                data = json.loads(request.body.decode('utf-8'))

            except json.decoder.JSONDecodeError as e:
                print(f"Error: {e.msg}")

            snapshot_id = data.get('snapshot_id')

            if snapshot_id:
                query_set = BrightDataSnapshot.objects.filter(
                    snapshot_id=snapshot_id,
                    dataset_id=helpers.bright_data.BRIGHT_DATA_DATASET_ID,
                )

                if not query_set.exists():
                    instance = BrightDataSnapshot.objects.create(
                        snapshot_id=snapshot_id,
                        dataset_id=helpers.bright_data.BRIGHT_DATA_DATASET_ID,
                    )

                    get_snapshot_instance_progress_task(instance.id)
                else:
                    instance_ids = query_set.values_list('id', flat=True)

                    for instance_id in instance_ids:
                        get_snapshot_instance_progress_task(instance_id)

    return HttpResponse('OK')


@csrf_exempt
def reddit_post_webhook_handler(request):
    if request.method != 'POST':
        # Intentionally not indicating that a POST request is required for security reasons
        return HttpResponse('OK')

    auth = request.headers.get('Authorization')

    if auth.startswith('Basic '):
        token = auth.split(' ')[1]

        if token == f"{settings.BRIGHT_DATA_WEBHOOK_HANDLER_SECRET_KEY}":
            data = []

            try:
                data = json.loads(request.body.decode('utf-8'))

            except json.decoder.JSONDecodeError as e:
                print(f"Error: {e.msg}")

            reddit_db_services.handle_reddit_thread_results(reddit_results=data)

    return HttpResponse('OK')
