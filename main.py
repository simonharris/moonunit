import argparse
from datetime import datetime, timezone

from atproto import Client

import config
from moon import phasecalc as pc


"""
TODO: Blue moon
TODO: Harvest moon
"""

def do_phase() -> str:
    phase = pc.get_current_phase()
    ill = pc.get_current_illumination()

    message = f"The current moon phase is {phase} with {ill:.2f}% illumination."

    if phase == 'full moon':
        fm_dtl = pc.get_current_fm()
        message = message + f' Because it is {fm_dtl[0]}, the full moon is called the "{fm_dtl[1]} Moon".'

    return message


def do_rise() -> str:

    def nice_date(when):
        today = (datetime.now(timezone.utc).date() - when.date()).days == 0
        nice = when.strftime('%H:%M')

        if not today:
            nice += ' tomorrow'

        return nice

    # print(pc.get_current_rise_set())

    moon_up, ps, pr, ns, nr = pc.get_current_rise_set()

    if moon_up:
        message = f"The moon is currently above the horizon. It will set at {nice_date(ns)}."
    else:
        message = f"The moon is not currently above the horizon. It will rise at {nice_date(nr)}."
    
    return message


def do_constellation() -> str:
    const = pc.get_current_constellation()
    return f"The moon is currently in the constellation {const[0]}. {const[1]}".strip()


def send_post(message: str):
    # print(message)
    client = Client(config.API_HOST)
    client.login(config.API_USER, config.API_PASS)
    post = client.send_post(message)
    # print(post) 


# main ------------------------------------------------------------------------


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Moon Unit Bot')
    parser.add_argument('-p', '--phase', action='store_true', help='phases of the moon')
    parser.add_argument('-r', '--rise', action='store_true', help='moonrise/set')
    parser.add_argument('-s', '--stars', action='store_true', help='constellations')

    args = parser.parse_args()
   
    if args.phase:
        message = do_phase()
        # print(message)
        send_post(message)

    if args.rise:
        message = do_rise()
        # print(message)
        send_post(message)   
        
    if args.stars:
        message = do_constellation()
        # print(message)
        send_post(message)
