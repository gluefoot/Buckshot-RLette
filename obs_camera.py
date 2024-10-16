# via John Montgomery on StackOverflow: https://stackoverflow.com/questions/604749/how-do-i-access-my-webcam-in-python
#  which is itself via sastanin: https://stackoverflow.com/questions/2601194/displaying-a-webcam-feed-using-opencv-and-python/11449901#11449901
# and HansHirse: https://stackoverflow.com/questions/58405119/how-to-resize-the-window-obtained-from-cv2-imshow

# bounding boxes by stwykd: https://stackoverflow.com/questions/20831612/getting-the-bounding-box-of-the-recognized-words-using-python-tesseract

# also look at windows-capture: https://github.com/NiiightmareXD/windows-capture/tree/main/windows-capture-python

import cv2
import pytesseract

# HansHirse section
cv2.namedWindow('Preview', cv2.WINDOW_KEEPRATIO)
aspect = (16,9)
scale = 60
cv2.resizeWindow('Preview', aspect[0]*scale, aspect[1]*scale)
vc = cv2.VideoCapture(1) # index 1 is obs virtual cam apparently?

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

image_text = None
while rval:
    # replace text and print if needed
    new_text = pytesseract.image_to_string(frame)
    if new_text != image_text:
        print(new_text)
        image_text = new_text

    d = pytesseract.image_to_data(frame, output_type=pytesseract.Output.DICT)
    n_boxes = len(d['level'])
    for i in range(n_boxes):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # personal note: beer and cigarette descriptions come through very clearly, but inverter doesn't. No item names are being picked up, neither are the yes/no options @ pills

    cv2.imshow('Preview', frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

vc.release()
cv2.destroyWindow("preview")