from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
import json
import base64
from .models import SensorValue


class LuftDatenHookView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        known_keys = (
            settings.LUFTDATEN_BASIC_AUTH1,
            settings.LUFTDATEN_BASIC_AUTH2,
        )
        known_keys_encoded = [('Basic %s' % (base64.b64encode(k.encode('ascii')).decode())) for k in known_keys]
        assert request.META['HTTP_AUTHORIZATION'] in known_keys_encoded
        data = json.loads(request.body.decode('utf-8'))
        wanted_data = [
            'SDS_P1',
            'SDS_P2',
            'temperature',
            'humidity',
            'samples',
            'min_micro',
            'max_micro',
            'signal',
        ]
        data = [d for d in data['sensordatavalues'] if d['value_type'] in wanted_data]
        data = {d['value_type']: d['value'] for d in data}
        device = str(known_keys_encoded.index(request.META['HTTP_AUTHORIZATION']))
        SensorValue.objects.create(device=device, **data)
        return HttpResponse('ok')
