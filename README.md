# Rock_paper_scissors_with_pc

Description:

This is a game played between human and pc.I have named the pc name as anu,it can be changed as you want by modifying name in game.py file.This model is trained using transfer learning of inceptionv3 model.Dataset need to be generated using openCV.When the game begins you need to enter the maximum score of the game ,when either of the players reaches this score then the game terminates and displays the result as a picture. 

Requirements
Python 3
Keras
Tensorflow
OpenCV
Set up instructions
download the files from my repo
Gather Images for each gesture (rock, paper and scissors and None): In this example, we gather 500 images for the "rock" gesture in which 400 are saved in train folder and 100 are saved in validation folder
$ python3 get_training_images.py rock 500
Train and validate the model
$ python3 rps_train.py
Play the game with your computer!
$ python3 game.py
