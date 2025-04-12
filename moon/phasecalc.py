from datetime import datetime
import time 

import ephem


CYCLE_DAYS = 29.53058770576
CYCLE_SECS = CYCLE_DAYS * 24 * 60 * 60

# Bramall Lane - definitely the centre of the country, if not the world
LOC_LAT = '53.3696389'
LOC_LON = '1.4706554'

# Datetime of first new moon in year 2000
FIRST_NEW = '2000-01-06 18:14'

PHASES = [
    ['new moon', 0, 1],
    ['waxing crescent', 1, 6.38264692644],
    ['first quarter', 6.38264692644, 8.38264692644],
    ['waxing gibbous', 8.38264692644, 13.76529385288],
    ['full moon', 13.76529385288, 15.76529385288],
    ['waning gibbous', 15.76529385288, 21.14794077932],
    ['last quarter', 21.14794077932, 23.14794077932],
    ['waning crescent', 23.14794077932, 28.53058770576],
    ['new moon', 28.53058770576, 29.53058770576],
]

# https://www.rmg.co.uk/stories/topics/what-are-names-full-moons-throughout-year
FM_NAMES = {
    '01': 'Wolf',
    '02': 'Snow',
    '03': 'Worm',
    '04': 'Pink',
    '05': 'Flower',
    '06': 'Strawberry',
    '07': 'Buck',
    '08': 'Sturgeon',
    '09': 'Full Corn',
    '10': 'Hunter\'s ',
    '11': 'Beaver',
    '12': 'Cold',
}


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
    return get_phase(datetime.now())


def get_illumination(when: datetime) -> float:
    return ephem.Moon(when).moon_phase * 100


def get_current_illumination() -> float:
    return get_illumination(datetime.now())


def get_fm(when: datetime) -> tuple:
    return (when.strftime('%B'), FM_NAMES[when.strftime('%m')])


def get_current_fm() -> tuple:
    return get_fm(datetime.now())


def get_rise_set(when: datetime):

    whenf = when.strftime('%Y/%m/%d')

    obs = ephem.Observer()
    obs.date = whenf
    obs.lat = LOC_LAT
    obs.lon = LOC_LON
    moon = ephem.Moon()

    # ps = obs.previous_setting(moon) 
    # pr = obs.previous_rising(moon)
    # ns = obs.next_setting(moon)
    nr = obs.next_rising(moon, start='2025/04/12')

    is_up = False

    return (is_up, nr,) #ps, pr, ns, nr)


def get_current_rise_set() -> tuple:
    return get_rise_set(datetime.now())


# >>> m = ephem.Moon('1980/6/1')
# >>> print(ephem.constellation(m))
# ('Sgr', 'Sagittarius')