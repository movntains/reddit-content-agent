from django.db import models


class BrightDataSnapshot(models.Model):
    snapshot_id = models.CharField(max_length=120)
    dataset_id = models.CharField(max_length=120)
    status = models.CharField(max_length=120)
    error_message = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    records = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.snapshot_id

    @property
    def is_downloadable(self) -> bool:
        if self.error_message:
            return False

        return self.status == 'ready' and self.records > 0
