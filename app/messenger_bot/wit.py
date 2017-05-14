from wit import Wit
from app.nsfw.models import Station, Alert, Subscription
from .models import Messenger
import geopy.distance
from geopy.geocoders import Nominatim
from django.core.cache import cache
import datetime
from django.conf import settings
import logging
from .facebook import fb_message

logger = logging.getLogger('nsfw')


def first_entity_value(entities, entity):
    """
    Returns first entity value
    """
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val


def send(request, response):
    """
    Sender function
    """
    # We use the fb_id as equal to session_id
    fb_id = request['session_id']
    text = response['text'].decode('utf8')
    # send message
    fb_message(fb_id, text, response.get('quickreplies'))


def get_closest_station(lat, lon):
    closest = None
    for station in Station.objects.all():
        d = geopy.distance.distance((station.lat, station.lon), (lat, lon)).km
        if closest is None or closest['d'] > d:
            closest = {'station': station, 'd': d}
    return closest['station']


def subscribe(request):
    request['context'] = {}
    context = request['context']
    messenger, created = Messenger.objects.get_or_create(messenger_id=request['session_id'])
    station = cache.get(request['session_id'])
    if station:
        Subscription.objects.get_or_create(messenger=messenger, station=Station.objects.get(pk=station))
        context['justSubscribed'] = created
    else:
        logger.error('Messenger Subscription: Station not known. %s' % request)
        context['noStation'] = True
    return context


def is_subscribed(session_id, station):
    try:
        messenger = Messenger.objects.get(messenger_id=session_id)
        return Subscription.objects.filter(
            messenger=messenger,
            station=station
        ).exists()
    except (Messenger.DoesNotExist, Subscription.DoesNotExist):
        return False


def get_air_quality(request):
    geolocator = Nominatim()
    context = request['context']
    entities = request['entities']
    loc = first_entity_value(entities, 'location')

    for context_key in (
        'missingLocation',
        'outOfGermany',
        'subscribed',
        'notSubscribed',
        'location',
        'station',
        'stationId',
        'lastAlertValue',
        'lastAlertDate',
        'kind',
        'clean',
        'notFound',
    ):
        try:
            del context[context_key]
        except KeyError:
            pass
    if not loc:
        context['missingLocation'] = True
    else:
        loc = geolocator.geocode(loc, language='en')
        if not loc:
            loc = geolocator.geocode('{}, Germany'.format(loc), language='en')
        if loc:
            closest_station = get_closest_station(loc.latitude, loc.longitude)
            # is subscribed ?
            if is_subscribed(request['session_id'], closest_station):
                context['subscribed'] = True
            else:
                context['notSubscribed'] = True
            # oldest alert we want
            max_date = datetime.datetime.now() - datetime.timedelta(days=2)
            last_alert = Alert.objects.filter(station=closest_station, report__date__gte=max_date).last()
            context['location'] = loc.address
            context['station'] = closest_station.name
            context['stationId'] = closest_station.pk
            cache.set(request['session_id'], closest_station.pk)
            if last_alert:
                context['lastAlertValue'] = last_alert.value
                context['lastAlertDate'] = last_alert.report.date.strftime('%x')
                context['kind'] = last_alert.report.kind
            else:
                context['clean'] = True
        else:
            context['notFound'] = True
    return context


# Setup Actions
ACTIONS = {
    'send': send,
    'subscribe': subscribe,
    'getAQ': get_air_quality,
}


def get_client(send=None):
    actions = ACTIONS.copy()
    if send:
        actions['send'] = send
    return Wit(access_token=settings.WIT_TOKEN, actions=actions)
