# temperature-humidity-sensor

**Hardware**

- 1x Arduino MKR WiFi1010
- 1x DHT-11 Temperature and Humidity Sensor
- 1x USB-Powered Humidifier
- 1x Relay Module (I built one from scratch, but you can easily find a pre-built one)
    - 1x 5vRelay
    - 1x 1K Resistor
    - 1x 2N222 NPN Transistor
    - 1x 1N4007 Diode
- 1x MB102 Breadboard Power Supply
- 1x Breadboard

**Software / Tools**

- VSCode w PlatformIO IDE Extension (You can also use Arduino IDE) - For coding, compiling and uploading code to the Arduino, as well as to build the webapp.
- Firebase Realtime Database - For storing our historical temperature and humidity levels
- Streamlit - For the webapp front-end as well as data visualisation
- Heroku - For hosting our webapp
- Github - For version control

**Background**

If you’re someone who sleeps in an air-conditioned room every night, you would have a tendency to wake up with dry skin or an uncomfortably dry throat. A humidifer can help to reduce dryness in a room for a more comfortable night of rest. For this project, you will be: 

1. Installing a temperature and humidity sensor in your room
2. Sends data to a real-time database
3. Control a USB humidifer based on the humidity levels 
4. Turn on/off the sensor and visualise the temperature and humidity levels in a webapp

**Other Links**

View the live webapp: https://temperature-humidity-sensor.herokuapp.com/
View the demo video: https://drive.google.com/file/d/1IYdQ4XyEQ9qftm5fOvxsQDK9rHyZxyXI/view?usp=sharing

