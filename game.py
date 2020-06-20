#!/usr/bin/env python
# coding: utf-8

# In[ ]:
print("please wait, it is loading........")

from PIL import Image
from tensorflow.keras.models import load_model
import cv2
import numpy as np
from random import choice
import os
import time

abhinay_score=0
anu_score=0

max_score=int(input("enter game maximum score"))


REV_CLASS_MAP = {
    0: "none",
    1: "paper",
    2: "rock",
    3: "scissor"
}

def load(np_image):
   np_image = np.array(np_image).astype('float32')/255
   np_image = cv2.resize(np_image, (300, 300))
   np_image = np.expand_dims(np_image, axis=0)
   return np_image

def mapper(val):
    return REV_CLASS_MAP[val]


def calculate_winner(move1, move2):
    if move1 == move2:
        return "Tie"

    if move1 == "rock":
        if move2 == "scissor":
            return "User"
        if move2 == "paper":
            return "Computer"

    if move1 == "paper":
        if move2 == "rock":
            return "User"
        if move2 == "scissor":
            return "Computer"

    if move1 == "scissor":
        if move2 == "paper":
            return "User"
        if move2 == "rock":
            return "Computer"


model = load_model("model.h5")

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1300)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
cap.set(cv2.CAP_PROP_FPS, 5)
prev_move = None

icon1 = cv2.imread(os.path.join("images","winner.jpg"),1)
icon1 = cv2.resize(icon1, (300, 300))
icon2 = cv2.imread(os.path.join("images","loser.jpg"),1)
icon2 = cv2.resize(icon2, (300, 300))
while True:
    ret, frame = cap.read()
    
    if not ret:
        continue
    if(abhinay_score==max_score or anu_score==max_score):
        break;
    # rectangle for user to play
    cv2.rectangle(frame, (100, 100), (500, 500), (255, 255, 255), 2)
    # rectangle for computer to play
    cv2.rectangle(frame, (800, 100), (1200, 500), (255, 255, 255), 2)
    
    # extract the region of image within the user rectangle
    img = frame[100:500, 100:500]
    #img = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (300, 300))
    image = load(img)
    res=model.predict(image)
    user_move_name= mapper(np.argmax(res))
    #print(user_move_name)
    # predict the move made
    

    # predict the winner (human vs computer)
    if prev_move != user_move_name:
        if user_move_name != "none":
            computer_move_name = choice(['rock', 'paper', 'scissor'])
            winner = calculate_winner(user_move_name, computer_move_name)
            if(winner=="User"):
                abhinay_score+=1
            elif(winner=="Computer"):
                anu_score+=1
        else:
            computer_move_name = "none"

    prev_move = user_move_name

    # display the information
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "ABHINAY",
                (250, 50), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "ANU",
                (900, 50), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "Your Move: " + user_move_name,
                (50, 540), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "ANU's Move: " + computer_move_name,
                (750, 540), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "SCORES :"+str(abhinay_score)+" : "+str(anu_score),
                (400, 650), font, 2, (0, 0, 255), 4, cv2.LINE_AA)

    if computer_move_name != "none":
        #print(computer_move_name)
        icon = cv2.imread(os.path.join("images","{}.jpg".format(computer_move_name)))
        icon = cv2.resize(icon, (400, 400))
        frame[100:500, 800:1200] = icon

    
    cv2.imshow("Rock Paper Scissor", frame)
    k = cv2.waitKey(10)
    if k == ord('q'):
        break
    

#cv2.destroyAllWindows()
if(abhinay_score>anu_score):
   cv2.imshow("Result : You Won",cv2.imread(os.path.join('images','winner.jpg')))
   cv2.waitKey()
else:
   cv2.imshow("Result : You Lose",cv2.imread(os.path.join('images','loser.jpg')))
   cv2.waitKey()
cap.release()

