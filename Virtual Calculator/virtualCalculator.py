import cv2
from cvzone.HandTrackingModule import HandDetector

class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self,img):
        cv2.rectangle(img, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height), (225, 225, 225), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height), (50, 50, 50), 3)
        cv2.putText(img, self.value, (self.pos[0] + 33, self.pos[1] + 70), cv2.FONT_HERSHEY_COMPLEX, 2, (50, 50, 50), 2)

    def checkClick(self,x,y):
        if self.pos[0]<x<self.pos[0]+self.width and self.pos[1]<y<self.pos[1]+self.height:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (255, 255, 255),
                          cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50), 3)
            cv2.putText(img, self.value, (self.pos[0] + 27, self.pos[1] + 80), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 0), 3)
            return True
        else:
            return False

#WEBCAM
cap = cv2.VideoCapture(0)
cap.set(3,1280) #WIDTH
cap.set(4,720)  #HEIGHT
detector = HandDetector(detectionCon=0.8, maxHands=1)

buttonListValues=[['7','8','9','*'],
                  ['4','5','6','/'],
                  ['1','2','3','+'],
                  ['.','0','=','-']]
#CREATING BUTTON
buttonList = []
for x in range(4):
    for y in range(4):
        xpos = x*100 + 700
        ypos = y*100 + 150
        buttonList.append(Button((xpos,ypos),100,100,buttonListValues[y][x]))

#VARIABLES
myEqu = ''
delayCounter = 0

#LOOP
while True:
    #GET IMAGE FROM CAMERA
    success, img = cap.read()
    img = cv2.flip(img, 1)

    #HAND DETECTION
    hands, img = detector.findHands(img, flipType=False)

    #DRAW BUTTONS
    cv2.rectangle(img, (700,50), (700+400, 70+150), (225, 225, 225), cv2.FILLED)
    cv2.rectangle(img, (700,50), (700+400, 70+150), (50,50,50), 3)
    for button in buttonList:
        button.draw(img)

    #CHECK FOR HAND
    if hands:
        lmList = hands[0]['lmList']
        length, _, img = detector.findDistance(lmList[8], lmList[12], img)
        x,y = lmList[8]
        if length<50:
            for i,button in enumerate(buttonList):
                if button.checkClick(x, y) and delayCounter == 0:
                    myVal = buttonListValues[int(i%4)][int(i/4)]

                    if myVal == '=':
                        myEqu = str(eval(myEqu))
                    else:
                        myEqu += myVal

                    delayCounter = 1

    #AVOID DUPLICATES
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0

    #DISPLAY EQU/RESULT
    cv2.putText(img, myEqu, (710, 120), cv2.FONT_HERSHEY_COMPLEX, 2, (50, 50, 50), 2)

    #DISPLAY IMAGE
    cv2.imshow("image", img)
    key = cv2.waitKey(1)

    if key == ord('c'):
        myEqu = ''
