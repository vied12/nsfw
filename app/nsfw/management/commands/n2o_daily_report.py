from app.nsfw.management.uma import UmaCommand


class Command(UmaCommand):
    help = 'Get a NO2 daily report'
    pollutant = 'NO2'
    data_type = '1TMAX'
