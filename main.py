

import cv2
import datetime
import json
from async_frame_reader.video_async import MultiCameraCapture
import os
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import pyautogui as p
import autopy
import time


# Hand Detector
detectorHand = HandDetector(detectionCon=0.8, maxHands=1)

# Variables
# Parameters
width, height = 1280, 720
gestureThreshold = 300
folderPath = "C:\\Users\\user\\PycharmProject\\pythonProject\\opencvproject\\Presentation"
imgList = []
delay = 30
buttonPressed = False
counter = 0
drawMode = False
imgNumber = 0
delayCounter = 0
annotations = [[]]
annotationNumber = -1
annotationStart = False
hs, ws = int(120 * 1), int(213 * 1)  # width and height of small image

pathImages = sorted(os.listdir(folderPath), key=len)



if __name__ == "__main__":
    cameras = json.loads(open('C:\\Users\\user\\PycharmProject\\pythonProject\\opencvproject\\concurrent-camera-reader-second_camera_without_async\\concurrent-camera-reader-second_camera_without_async\\cameras.json').read())
    captured = MultiCameraCapture(sources=cameras)

    while True:
        for camera_name, cap in captured.captures.items():
            frame = captured.read_frame(cap)
            font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX

            # Get date and time and
            # save it inside a variable
            dt = str(datetime.datetime.now())

            # put the dt variable over the
            # video frame
            #frame = cv2.putText(frame, dt,(10, 100),font, 1, (210, 155, 155), 4, cv2.LINE_8)
            frame = cv2.flip(frame, 1)
            pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
            imgCurrent = cv2.imread(pathFullImage)
            # reading pseudoscreen image
            read = cv2.imread("C:\\Users\\user\\Desktop\\image.png")
            # Find the hand and its landmarks
            hands, frame = detectorHand.findHands(frame)
            # Draw Gesture Threshold line
            cv2.line(frame, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)
            # np.logical_and(arr > 1, arr < 3)
            if hands and buttonPressed is False:
                # If hand is detected

                hand = hands[0]
                cx, cy = hand["center"]
                lmList = hand["lmList"]  # List of 21 Landmark points
                fingers = detectorHand.fingersUp(hand)  # List of which fingers are up

                # Constrain values for easier drawing
                xVal = int(np.interp(lmList[8][0], [width // 2, width], [0, width]))
                yVal = int(np.interp(lmList[8][1], [50, height - 50], [0, height]))
                indexFinger = xVal, yVal

                if cy <= gestureThreshold:  # If hand is at the height of the face
                    if fingers == [1, 0, 0, 0, 0]: # if thumb is up move slide backward
                        p.press("left")
                        print("Left")
                        buttonPressed = True
                        if imgNumber > 0:
                            imgNumber -= 1
                            annotations = [[]]
                            annotationNumber = -1
                            annotationStart = False
                    if fingers == [0, 0, 0, 0, 1]:  # if little finger is up move forward
                        p.press("right")
                        print("Right")
                        buttonPressed = True
                        if imgNumber < len(pathImages) - 1:
                             imgNumber += 1
                             annotations = [[]]
                             annotationNumber = -1
                             annotationStart = False

                if fingers == [0, 1, 1, 0, 0]:  # annotation
                   # autopy.mouse.move(xVal, yVal)

                    cv2.circle(frame, indexFinger, 12, (0, 0, 255), cv2.FILLED)
                    cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)
                    cv2.circle(read, indexFinger, 12, (0, 0, 255), cv2.FILLED)

                if fingers == [1, 1, 0, 0, 1]: # pseudo screen


                        img = p.screenshot()
                        saved = img.save("C:\\Users\\user\\Desktop\\image.png")
                        read = cv2.imread("C:\\Users\\user\\Desktop\\image.png")
                        #cv2.imshow("pseudoscreen", read)
                        if cv2.waitKey(1) & 0XFF == ord('q'):
                            break



                #    autopy.mouse.click()

                if fingers == [0, 1, 0, 0, 0]: # writing

                    if annotationStart is False:
                        annotationStart = True
                        annotationNumber += 1
                        annotations.append([])
                    print(annotationNumber)
                    annotations[annotationNumber].append(indexFinger)
                    cv2.circle(frame, indexFinger, 12, (0, 0, 255), cv2.FILLED)
                    cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)
                    cv2.circle(read, indexFinger, 12, (0, 0, 255), cv2.FILLED)


                else:
                    annotationStart = False
                if fingers == [1,1,0,0,0]:
                    import pyautogui
                    import tkinter as tk
                    from tkinter.filedialog import *

                    root = tk.Tk()

                    canvas1 = tk.Canvas(root, width=180, height=50)
                    canvas1.pack()


                    def takeScreenshot():
                        myScreenshot = pyautogui.screenshot()
                        save_path = asksaveasfilename()
                        myScreenshot.save(save_path + "_screenshot.png")


                    myButton = tk.Button(text="Take Screenshoot", command=takeScreenshot, font=10)
                    canvas1.create_window(80, 20, window=myButton)

                    root.mainloop()
                if fingers == [0, 1, 1, 1, 0]:
                    if annotations:
                        annotations.pop(-1)
                        annotationNumber -= 1
                        buttonPressed = True

            else:
                annotationStart = False

            if buttonPressed:
                counter += 1
                if counter > delay:
                    counter = 0
                    buttonPressed = False

            for i, annotation in enumerate(annotations):
                for j in range(len(annotation)):
                    if j != 0:
                        cv2.line(frame, annotation[j - 1], annotation[j], (0, 0, 200), 12)
                        cv2.line(imgCurrent, annotation[j - 1], annotation[j], (0, 0, 200), 12)
                        cv2.line(read, annotation[j - 1], annotation[j], (0, 0, 200), 12)





            cv2.imshow(camera_name, frame)
            # password generation
            import random
            import array


            def webcampassword():
                """

                :rtype: object
                """
                print("")


            # maximum length of password needed
            # this can be changed to suit your password length
            MAX_LEN = 12

            # declare arrays of the character that we need in out password
            # Represented as chars to enable easy string concatenation
            DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                                 'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                                 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                                 'z']

            UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                                 'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
                                 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                                 'Z']

            SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',
                       '*', '(', ')', '<']

            # combines all the character arrays above to form one array
            COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS

            # randomly select at least one character from each character set above
            rand_digit = random.choice(DIGITS)
            rand_upper = random.choice(UPCASE_CHARACTERS)
            rand_lower = random.choice(LOCASE_CHARACTERS)
            rand_symbol = random.choice(SYMBOLS)

            # combine the character randomly selected above
            # at this stage, the password contains only 4 characters but
            # we want a 12-character password
            temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol

            # now that we are sure we have at least one character from each
            # set of characters, we fill the rest of
            # the password length by selecting randomly from the combined
            # list of character above.
            for x in range(MAX_LEN - 4):
                temp_pass = temp_pass + random.choice(COMBINED_LIST)

                # convert temporary password into array and shuffle to
                # prevent it from having a consistent pattern
                # where the beginning of the password is predictable
                temp_pass_list = array.array('u', temp_pass)
                random.shuffle(temp_pass_list)

            # traverse the temporary password array and append the chars
            # to form the password
            password = ""
            for x in temp_pass_list:
                password = password + x

            # print out password
            print(password)
            print(type(password))
            cv2.imshow("Presentation", imgCurrent)

            cv2.imshow("pseudoscreen", read)


            if cv2.waitKey(1) == 27:
                break
