import numpy as np
import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
from variables import faceFeaturePos, color
from cameraPorts import chooseCamera


def main():
    video = cv2.VideoCapture(chooseCamera())
    detector = FaceMeshDetector(maxFaces=1)
    # face_cascade = cv2.CascadeClassifier(
    # cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # eye_cascade = cv2.CascadeClassifier(
    # cv2.data.haarcascades + 'haarcascade_eye.xml')

    while True:
        ret, frame = video.read()
        frame = cv2.flip(frame, 1)
        frame, faces = detector.findFaceMesh(frame, draw=False)

        if faces:
            face = faces[0]

            # up, down, left, right
            leftEye = [faceFeaturePos["upLeftEye"],
                       faceFeaturePos["downLeftEye"],
                       faceFeaturePos["leftLeftEye"],
                       faceFeaturePos["rightLeftEye"]]

            rightEye = [faceFeaturePos["upRightEye"],
                        faceFeaturePos["downLeftEye"],
                        faceFeaturePos["leftRightEye"],
                        faceFeaturePos["rightRightEye"]]

            mouth = [faceFeaturePos["upMouth"],
                     faceFeaturePos["downMouth"],
                     faceFeaturePos["leftMouth"],
                     faceFeaturePos["rightMouth"]]

            faceId = leftEye + rightEye + mouth

            for id in faceId:
                cv2.circle(frame, face[id], 5, color["blue"], cv2.FILLED)

        cv2.imshow('video capture', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()


main()
