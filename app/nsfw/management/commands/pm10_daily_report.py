from app.nsfw.management.uma import UmaCommand


class Command(UmaCommand):
    help = 'Get a PM10 daily report'
    pollutant = 'PM1'
    data_type = '1TMW'
