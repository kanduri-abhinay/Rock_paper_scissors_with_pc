#!/usr/bin/env python
# coding: utf-8


import cv2
import os
import sys



cap=cv2.VideoCapture(0)

try:
    label=sys.argv[1]
    samples=int(sys.argv[2])
except:
    print("give the label name and number of samples required")
    exit(-1)
    
dir_path='dataset'
train_path=os.path.join(dir_path,'train')
valid_path=os.path.join(dir_path,'validation')
class_path1=os.path.join(train_path,label)
class_path2=os.path.join(valid_path,label)


try:
    os.mkdir('dataset')
except FileExistsError:
    pass
try:
    os.mkdir(train_path)
except FileExistsError:
    pass
try:
    os.mkdir(valid_path)
except FileExistsError:
    pass
try:
    os.mkdir(class_path1)
except FileExistsError:
    print("already existing and saving new ones with this old ones")
'''except Exception:
    print('error')'''
try:
    os.mkdir(class_path2)
except FileExistsError:
    pass


start = False
count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    if count == samples:
        break

    cv2.rectangle(frame, (100, 100), (400, 400), (255, 255, 255), 2)

    if start:
        roi = frame[100:400, 100:400]
        if(count<samples-100):
            save_path = os.path.join(class_path1, '{}.jpg'.format(count + 1))
        else:
            save_path = os.path.join(class_path2, '{}.jpg'.format(count + 1))

        cv2.imwrite(save_path, roi)
        count += 1

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "Collecting {}".format(count),
            (5, 50), font, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow("Collecting images", frame)

    k = cv2.waitKey(10)
    if k == ord('a'):
        start = not start

    if k == ord('q'):
        break

print("\n{} image(s) saved to {}".format(samples-100, class_path1))
print("n{} images saved to {}".format(100,class_path2))
cap.release()
cv2.destroyAllWindows()
