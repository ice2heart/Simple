#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем модули фласка, библиотеку для работы с I2c и GPIO
from flask import Flask, json, jsonify, render_template, request, abort
from i2clibraries import i2c_lcd_smbus
import RPi.GPIO as GPIO

# Настраиваем GPIO на 22 порту будет висеть кнопка
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN)

# Настройка для экранчика
lcd = i2c_lcd_smbus.i2c_lcd(0x27, 1, 2, 1, 0, 4, 5, 6, 7, 3)
lcd.command(lcd.CMD_Display_Control | lcd.OPT_Enable_Display)
lcd.backLightOn()
lcd.clear()


app = Flask(__name__)

# Глобальная переменная с состоянием двери
door_status = 'close'


# Создаем маршрут на главную страницу
@app.route("/")
def show_index():
    # Отдаем главную страницу, тут можно добавлять переменных
    # для рендера, но нас это не интересует
    return render_template('index.html')


# А вот и наше API, запрос состояние
@app.route('/api/status', methods=['POST'])
def post_status():
    if (GPIO.input(22)):
        door_status = "close"
    else:
        door_status = "open"
    return jsonify({'door': door_status})


# А тут мы устанавливаем текст на экранчике
@app.route('/api/settext', methods=['POST'])
def post_text():
    lcd.clear()
    lcd.writeString(request.values['text'])
    return jsonify({'text': request.values['text']})


# Ну и главное запускаем все
if __name__ == "__main__":
    app.run(host='0.0.0.0')
