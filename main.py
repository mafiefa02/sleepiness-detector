import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
from variables import *
from cameraPorts import chooseCamera
import simpleaudio as sa
import time
import paho.mqtt.client as mqtt

mqttBroker = "test.mosquitto.org"
client = mqtt.Client("drowsiness_detection")
try:
    client.connect(mqttBroker)
    print("Connected to MQTT Broker: " + mqttBroker)
    time.sleep(3)
except:
    print("Connection failed to MQTT Broker: " + mqttBroker)
    time.sleep(3)


def alert(frame, type):
    cv2.rectangle(frame, (700, 20), (1250, 80), color["red"], cv2.FILLED)
    cv2.putText(frame, "DROWSY ALERT!", (710, 60),
                cv2.FONT_HERSHEY_PLAIN, 3, color["white"], 2)
    client.publish("drowsiness_detection", type)


def alertStop():
    client.publish("drowsiness_detection", "stop")


def main():
    video = cv2.VideoCapture(chooseCamera())
    video.set(3, 1280)
    video.set(4, 720)
    alarm = sa.WaveObject.from_wave_file("assets/alarm.wav")
    detector = FaceMeshDetector(maxFaces=1)

    # conditions
    sleepDummyCount, yawnDummyCount, sleepyDelay, yawnDelay = (0, 0, 7, 7)
    sleepState, yawnState = (False, False)
    sleepCount = 0
    yawnCount = 0
    alert_condition = False

    while True:
        ret, frame = video.read()
        frame = cv2.flip(frame, 1)
        frame, faces = detector.findFaceMesh(frame, draw=False)

        if faces:
            face = faces[0]

            for id in faceId:
                cv2.circle(frame, face[id], 3, color["red"], cv2.FILLED)

            leftEyeVerticalDistance, leftEyeVerticalPos = detector.findDistance(
                face[upLeftEye], face[downLeftEye])
            rightEyeVerticalDistance, rightEyeVerticalPos = detector.findDistance(
                face[upRightEye], face[downRightEye])
            leftEyeHorizontalDistance, leftEyeHorizontalPos = detector.findDistance(
                face[leftLeftEye], face[rightLeftEye])
            rightEyeHorizontalDistance, rightEyeHorizontalPos = detector.findDistance(
                face[leftRightEye], face[rightRightEye])

            leftEyeRatio = 100*(leftEyeVerticalDistance /
                                leftEyeHorizontalDistance)
            rightEyeRatio = 100*(rightEyeVerticalDistance /
                                 rightEyeHorizontalDistance)

            mouthVerticalDistance, mouthVerticalPos = detector.findDistance(
                face[upMouth], face[downMouth])
            mouthHorizontalDistance, mouthHorizontalPos = detector.findDistance(
                face[leftMouth], face[rightMouth])

            mouthRatio = 100*(mouthVerticalDistance/mouthHorizontalDistance)
            print(leftEyeRatio, rightEyeRatio, mouthRatio)

            # SLEEP
            if leftEyeRatio <= sleepyEyeRatio or rightEyeRatio <= sleepyEyeRatio:
                sleepDummyCount += 1
                if sleepDummyCount >= sleepyDelay:
                    print("Sleepy")
                    sleepState = True
                    sleepCount += 1
                    alert(frame, "sleep")
            else:
                alertStop()
                sleepDummyCount = 0
                sleepState = False

            # YAWN
            if mouthRatio >= sleepyMouthRatio:
                yawnDummyCount += 1
                if yawnDummyCount >= yawnDelay:
                    print("Yawn")
                    yawnState = True
                    yawnCount += 1
                    alert(frame, "yawn")
            else:
                alertStop()
                yawnDummyCount = 0
                yawnState = False

        cv2.imshow('video capture', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()


main()
