import requests
from django.conf import settings
import logging

logger = logging.getLogger('nsfw')


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
