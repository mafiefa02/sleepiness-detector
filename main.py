from cv2 import rectangle, putText, FILLED, FONT_HERSHEY_PLAIN, FONT_HERSHEY_SIMPLEX, flip, imshow, waitKey, circle, destroyAllWindows, VideoCapture, resize, INTER_AREA, COLOR_BGR2GRAY, cvtColor, COLOR_RGB2BGR, COLOR_RGB2GRAY, COLOR_BGR2RGB, COLOR_GRAY2RGB, COLOR_GRAY2BGR, COLOR_BGR2GRAY, COLOR_GRAY2BGR, COLOR_BGR2RGB, COLOR_RGB2BGR, COLOR_RGB2GRAY, COLOR_GRAY2RGB, COLOR_GRAY2BGR, COLOR_BGR2GRAY, COLOR_GRAY2BGR, COLOR_BGR2RGB, COLOR_RGB2BGR, COLOR_RGB2GRAY, COLOR_GRAY2RGB, COLOR_GRAY2BGR, COLOR_BGR2GRAY, COLOR_GRAY2BGR, COLOR_BGR2RGB, COLOR_RGB2BGR, COLOR_RGB2GRAY, COLOR_GRAY2RGB, COLOR_GRAY2BGR, COLOR_BGR2GRAY, COLOR_GRAY2BGR, COLOR_BGR2RGB, COLOR_RGB2BGR, COLOR_RGB2GRAY, COLOR_GRAY2RGB, COLOR_GRAY2BGR, COLOR_BGR2GRAY, COLOR_GRAY2BGR, COLOR_BGR2RGB, COLOR_RGB2BGR, COLOR_RGB2GRAY, COLOR_GRAY2RGB, COLOR_GRAY2BGR, COLOR_BGR2GRAY, COLOR_GRAY2BGR
from cvzone.FaceMeshModule import FaceMeshDetector
from variables import *
from cameraPorts import chooseCamera
from broker import connectBroker
from threading import Thread
from time import sleep

# initialize broker
client = connectBroker(
    "test.mosquitto.org", "drowsiness_detection")


def alert(frame, type):
    rectangle(frame, (700, 20), (1250, 80), color["red"], FILLED)
    putText(frame, "DROWSY ALERT!", (710, 60),
            FONT_HERSHEY_PLAIN, 3, color["white"], 2)
    client.publish("drowsiness_detection", type)
    print("Published: " + type)
    sleep(3)  # alert for 3 seconds


def alertStop():
    client.publish("drowsiness_detection", "stop")
    print("Published: stop")


def main():
    # initialize camera
    video = VideoCapture(chooseCamera())
    video.set(3, 1280)
    video.set(4, 720)

    # initialize detector
    detector = FaceMeshDetector(maxFaces=1)

    # conditions
    sleepDummyCount, yawnDummyCount, sleepyDelay, yawnDelay = (0, 0, 7, 7)
    sleepState, yawnState = (False, False)
    sleepCount = 0
    yawnCount = 0

    while True:
        # read video
        ret, frame = video.read()
        frame = flip(frame, 1)
        frame, faces = detector.findFaceMesh(frame, draw=False)

        if sleepState:
            alert_event = Thread(target=alert, args=(
                frame, "sleepy"))
            alert_event.start()
            alert_event.join()
        elif yawnState:
            alert_event = Thread(target=alert, args=(
                frame, "yawn"))
            alert_event.start()
            alert_event.join()
        else:
            alertStop()

        # check if face is detected
        if faces:
            face = faces[0]

            for id in faceId:
                circle(frame, face[id], 3, color["red"], FILLED)

            # get distance of eyes and mouth
            leftEyeVerticalDistance, leftEyeVerticalPos = detector.findDistance(
                face[upLeftEye], face[downLeftEye])
            rightEyeVerticalDistance, rightEyeVerticalPos = detector.findDistance(
                face[upRightEye], face[downRightEye])
            leftEyeHorizontalDistance, leftEyeHorizontalPos = detector.findDistance(
                face[leftLeftEye], face[rightLeftEye])
            rightEyeHorizontalDistance, rightEyeHorizontalPos = detector.findDistance(
                face[leftRightEye], face[rightRightEye])

            # get ratio of eyes and mouth
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

            # sleepy detection
            if leftEyeRatio <= sleepyEyeRatio or rightEyeRatio <= sleepyEyeRatio:
                sleepDummyCount += 1
                if sleepDummyCount >= sleepyDelay:
                    sleepState = True
                    sleepCount += 1
            else:
                sleepDummyCount = 0
                sleepState = False

            # yawn detection
            if mouthRatio >= sleepyMouthRatio:
                yawnDummyCount += 1
                if yawnDummyCount >= yawnDelay:
                    yawnState = True
                    yawnCount += 1
            else:
                yawnDummyCount = 0
                yawnState = False

        # show video
        imshow('video capture', frame)

        # exit by pressing 'q'
        if waitKey(1) == ord('q'):
            break

    video.release()
    destroyAllWindows()


main()
