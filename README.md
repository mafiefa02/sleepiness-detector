# sleepiness-detector

This is a machine learning project for the `FI3271-Instrumentasi Berbasis Jaringan`'s final exam. This project uses object detection concept to detect whether a subject in front of a camera module is feeling sleepy or not.

## How it works
This program uses `OpenCV` as a tool for computer vision. The object detection algorithm we used is the `FaceMeshDetector` from the `FaceMeshModule` found in the `cvzone` library. We calculated the distance between the upper part of the object's eyes and used that distance as a parameter to determine whether the object observed is feeling sleepy or not.
### How it is connected to Arduino ESP8266
We are using a Raspberry Pi device to run the program. The program will be subscribed to a topic over the `test.mosquitto.org` broker. The message published on that topic is then attained using ESP8266 which then acts as a relay for the buzzer we used for the alarm device.

## The contributor
- Muhammad Afief Abdurrahman (10221006)
- Mohammad Ibrahim Akhyari (10221036)
- Natsir Hasan (10219107)
