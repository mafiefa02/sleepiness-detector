import cv2


def list_ports():
    """
    Test the ports and returns a tuple with the available ports and the ones that are working.
    """
    non_working_ports = []
    dev_port = 0
    working_ports = []
    available_ports = []
    # if there are more than 5 non working ports stop the testing.
    while len(non_working_ports) < 6:
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            non_working_ports.append(dev_port)
            # print("Port %s is not working." % dev_port)
        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            if is_reading:
                # print("Port %s is working and reads images (%s x %s)" %(dev_port, h, w))
                working_ports.append(dev_port)
            else:
                # print("Port %s for camera ( %s x %s) is present but does not reads." % (dev_port, h, w))
                available_ports.append(dev_port)
        dev_port += 1
    return working_ports


def chooseCamera():
    availableCameras = list_ports()
    if len(availableCameras) == 1:
        return 0
    else:
        while True:
            print("Available camera port to use:")
            for portNumber in range(len(availableCameras)):
                print(f"{portNumber+1}. Port {portNumber}")

            camera = input("\nWhat camera do you want to use? ")
            if camera:
                break
        return int(camera)-1
