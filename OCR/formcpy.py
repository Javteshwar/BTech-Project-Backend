import cv2
import numpy as np
import pytesseract
import os
import re
import json
import math
pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\kunal\\Desktop\\Workspace\\major\\Tesseract-ocr\\tesseract.exe'

per = 25
pixelThres = 0.3

# formName="form1"
formName = input('Form Name:')

with open('my_dict.json', 'r') as f:
    dic = json.load(f)
roi = dic[formName]

imgQ = cv2.imread('query.jpg')
h, w, c = imgQ.shape
orb = cv2.ORB_create(1000)
kp1, des1 = orb.detectAndCompute(imgQ, None)

path = 'user_form'

mylist = os.listdir(path)
for j, y in enumerate(mylist):
    img = cv2.imread(path+"/"+y)
    kp2, des2 = orb.detectAndCompute(img, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.match(des2, des1)
    matches = sorted(matches, key=lambda x: x.distance)
    good = matches[:int(len(matches)*(per/100))]
    imgmatch = cv2.drawMatches(img, kp2, imgQ, kp1, good, None, flags=2)

    srcpoints = np.float32(
        [kp2[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dstpoints = np.float32(
        [kp1[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    M, _ = cv2.findHomography(srcpoints, dstpoints, cv2.RANSAC, 5.0)
    imgScan = cv2.warpPerspective(img, M, (w, h))
    # imgScan=cv2.resize(imgScan,(w//2,h//2))
    # cv2.imshow(y,imgScan)

    imgShow = imgScan.copy()
    imgMask = np.zeros_like(imgShow)

    myData = []
    print(f'#####Extracting data from form {j}#####')

    jsonRes = {}
    for x, r in enumerate(roi):
        cv2.rectangle(imgMask, (r[0][0], r[0][1]),
                      (r[1][0], r[1][1]), (0, 255, 0), cv2.FILLED)
        imgShow = cv2.addWeighted(imgShow, 0.99, imgMask, 0.1, 0)

        imgCrop = imgScan[r[0][1]:r[1][1], r[0][0]:r[1][0]]
        # cv2.imshow(str(x),imgCrop)

        if r[2] == 'text':
            s = pytesseract.image_to_string(imgCrop)
            s = s.replace('\n', '')
            s = s.strip()
            s = s.replace('\x0c', '')
            print(f'{r[3]}:{s}')
            myData.append(s)
            jsonRes[r[3]] = s
        if r[2] == 'box':
            imgGray = cv2.cvtColor(imgCrop, cv2.COLOR_BGR2GRAY)
            imgThresh = cv2.threshold(
                imgGray, 170, 255, cv2.THRESH_BINARY_INV)[1]
            totalPixels = cv2.countNonZero(imgThresh)
            total_area = (r[1][1]-r[0][1])*(r[1][0]-r[0][0])
            math.sqrt(total_area)
            print(total_area)
            print(totalPixels)
            if totalPixels/total_area > pixelThres:
                totalPixels = 1
            else:
                totalPixels = 0
            print(f'{r[3]}:{totalPixels}')
            myData.append(totalPixels)
            jsonRes[r[3]] = totalPixels
    with open('output.csv', 'a+') as f:
        for data in myData:
            f.write((str(data)+','))
        f.write('\n')
    imgShow = cv2.resize(imgShow, (w//2, h//2))
    cv2.imshow(y+"2", imgShow)

print(jsonRes)
imgQ = cv2.resize(imgQ, (w//2, h//2))
cv2.waitKey(0)
