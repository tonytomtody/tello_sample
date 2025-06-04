from djitellopy import Tello
import threading
from time import sleep
import keyboard
#import cv2

def tello_init():
    global tello,telloflight
    tello = Tello()
    tello.connect()
    print("Tello is connected!")
    print(f"Battery: {tello.get_battery()}%")
    if tello.get_battery() < 20:
        print("Battery is low, please charge the drone.")
        tello.end()
        return
    print("Tello is ready to fly!")
    telloflight = True
    threadstart()


def tello_thread():
    global telloflight, tello
    telloflight = True
    while telloflight:
        global listening
        tello.takeoff()
        sleep(3)  # Wait for the drone to stabilize after takeoff
        for i in range(6):
            tello.move_forward(100)
        tello.rotate_counter_clockwise(90)
        for i in range(6):
            tello.move_forward(100)
        tello.rotate_counter_clockwise(90)
        for i in range(5):
            tello.move_forward(100)
        tello.land()
        tello.end()
        print("flight complete!")
        listening = False
        telloflight = False
        

def keyboard_thread():
    global listening
    global telloflight
    listening = True
    while listening:
        if keyboard.is_pressed('q'):
            print("Exiting...")
            telloflight = False
            tello.land()
            tello.end()
            break
        elif keyboard.is_pressed('e'):
            print("emergency stop!")
            telloflight = False
            tello.emergency()
            tello.land()
            tello.end()
            break

#def camera_thread():
    #tello.streamon()
    #frame_read = tello.get_frame_read()
    #while telloflight:
        #img = frame_read.frame
        #cv2.imshow("drone", img)
    #tello.streamoff()

def threadstart():
    threadings = []
    tello_threading = threading.Thread(target=tello_thread)
    keyboard_threading = threading.Thread(target=keyboard_thread)
    #camera_threading = threading.Thread(target=camera_thread)
    threadings.append(tello_threading)
    threadings.append(keyboard_threading)
    #threadings.append(camera_threading)

    for thread in threadings:
        thread.start()

    for thread in threadings:
        thread.join()

tello_init()
