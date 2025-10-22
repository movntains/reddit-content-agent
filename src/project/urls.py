"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

from snapshots.views import reddit_post_webhook_handler, snapshot_webhook_handler

urlpatterns = [
    path("admin/", admin.site.urls),
    path("qstash/webhook/", include("django_qstash.urls")),
    path("webhooks/bright_data/scrape/", snapshot_webhook_handler),
    path("webhooks/bright_data/reddit/", reddit_post_webhook_handler),
]
