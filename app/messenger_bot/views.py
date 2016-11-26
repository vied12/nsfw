from wit import Wit
from django.http import HttpResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from app.nsfw.models import Station, Alert, Subscription
from .models import Messenger
import geopy.distance
from geopy.geocoders import Nominatim
import requests
import json
from django.core.cache import cache
import logging
import datetime

logger = logging.getLogger('nsfw')


class NSFWMessengerBot(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == settings.FB_VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    fb_id = message['sender']['id']
                    # We retrieve the message content
                    try:
                        text = message['message'].get('text')
                        client.run_actions(session_id=fb_id, message=text)
                    except:
                        pass
        return HttpResponse()


def fb_message(sender_id, text, quick_replies=None):
    """
    Function for returning response to messenger
    """
    data = {
        'recipient': {'id': sender_id},
        'message': {'text': text},
    }
    # Setup the query string with your PAGE TOKEN
    qs = 'access_token=' + settings.FB_PAGE_TOKEN
    # Send POST request to messenger
    if quick_replies:
        data['message']['quick_replies'] = []
        for rep in quick_replies:
            data['message']['quick_replies'].append({
                'title': rep,
                'content_type': 'text',
                'payload': rep
            })
    resp = requests.post('https://graph.facebook.com/me/messages?' + qs,
                         json=data)
    return resp.content


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
    context = request['context']
    messenger, created = Messenger.objects.get_or_create(messenger_id=request['session_id'])
    station = cache.get(request['session_id'])
    if station:
        Subscription.objects.get_or_create(messenger=messenger, station=Station.objects.get(pk=station))
        context['justSubscribed'] = created
    else:
        logger.error('Messenger Subscription. Station not known. %s' % request)
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

    for k in (
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
            del context[k]
        except KeyError:
            pass
    if not loc:
        context['missingLocation'] = True
    else:
        loc = geolocator.geocode(loc, language='en')
        if not loc:
            loc = geolocator.geocode('{}, Germany'.format(loc), language='en')
        if loc:
            # out of germany ?
            if loc.address.split(', ')[-1] != 'Germany':
                context['outOfGermany'] = True
            else:
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
actions = {
    'send': send,
    'subscribe': subscribe,
    'getAQ': get_air_quality,
}
client = Wit(access_token=settings.WIT_TOKEN, actions=actions)
