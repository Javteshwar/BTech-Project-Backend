from json.decoder import JSONDecodeError
import cv2
import random
import json
scale = 0.5
circles = []
counter = 0
counter2 = 0
point1 = []
point2 = []
myPoints = []
myColor = []

formName = input('Enter Form Name: ')


def mousePoints(event, x, y, flags, params):
    global counter, point1, point2, counter1, counter2, circles, myColor
    if event == cv2.EVENT_LBUTTONDOWN:
        if counter == 0:
            point1 = int(x//scale), int(y//scale)
            counter = 1
            myColor = (random.randint(0, 2)*200, random.randint(0, 2)
                       * 200, random.randint(0, 2)*200)
        elif counter == 1:
            point2 = int(x//scale), int(y//scale)
            type_ = input('Enter Type: ')
            name = input('Enter Name: ')
            myPoints.append([point1, point2, type_, name])
            # myPoints.append([point1,point2])
            counter = 0
        circles.append([x, y, myColor])
        counter2 += 1


img = cv2.imread('query.jpg')
img = cv2.resize(img, (0, 0), None, scale, scale)

while True:
    for x, y, color in circles:
        cv2.circle(img, (x, y), 3, color, cv2.FILLED)
    cv2.imshow("original", img)
    cv2.setMouseCallback("original", mousePoints)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        print(myPoints)
        break

temp_dict = {formName: myPoints}

my_loaded_dict = {}
with open('form_dict.txt', 'r') as f:
    try:
        my_loaded_dict = json.load(f)
    except JSONDecodeError:
        pass
    f.close()
my_loaded_dict.update(temp_dict)
with open('form_dict.txt', 'w') as f:
    json.dump(my_loaded_dict, f, indent=4)
    f.close()
