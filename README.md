# ESP32-S3 (Arduino Nano) Display Server

This repository contains the code for an Arduino Nano, ESP32-S3, with an 8 segment MAX7219 running MicroPython.

## Features
* WiFi connection
* WebREPL enabled
* API server using [micropyserver](https://github.com/troublegum/micropyserver/)
* Scrolling or Printed messages to the display
* Customizable brightness, speed, and repetition.


## Sending Messages
To send a basic message, you can just use curl: 

`curl http://10.10.20.12/message -d "message=Smells like magic"`.

To send a full brightness without scrolling: 

`curl http://10.10.20.12/message -d "message=Smells like magic" -d "scroll=False" -d "brightness=10"`

## PIN Configuration
I've documented the configuration within the `boot.py` but the configuration is as follows.
* VCC -> 3.3v
* Data (DIN) -> D2
* Load (CS)  -> D3
* CLK        -> D4
