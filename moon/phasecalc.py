import math
import time


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
    """
    With thanks to Minkukel Plus:
    https://minkukel.com/en/various/calculating-moon-phase/
    """

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
            the_phase = phase[0]
            break

    return (the_phase, when)


def get_current_phase() -> tuple:
    return get_phase(time.time())


def get_illumination(when: int):
    """
    With thanks to Greg Miller:
    https://celestialprogramming.com/meeus-illuminated_fraction_of_the_moon.html
    """

    def JulianDateFromUnixTime(t):
        # Not valid for dates before Oct 15, 1582
        return (t / 86400000) + 2440587.5

    # def UnixTimeFromJulianDate(jd):
    #     //Not valid for dates before Oct 15, 1582
    #     return (jd-2440587.5)*86400000

    def constrain(d):
        t = d % 360
        if t < 0:
            t += 360
        return t

    jd = JulianDateFromUnixTime(when)

    toRad = math.pi/180.0
    T = (jd - 2451545) / 36525.0

    D = constrain(297.8501921 + 445267.1114034*T - 0.0018819*T*T + 1.0/545868.0*T*T*T - 1.0/113065000.0*T*T*T*T) * toRad # 47.2
    M = constrain(357.5291092 + 35999.0502909*T - 0.0001536*T*T + 1.0/24490000.0*T*T*T) * toRad  # 47.3
    Mp = constrain(134.9633964 + 477198.8675055*T + 0.0087414*T*T + 1.0/69699.0*T*T*T - 1.0/14712000.0*T*T*T*T) * toRad #47.4

    # 48.4
    i = constrain(180 - D*180/math.pi - 6.289 * math.sin(Mp) + 2.1 * math.sin(M) -1.274 * math.sin(2*D - Mp) -0.658 * math.sin(2*D) -0.214 * math.sin(2*Mp) -0.11 * math.sin(D)) * toRad

    k = ( 1 + math.cos(i) ) / 2
    return k * 100


def get_current_illumination() -> int:
    return get_illumination(time.time())
