import os
from zoneinfo import ZoneInfo

API_HOST = os.environ.get('API_MOON_HOST')
API_USER = os.environ.get('API_MOON_USER')
API_PASS = os.environ.get('API_MOON_PASS')

DEBUG = False

# Bramall Lane - definitely the centre of the country, if not the world
LOC_LAT = '53.3696389'
LOC_LON = '1.4706554'
TZ_DISP = ZoneInfo('Europe/London')


