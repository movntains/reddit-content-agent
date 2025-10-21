from django.contrib import admin

from .models import BrightDataSnapshot


class BrightDataSnapshotAdmin(admin.ModelAdmin):
    list_display = ['snapshot_id', 'records', 'status', 'is_downloadable']
    list_filter = ['status']


admin.site.register(BrightDataSnapshot, BrightDataSnapshotAdmin)
