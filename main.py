from atproto import Client

import config
from moon import phasecalc as pc

client = Client(config.API_HOST)
client.login(config.API_USER, config.API_PASS)

phase = pc.get_current_phase()
ill = pc.get_current_illumination()

message = f"The current moon phase is {phase} with {ill:.2f}% illumination"

# print(message)
post = client.send_post(message)
# print(post) 
