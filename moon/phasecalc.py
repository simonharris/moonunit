import time


# with thanks to: https://minkukel.com/en/various/calculating-moon-phase/


CYCLE_DAYS = 29.53058770576
CYCLE_SECS = CYCLE_DAYS * 24 * 60 * 60

# Datetime of first new moon in year 2000
FIRST_NEW = '2000-01-06 18:14'


# TODO: could be a dict or so for more structure
PHASES = [
    ['new', 0, 1],
    ['waxing crescent', 1, 6.38264692644],
    ['first quarter', 6.38264692644, 8.38264692644],
    ['waxing gibbous', 8.38264692644, 13.76529385288],
    ['full', 13.76529385288, 15.76529385288],
    ['waning gibbous', 15.76529385288, 21.14794077932],
    ['last quarter', 21.14794077932, 23.14794077932],
    ['waning crescent', 23.14794077932, 28.53058770576],
    ['new', 28.53058770576, 29.53058770576],
]


def get_phase(when: int) -> tuple:

    first_new = time.mktime(time.strptime(FIRST_NEW, '%Y-%m-%d %H:%M'))

    # Calculate seconds between date and new moon 2000
    total_secs = when - first_new

    current_secs = total_secs % CYCLE_SECS

    # Calculate the fraction of the moon cycle
    current_frac = current_secs / CYCLE_SECS

    # Calculate days in current cycle (moon age)
    current_days = current_frac * CYCLE_DAYS

    # Find current phase in the array
    for phase in PHASES:
        if (current_days >= phase[1]) and (current_days <= phase[2]):
            the_phase = phase[0];
            break

    return (the_phase, when)


def get_current() -> tuple:
    return get_phase(time.time())
