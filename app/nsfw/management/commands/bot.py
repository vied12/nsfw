from django.core.management.base import BaseCommand
from app.messenger_bot.wit import get_client
import logging


class Command(BaseCommand):
    help = 'Starts an interactive conversation with the bot.'

    def add_arguments(self, parser):
        parser.add_argument('--debug', help='debug logs', action='store_const', const=True)

    def send(self, request, response):
        text = response['text'].decode('utf8')
        print(text)

    def handle(self, *args, **options):
        wit_client = get_client(send=self.send)
        if options['debug']:
            wit_client.logger.setLevel(logging.DEBUG)
        wit_client.interactive()
