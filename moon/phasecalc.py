from datetime import datetime, timezone
import time
from zoneinfo import ZoneInfo

import ephem

from .data import CONSTELLATIONS, FM_NAMES, PHASES

CYCLE_DAYS = 29.53058770576
CYCLE_SECS = CYCLE_DAYS * 24 * 60 * 60

# Bramall Lane - definitely the centre of the country, if not the world
LOC_LAT = '53.3696389'
LOC_LON = '1.4706554'

# Datetime of first new moon in year 2000
FIRST_NEW = '2000-01-06 18:14'

TZ_DISP = ZoneInfo('Europe/London')


def _get_dt_utc():
    """
    Pyephem speaks UTC, so we work with that throughout, formatting to UK time
    for display
    """
    return datetime.now(timezone.utc)


def get_phase(when: datetime) -> str:
    """
    With thanks to Minkukel Plus:
    https://minkukel.com/en/various/calculating-moon-phase/
    """

    first_new = time.mktime(time.strptime(FIRST_NEW, '%Y-%m-%d %H:%M'))

    # Calculate seconds between date and new moon 2000
    total_secs = when.timestamp() - first_new

    current_secs = total_secs % CYCLE_SECS

    # Calculate the fraction of the moon cycle
    current_frac = current_secs / CYCLE_SECS

    # Calculate days in current cycle (moon age)
    current_days = current_frac * CYCLE_DAYS

    # Find current phase in the array
    for phase in PHASES:
        if (current_days >= phase[1]) and (current_days <= phase[2]):
            the_phase = phase[0]
            break

    return the_phase


def get_current_phase() -> str:
    return get_phase(_get_dt_utc())


def get_illumination(when: datetime) -> float:
    return ephem.Moon(when).moon_phase * 100


def get_current_illumination() -> float:
    return get_illumination(_get_dt_utc())


def get_fm(when: datetime) -> tuple:
    return (when.strftime('%B'), FM_NAMES[when.strftime('%m')])


def get_current_fm() -> tuple:
    return get_fm(_get_dt_utc())


def get_rise_set(when: datetime):

    bdtbl = ephem.Observer()
    bdtbl.date = when
    bdtbl.lat = LOC_LAT
    bdtbl.lon = LOC_LON
    moon = ephem.Moon()

    ps = ephem.to_timezone(bdtbl.previous_setting(moon, start=when), TZ_DISP)
    pr = ephem.to_timezone(bdtbl.previous_rising(moon, start=when), TZ_DISP)
    ns = ephem.to_timezone(bdtbl.next_setting(moon, start=when), TZ_DISP)
    nr = ephem.to_timezone(bdtbl.next_rising(moon, start=when), TZ_DISP)

    is_up = pr > ps

    return (is_up, ps, pr, ns, nr)


def get_current_rise_set() -> tuple:
    return get_rise_set(_get_dt_utc())


def get_constellation(when: datetime) -> tuple:
    moon = ephem.Moon(when)
    con_name = ephem.constellation(moon)[1]
    con_name = con_name.replace('Scorpius', 'Scorpio')
    con_name = con_name.replace('Capricornus', 'Capricorn')

    return (con_name, CONSTELLATIONS[con_name]['desc'])


def get_current_constellation() -> tuple:
    return get_constellation(_get_dt_utc())
