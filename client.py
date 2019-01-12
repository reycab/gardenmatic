# -*- coding: utf-8 -*-
"""."""
import RPi.GPIO as GPIO
import time
import requests
import Adafruit_DHT

email = "admin@admin.com"
password = "qwerty123"
API_ROOT = "http://192.168.1.5:8000"
API_AUTH = API_ROOT + "/api-auth/login"
API_URL = API_ROOT + "/api"

LUZ = None
HUMEDAD_AMBIENTE = None
TEMPERATURA_AMBIENTE = None
HUMEDAD_TIERRA = None
SOLENOIDE_VALVE = 0
PIN_VALVE = None

GPIO.setmode(GPIO.BCM)


def enviar_lectura_a_server(pin, lectura, tipo_sensor):
    """."""
    requests.post(
        API_URL + '/reading-sensor/',
        auth=(email, password),
        data={'pin': pin, 'lectura': lectura, 'tipo_sensor': tipo_sensor})


def porcentaje_luminosidad(x, in_min, in_max, out_min, out_max):
    """."""
    porcentaje = (
        (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
    return porcentaje


def sensores_disponibles():
    """."""
    r = requests.get(
        API_URL + '/sensores-disponibles/',
        auth=(email, password))
    return r.json()


def leer_luminocidad(pin):
    """."""
    count = 0
    # Se establece al pin como SALIDA
    GPIO.setup(pin, GPIO.OUT)
    # Se establece el pin en modo BAJO (0)
    GPIO.output(pin, GPIO.LOW)
    # Se hace una "pausa" de 100 milisegundos
    time.sleep(0.1)

    # Se cambia el pin a ENTRADA
    GPIO.setup(pin, GPIO.IN)

    # Mientras el pin siga siendo BAJO la variable count suma 1
    while (GPIO.input(pin) == GPIO.LOW):
        count += 1
        # Si la variable count es mayor o igual 100000
        # indica que hay ausencia de luz y se detiene la ejecución
        if count >= 100000:
            break
    return count


def leer_temperatura_humedad(pin):
    """."""
    humedad, temperatura = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, pin)
    return humedad, temperatura


def leer_humedad_tierra(pin):
    """."""
    hum_tierra = 0
    GPIO.setup(pin, GPIO.IN)
    if GPIO.input(pin) == GPIO.LOW:
        hum_tierra = 1
    return hum_tierra


def abrir_valvula(pin):
    """."""
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.5)
    GPIO.cleanup()


for sensor in sensores_disponibles():
    if sensor['type_sensor'] == 'light':
        LUZ = leer_luminocidad(sensor['pin'])
        luminosidad = porcentaje_luminosidad(LUZ, 100000, 0, 0, 100)
        if LUZ is not None:
            enviar_lectura_a_server(
                sensor['pin'], '{}'.format(luminosidad), sensor['type_sensor'])
        else:
            print('No se puede leer el sensor de LUZ')

    if sensor['type_sensor'] == 'ambient_humidity':
        HUMEDAD_AMBIENTE, TEMPERATURA_AMBIENTE = leer_temperatura_humedad(sensor['pin'])  # noqa
        if HUMEDAD_AMBIENTE is not None:
            enviar_lectura_a_server(
                sensor['pin'], '{}'.format(HUMEDAD_AMBIENTE),
                sensor['type_sensor'])
        else:
            print('No se puede leer el sensor de humedad ambiente')

    if sensor['type_sensor'] == 'ambient_temperature':
        HUMEDAD_AMBIENTE, TEMPERATURA_AMBIENTE = leer_temperatura_humedad(sensor['pin'])  # noqa
        if TEMPERATURA_AMBIENTE is not None:
            enviar_lectura_a_server(
                sensor['pin'], '{}'.format(TEMPERATURA_AMBIENTE),
                sensor['type_sensor'])
        else:
            print('No se puede leer el sensor de temperatura ambiente')

    if sensor['type_sensor'] == 'ground_humidity':
        HUMEDAD_TIERRA = leer_humedad_tierra(sensor['pin'])
        if HUMEDAD_TIERRA is not None:
            enviar_lectura_a_server(
                sensor['pin'], '{}'.format(HUMEDAD_TIERRA),
                sensor['type_sensor'])
        else:
            print('No se puede leer el sensor de humedad de tierra')

    if sensor['type_sensor'] == 'solenoide_valve':
        PIN_VALVE = sensor['pin']

if PIN_VALVE is not None:
    if HUMEDAD_TIERRA is not None:
        if HUMEDAD_TIERRA == 0:
            abrir_valvula(PIN_VALVE)
        SOLENOIDE_VALVE = 1
    enviar_lectura_a_server(
        PIN_VALVE, SOLENOIDE_VALVE, 'solenoide_valve')
else:
    print('No hay valvula activa o agregada al sistema')
