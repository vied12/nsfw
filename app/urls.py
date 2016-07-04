"""nsfw URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from .nsfw.feeds import RssLatestEntriesFeed, AtomLatestEntriesFeed
from .nsfw.views import HomePageView
from .nsfw.api import AlertViewSet, StationViewSet, SubscriptionViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'alerts', AlertViewSet)
router.register(r'stations', StationViewSet)
router.register(r'subscriptions', SubscriptionViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^alerts/rss/(?P<station_id>\w+)/$', RssLatestEntriesFeed()),
    url(r'^alerts/atom/(?P<station_id>\w+)/$', AtomLatestEntriesFeed()),
    url(r'^$', HomePageView.as_view()),
    url(r'^station/(?P<station_id>\w+)/$', HomePageView.as_view()),

]
