import os
import time

import paho.mqtt.client as mqtt

from telegram.bot import Bot
from telegram.parsemode import ParseMode

# initializing the bot with API_KEY and CHAT_ID
if os.getenv('TELEGRAM_BOT_API_KEY') == None:
    print("Error: Please set the environment variable TELEGRAM_BOT_API_KEY and try again.")
    exit(1)
bot = Bot(os.getenv('TELEGRAM_BOT_API_KEY'))

if os.getenv('TELEGRAM_BOT_CHAT_ID') == None:
    print("Error: Please set the environment variable TELEGRAM_BOT_CHAT_ID and try again.")
    exit(1)
chat_id = os.getenv('TELEGRAM_BOT_CHAT_ID')

# based on example from https://pypi.org/project/paho-mqtt/
# The callback for when the client receives a CONNACK response from the server.

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    if rc == 0:
        print("Connected successfully to broker")
    else:
        print("Connection failed")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

    # Multi Level Subscription
    client.subscribe("teslamate/cars/#", 0)

# The callback for when a PUBLISH message is received from the server.

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload.decode()))
    title = msg.topic
    value = str(msg.payload.decode())
    # Check Teslamate MQTT Topics based on https://docs.teslamate.org/docs/integrations/mqtt
    if msg.topic == "teslamate/cars/1/display_name":
        title = "<b>Display Name</b> : "
    elif msg.topic == "teslamate/cars/1/state":
        title = "<b>State</b> : "
    elif msg.topic == "teslamate/cars/1/since":
        title = "<b>Since</b> : "
    elif msg.topic == "teslamate/cars/1/healthy":
        title = "<b>Healthy</b> : "
    elif msg.topic == "teslamate/cars/1/version":
        title = "<b>Version</b> : "
    elif msg.topic == "teslamate/cars/1/update_available":
        title = "<b>State</b> : "
    elif msg.topic == "teslamate/cars/1/update_version":
        title = "<b>Update Version</b> : "
    elif msg.topic == "teslamate/cars/1/model":
        title = "<b>Model</b> : "
    elif msg.topic == "teslamate/cars/1/trim_badging":
        title = "<b>Trim Badging</b> : "
    elif msg.topic == "teslamate/cars/1/exterior_color":
        title = "<b>Exterior Color</b> : "
    elif msg.topic == "teslamate/cars/1/wheel_type":
        title = "<b>Wheel Type</b> : "
    elif msg.topic == "teslamate/cars/1/spoiler_type":
        title = "<b>Spoiler Type</b> : "
    elif msg.topic == "teslamate/cars/1/geofence":
        title = "<b>Geofence</b> : "
    elif msg.topic == "teslamate/cars/1/latitude":
        title = "<b>latitude</b> : "
    elif msg.topic == "teslamate/cars/1/longitude":
        title = "<b>Longitude</b> : "
    elif msg.topic == "teslamate/cars/1/shift_state":
        title = "<b>Shift State</b> : "
    elif msg.topic == "teslamate/cars/1/power":
        title = "<b>Power</b> : "
    elif msg.topic == "teslamate/cars/1/speed":
        title = "<b>Speed</b> : "
    elif msg.topic == "teslamate/cars/1/heading":
        title = "<b>Heading</b> : "
    elif msg.topic == "teslamate/cars/1/elevation":
        title = "<b>Elevation</b> : "
    elif msg.topic == "teslamate/cars/1/locked":
        title = "<b>Locked</b> : "
    elif msg.topic == "teslamate/cars/1/sentry_mode":
        title = "<b>Sentry Mode</b> : "
    elif msg.topic == "teslamate/cars/1/windows_open":
        title = "<b>Windows Open</b> : "
    elif msg.topic == "teslamate/cars/1/doors_open":
        title = "<b>Doors Open</b> : "
    elif msg.topic == "teslamate/cars/1/trunk_open":
        title = "<b>Trunk Open</b> : "
    elif msg.topic == "teslamate/cars/1/frunk_open":
        title = "<b>Frunk Open</b> : "
    elif msg.topic == "teslamate/cars/1/is_user_present":
        title = "<b>Is User Present</b> : "
    elif msg.topic == "teslamate/cars/1/is_climate_on":
        title = "<b>Is Climate On</b> : "
    elif msg.topic == "teslamate/cars/1/inside_temp":
        title = "<b>Inside Temp</b> : "
    elif msg.topic == "teslamate/cars/1/outside_temp":
        title = "<b>Outside Temp</b> : "
    elif msg.topic == "teslamate/cars/1/is_preconditioning":
        title = "<b>Is Preconditioning</b> : "
    elif msg.topic == "teslamate/cars/1/odometer":
        title = "<b>Odometer</b> : "
    elif msg.topic == "teslamate/cars/1/est_battery_range_km":
        title = "<b>Est Battery Range Km</b> : "
    elif msg.topic == "teslamate/cars/1/rated_battery_range_km":
        title = "<b>Rated Battery Range Km</b> : "
    elif msg.topic == "teslamate/cars/1/ideal_battery_range_km":
        title = "<b>Ideal Battery Range Km</b> : "
    elif msg.topic == "teslamate/cars/1/battery_level":
        title = "<b>Battery Level</b> : "
    elif msg.topic == "teslamate/cars/1/usable_battery_level":
        title = "<b>Usable Battery Level</b> : "
    elif msg.topic == "teslamate/cars/1/plugged_in":
        title = "<b>Plugged In</b> : "
    elif msg.topic == "teslamate/cars/1/charge_energy_added":
        title = "<b>Charge Energy Added</b> : "
    elif msg.topic == "teslamate/cars/1/charge_limit_soc":
        title = "<b>Charge Limit</b> : "
    elif msg.topic == "teslamate/cars/1/charge_port_door_open":
        title = "<b>Charge Port Door Open</b> : "
    elif msg.topic == "teslamate/cars/1/charger_actual_current":
        title = "<b>Charger Actual Current</b> : "
    elif msg.topic == "teslamate/cars/1/charger_phases":
        title = "<b>Charger Phases</b> : "
    elif msg.topic == "teslamate/cars/1/charger_power":
        title = "<b>Charger Power</b> : "
    elif msg.topic == "teslamate/cars/1/charger_voltage":
        title = "<b>Charger Voltage</b> : "
    elif msg.topic == "teslamate/cars/1/scheduled_charging_start_time":
        title = "<b>Scheduled Charging Start Time</b> : "
    elif msg.topic == "teslamate/cars/1/time_to_full_charge":
        title = "<b>Time To Full Charge</b> : "

    bot.send_message(
        chat_id,
        text = title + value,
        parse_mode=ParseMode.HTML,
    )

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set
if os.getenv('MQTT_BROKER_USERNAME') == None:
    pass
else:
    if os.getenv('MQTT_BROKER_PASSWORD') == None:
        client.username_pw_set(os.getenv('MQTT_BROKER_USERNAME', ''))
    else:
        client.username_pw_set(os.getenv('MQTT_BROKER_USERNAME', ''), os.getenv('MQTT_BROKER_PASSWORD', ''))

client.connect(os.getenv('MQTT_BROKER_HOST', '127.0.0.1'),
               int(os.getenv('MQTT_BROKER_PORT', 1883)), 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#client.loop_forever()

client.loop_start()  # start the loop
try:
    bot.send_message(
            chat_id,
            text="<b>"+"YOUR_BOT_NAME"+"</b>\n"+"I'm here!!! :)",
            parse_mode=ParseMode.HTML,
        )

    while True:

        time.sleep(1)

except KeyboardInterrupt:

    print("exiting")


client.disconnect()

client.loop_stop()
