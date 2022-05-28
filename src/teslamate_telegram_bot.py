import os
import time

import paho.mqtt.client as mqtt

from telegram.bot import Bot
from telegram.parsemode import ParseMode

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

import teslapy

# https://github.com/tdorssers/TeslaPy
# cache.json can be generated after Browser SSO authentication via cli.py of TeslPy
tesla_cache_file = '/app/src/cache.json'

# initializing the bot with API_KEY and CHAT_ID
if os.getenv('TELEGRAM_BOT_API_KEY') == None:
    print("Error: Please set the environment variable TELEGRAM_BOT_API_KEY and try again.")
    exit(1)
bot = Bot(os.getenv('TELEGRAM_BOT_API_KEY'))

if os.getenv('TELEGRAM_BOT_CHAT_ID') == None:
    print("Error: Please set the environment variable TELEGRAM_BOT_CHAT_ID and try again.")
    exit(1)
chat_id = os.getenv('TELEGRAM_BOT_CHAT_ID')

# Initialization
display_name = None
state = None
since = None
healthy = None
version = None
charger_phases = None
update_version = None
model = None
trim_badging = None
exterior_color = None
wheel_type = None
spoiler_type = None
geofence = None
latitude = None
longitude = None
shift_state = None
power = None
speed = None
heading = None
elevation = None
locked = None
sentry_mode = None
windows_open = None
doors_open = None
trunk_open = None
frunk_open = None
is_user_present = None
is_climate_on = None
inside_temp = None
outside_temp = None
is_preconditioning = None
odometer = None
est_battery_range_km = None
rated_battery_range_km = None
ideal_battery_range_km = None
battery_level = None
usable_battery_level = None
plugged_in = None
charge_energy_added = None
charge_limit_soc = None
charge_port_door_open = None
charger_actual_current = None
charger_phases = None
charger_power = None
charger_voltage = None
charge_current_request = None
charge_current_request_max = None
scheduled_charging_start_time = None
time_to_full_charge = None

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

    global display_name
    global state
    global since
    global healthy
    global version
    global update_available
    global update_version
    global model
    global trim_badging
    global exterior_color
    global wheel_type
    global spoiler_type
    global geofence
    global latitude
    global longitude
    global shift_state
    global power
    global speed
    global heading
    global elevation
    global locked
    global sentry_mode
    global windows_open
    global doors_open
    global trunk_open
    global frunk_open
    global is_user_present
    global is_climate_on
    global inside_temp
    global outside_temp
    global is_preconditioning
    global odometer
    global est_battery_range_km
    global rated_battery_range_km
    global ideal_battery_range_km
    global battery_level
    global usable_battery_level
    global plugged_in
    global charge_energy_added
    global charge_limit_soc
    global charge_port_door_open
    global charger_actual_current
    global charger_phases
    global charger_power
    global charger_voltage
    global charge_current_request
    global charge_current_request_max
    global scheduled_charging_start_time
    global time_to_full_charge

    # Check Teslamate MQTT Topics based on https://docs.teslamate.org/docs/integrations/mqtt
    if msg.topic == "teslamate/cars/1/display_name":
        display_name = value
    elif msg.topic == "teslamate/cars/1/state":
        state = value
    elif msg.topic == "teslamate/cars/1/since":
        since = value
    elif msg.topic == "teslamate/cars/1/healthy":
        healthy = value
    elif msg.topic == "teslamate/cars/1/version":
        version = value
    elif msg.topic == "teslamate/cars/1/update_available":
        update_available = value
    elif msg.topic == "teslamate/cars/1/update_version":
        update_version = value
    elif msg.topic == "teslamate/cars/1/model":
        model = value
    elif msg.topic == "teslamate/cars/1/trim_badging":
        trim_badging = value
    elif msg.topic == "teslamate/cars/1/exterior_color":
        exterior_color = value
    elif msg.topic == "teslamate/cars/1/wheel_type":
        wheel_type = value
    elif msg.topic == "teslamate/cars/1/spoiler_type":
        spoiler_type = value
    elif msg.topic == "teslamate/cars/1/geofence":
        geofence = value
    elif msg.topic == "teslamate/cars/1/latitude":
        latitude = value
    elif msg.topic == "teslamate/cars/1/longitude":
        longitude = value
    elif msg.topic == "teslamate/cars/1/shift_state":
        shift_state = value
    elif msg.topic == "teslamate/cars/1/power":
        power = value
    elif msg.topic == "teslamate/cars/1/speed":
        speed = value
    elif msg.topic == "teslamate/cars/1/heading":
        heading = value
    elif msg.topic == "teslamate/cars/1/elevation":
        elevation = value
    elif msg.topic == "teslamate/cars/1/locked":
        locked = value
    elif msg.topic == "teslamate/cars/1/sentry_mode":
        sentry_mode = value
    elif msg.topic == "teslamate/cars/1/windows_open":
        windows_open = value
    elif msg.topic == "teslamate/cars/1/doors_open":
        doors_open = value
    elif msg.topic == "teslamate/cars/1/trunk_open":
        trunk_open = value
    elif msg.topic == "teslamate/cars/1/frunk_open":
        frunk_open = value
    elif msg.topic == "teslamate/cars/1/is_user_present":
        is_user_present = value
    elif msg.topic == "teslamate/cars/1/is_climate_on":
        is_climate_on = value
    elif msg.topic == "teslamate/cars/1/inside_temp":
        inside_temp = value
    elif msg.topic == "teslamate/cars/1/outside_temp":
        outside_temp = value
    elif msg.topic == "teslamate/cars/1/is_preconditioning":
        is_preconditioning = value
    elif msg.topic == "teslamate/cars/1/odometer":
        odometer = value
    elif msg.topic == "teslamate/cars/1/est_battery_range_km":
        est_battery_range_km = value
    elif msg.topic == "teslamate/cars/1/rated_battery_range_km":
        rated_battery_range_km = value
    elif msg.topic == "teslamate/cars/1/ideal_battery_range_km":
        ideal_battery_range_km = value
    elif msg.topic == "teslamate/cars/1/battery_level":
        battery_level = value
    elif msg.topic == "teslamate/cars/1/usable_battery_level":
        usable_battery_level = value
    elif msg.topic == "teslamate/cars/1/plugged_in":
        plugged_in = value
    elif msg.topic == "teslamate/cars/1/charge_energy_added":
        charge_energy_added = value
    elif msg.topic == "teslamate/cars/1/charge_limit_soc":
        charge_limit_soc = value
    elif msg.topic == "teslamate/cars/1/charge_port_door_open":
        charge_port_door_open = value
    elif msg.topic == "teslamate/cars/1/charger_actual_current":
        charger_actual_current = value
    elif msg.topic == "teslamate/cars/1/charger_phases":
        charger_phases = value
    elif msg.topic == "teslamate/cars/1/charger_power":
        charger_power = value
    elif msg.topic == "teslamate/cars/1/charger_voltage":
        charger_voltage = value
    elif msg.topic == "teslamate/cars/1/charge_current_request":
        charge_current_request = value
    elif msg.topic == "teslamate/cars/1/charge_current_request_max":
        charge_current_request_max = value
    elif msg.topic == "teslamate/cars/1/scheduled_charging_start_time":
        scheduled_charging_start_time = value
    elif msg.topic == "teslamate/cars/1/time_to_full_charge":
        time_to_full_charge = value
    else:
        bot.send_message(
            chat_id,
            text = title + " : " + value,
            parse_mode=ParseMode.HTML,
        )

def start(update: Update, context: CallbackContext) -> None:
    """Sends a message with four inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Version", callback_data='version'),
            InlineKeyboardButton("Odometer", callback_data='odometer'),
        ],
        [
            InlineKeyboardButton("Battery", callback_data='battery'),
            InlineKeyboardButton("Sentry", callback_data='sentry'),
        ],
        [
            InlineKeyboardButton("Wake Up", callback_data='wake_up'),
            InlineKeyboardButton("What Else", callback_data='what_else'),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    global display_name
    global state
    global since
    global healthy
    global version
    global update_available
    global update_version
    global model
    global trim_badging
    global exterior_color
    global wheel_type
    global spoiler_type
    global geofence
    global latitude
    global longitude
    global shift_state
    global power
    global speed
    global heading
    global elevation
    global locked
    global sentry_mode
    global windows_open
    global doors_open
    global trunk_open
    global frunk_open
    global is_user_present
    global is_climate_on
    global inside_temp
    global outside_temp
    global is_preconditioning
    global odometer
    global est_battery_range_km
    global rated_battery_range_km
    global ideal_battery_range_km
    global battery_level
    global usable_battery_level
    global plugged_in
    global charge_energy_added
    global charge_limit_soc
    global charge_port_door_open
    global charger_actual_current
    global charger_phases
    global charger_power
    global charger_voltage
    global charge_current_request
    global charge_current_request_max
    global scheduled_charging_start_time
    global time_to_full_charge

    if query.data == "version":
        text = f"Version : {version}"
    elif query.data == "odometer":
        text = f"Odometer : {odometer}"
    elif query.data == "battery":
        if est_battery_range_km is not None:
            battery_value = f"Est Battery Range Km : {est_battery_range_km}\n"
        if rated_battery_range_km is not None:
            battery_value = f"{battery_value}Rated Battery Range Km : {rated_battery_range_km}\n"
        if ideal_battery_range_km is not None:
            battery_value = f"{battery_value}Ideal Battery Range Km : {ideal_battery_range_km}\n"
        if battery_level is not None:
            battery_value = f"{battery_value}Battery Level : {battery_level}\n"
        if usable_battery_level is not None:
            battery_value = f"{battery_value}Usable Battery Level : {usable_battery_level}\n"
        if plugged_in is not None:
            battery_value = f"{battery_value}Plugged In : {plugged_in}\n"
        if charge_energy_added is not None:
            battery_value = f"{battery_value}Charge Energy Added : {charge_energy_added}\n"
        if charge_limit_soc is not None:
            battery_value = f"{battery_value}Charge Limit SOC : {charge_limit_soc}\n"
        if charge_port_door_open is not None:
            battery_value = f"{battery_value}Charge Port Door Open : {charge_port_door_open}\n"
        if charger_actual_current is not None:
            battery_value = f"{battery_value}Charger Actual Current : {charger_actual_current}\n"
        if charger_phases is not None:
            battery_value = f"{battery_value}Charger Phases : {charger_phases}\n"
        if charger_power is not None:
            battery_value = f"{battery_value}Charger Power : {charger_power}\n"
        if charger_voltage is not None:
            battery_value = f"{battery_value}Charger Voltage : {charger_voltage}\n"
        if charge_current_request is not None:
            battery_value = f"{battery_value}Charge Current Request : {charge_current_request}\n"
        if charge_current_request_max is not None:
            battery_value = f"{battery_value}Charge Current Request Max : {charge_current_request_max}\n"
        if scheduled_charging_start_time is not None:
            battery_value = f"{battery_value}Scheduled Charging Start Time : {scheduled_charging_start_time}\n"
        if time_to_full_charge is not None:
            battery_value = f"{battery_value}Time To Full Charge : {time_to_full_charge}\n"

        text = battery_value
    elif query.data == "sentry":
        if sentry_mode is not None:
            if sentry_mode == "true":
                set_sentry = "false"
            else:
                set_sentry = "true"

            with teslapy.Tesla('YOUR_ACCOUNT_EMAIL', cache_file=tesla_cache_file) as tesla:
                tesla.fetch_token()
                vehicles = tesla.vehicle_list()
                vehicles[0].sync_wake_up()
                try:
                    vehicles[0].command('SET_SENTRY_MODE', on = set_sentry)
                    current_sentry_mode = vehicles[0].get_vehicle_data()['vehicle_state']['sentry_mode']
                except teslapy.HTTPError as e:
                    print(e)
                sentry_value = f"Current Sentry Mode : {current_sentry_mode}\n"
        text = sentry_value
    elif query.data == "wake_up":
        with teslapy.Tesla('YOUR_ACCOUNT_EMAIL', cache_file=tesla_cache_file) as tesla:
            tesla.fetch_token()
            vehicles = tesla.vehicle_list()
            vehicles[0].sync_wake_up()
            try:
                current_state = vehicles[0].get_vehicle_data()['state']
                state = current_state
            except teslapy.HTTPError as e:
                    print(e)

        if state is not None:
            state_value = f"Current State : {state}\n"

        text = state_value
    elif query.data == "what_else":
        if display_name is not None:
            what_else_value = f"Display Name : {display_name}\n"
        if state is not None:
            what_else_value = f"{what_else_value}State : {state}\n"
        if since is not None:
            what_else_value = f"{what_else_value}Since : {since}\n" 
        if healthy is not None:
            what_else_value = f"{what_else_value}Healthy : {healthy}\n"
        if update_available is not None:
            what_else_value = f"{what_else_value}Update Available : {update_available}\n"
        if update_version is not None:
            what_else_value = f"{what_else_value}Update Version : {update_version}\n"
        if model is not None:
            what_else_value = f"{what_else_value}Model : {model}\n"
        if trim_badging is not None:
            what_else_value = f"{what_else_value}Trim Badging : {trim_badging}\n"
        if wheel_type is not None:
            what_else_value = f"{what_else_value}Wheel Type : {wheel_type}\n"
        if exterior_color is not None:
            what_else_value = f"{what_else_value}Exterior Color : {exterior_color}\n"
        if spoiler_type is not None:
            what_else_value = f"{what_else_value}Spoiler Type : {spoiler_type}\n"
        if geofence is not None:
            what_else_value = f"{what_else_value}Geofence : {geofence}\n"
        if latitude is not None:
            what_else_value = f"{what_else_value}Latitude : {latitude}\n"
        if longitude is not None:
            what_else_value = f"{what_else_value}Longitude : {longitude}\n"
        if shift_state is not None:
            what_else_value = f"{what_else_value}Shift State : {shift_state}\n"
        if power is not None:
            what_else_value = f"{what_else_value}Power : {power}\n"
        if speed is not None:
            what_else_value = f"{what_else_value}Speed : {speed}\n"
        if heading is not None:
            what_else_value = f"{what_else_value}Heading : {heading}\n"
        if elevation is not None:
            what_else_value = f"{what_else_value}Elevation : {elevation}\n"
        if locked is not None:
            what_else_value = f"{what_else_value}Locked : {locked}\n"
        if sentry_mode is not None:
            what_else_value = f"{what_else_value}Sentry Mode : {sentry_mode}\n"
        if windows_open is not None:
            what_else_value = f"{what_else_value}Windows Open : {windows_open}\n"
        if doors_open is not None:
            what_else_value = f"{what_else_value}Doors Open : {doors_open}\n"
        if trunk_open is not None:
            what_else_value = f"{what_else_value}Trunk Open : {trunk_open}\n"
        if frunk_open is not None:
            what_else_value = f"{what_else_value}Frunk Open : {frunk_open}\n"
        if is_user_present is not None:
            what_else_value = f"{what_else_value}Is User Present : {is_user_present}\n"
        if is_climate_on is not None:
            what_else_value = f"{what_else_value}Is Climate On : {is_climate_on}\n"
        if inside_temp is not None:
            what_else_value = f"{what_else_value}Inside Temp : {inside_temp}\n"
        if outside_temp is not None:
            what_else_value = f"{what_else_value}Outside Temp : {outside_temp}\n"
        if is_preconditioning is not None:
            what_else_value = f"{what_else_value}Is Preconditioning : {is_preconditioning}\n"

        text = what_else_value

    query.edit_message_text(text)

def help_command(update: Update, context: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    update.message.reply_text("Use /start to check YOUR_BOT_NAME.")

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

updater = Updater(os.getenv('TELEGRAM_BOT_API_KEY'))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(CommandHandler('help', help_command))

client.loop_start()  # start the loop
try:
    bot.send_message(
            chat_id,
            text="<b>"+"YOUR_BOT_NAME"+"</b>\n"+"I'm here!!! :)",
            parse_mode=ParseMode.HTML,
        )

    while True:

        # Start the Bot
        updater.start_polling()

        time.sleep(1)

except KeyboardInterrupt:

    print("exiting")


client.disconnect()

client.loop_stop()
