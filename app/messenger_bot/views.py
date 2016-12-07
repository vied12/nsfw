from django.http import HttpResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from app.nsfw.models import Station, Subscription
from .models import Messenger
from django.conf import settings
import json
import logging
from .wit import get_client

logger = logging.getLogger('nsfw')

wit_client = get_client()


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
            for message in entry.get('messaging', []):
                # save id
                messenger, created = Messenger.objects.get_or_create(messenger_id=message['sender']['id'])
                # subscribe
                if 'optin' in message:
                    try:
                        station = message['optin']['ref']
                        Subscription.objects.get_or_create(messenger=messenger, station=Station.objects.get(pk=station))
                    except Exception as e:
                        logger.error('ERROR %s' % e)
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    fb_id = message['sender']['id']
                    # We retrieve the message content
                    try:
                        text = message['message'].get('text')
                        wit_client.run_actions(session_id=fb_id, message=text)
                    except:
                        pass
        return HttpResponse()
