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
from .messenger_bot.views import NSFWMessengerBot
from .luftdaten.views import LuftDatenHookView
from .luftdaten.api import SensorValueAggregatedViewSet
from rest_framework import routers
from django.views.decorators.cache import cache_page
from django.conf.urls.i18n import i18n_patterns

router = routers.DefaultRouter()
router.register(r'alerts', AlertViewSet)
router.register(r'stations', StationViewSet)
router.register(r'subscriptions', SubscriptionViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^webhook', NSFWMessengerBot.as_view()),
    url(r'^luftdaten$', LuftDatenHookView.as_view()),
    url(r'^api/luftdaten$', SensorValueAggregatedViewSet.as_view()),
]

urlpatterns += i18n_patterns(
    url(r'^admin/', admin.site.urls),
    url(r'^alerts/rss/(?P<station_id>\w+)/$', cache_page(60 * 60)(RssLatestEntriesFeed())),
    url(r'^alerts/atom/(?P<station_id>\w+)/$', cache_page(60 * 60)(AtomLatestEntriesFeed())),
    url(r'^$', cache_page(60 * 60)(HomePageView.as_view())),
    url(r'^station/(?P<station_id>\w+)/$', cache_page(60 * 60)(HomePageView.as_view()), name='station'),
    url(r'^neukolln/$', cache_page(60 * 60)(HomePageView.as_view())),
    # prefix_default_language=False
)
