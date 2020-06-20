# -*- coding: utf-8 -*-
"""rps.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ELIY0AhEU7vYOCTIUzDpdROSw7Vz9UhF
"""

import os
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from tensorflow.keras.applications.inception_v3 import InceptionV3

# Create an instance of the inception model from the local pre-trained weights

pre_trained_model = InceptionV3(
    input_shape=(300,300,3),
include_top=False)

# Make all the layers in the pre-trained model non-trainable
for layer in pre_trained_model.layers:
    layer.trainable=False
pre_trained_model.summary()

last_layer = pre_trained_model.get_layer('mixed7')
print('last layer output shape: ', last_layer.output_shape)
last_output = last_layer.output

class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('acc')>0.97):
      print("\nReached 97.0% accuracy so cancelling training!")
      self.model.stop_training = True

from tensorflow.keras.optimizers import RMSprop

# Flatten the output layer to 1 dimension
x = layers.Flatten()(last_output)
# Add a fully connected layer with 1,024 hidden units and ReLU activation
x = layers.Dense(1024,activation='relu')(x)
# Add a dropout rate of 0.2
x = layers.Dropout(0.2)(x)                  
# Add a final sigmoid layer for classification
x = layers.Dense(4,activation='softmax')(x)           

model = Model(pre_trained_model.input,x) 

model.compile(optimizer = tf.keras.optimizers.Adam(lr=0.001), 
              loss = 'categorical_crossentropy', 
              metrics =['acc'])

from google.colab import drive
drive.mount('/content/drive')

train_datagen = ImageDataGenerator(rescale=1./255,
                                  rotation_range=40,
                                  height_shift_range=0.2,
                                  width_shift_range=0.2,
                                  horizontal_flip=True)

# Note that the validation data should not be augmented!
test_datagen = ImageDataGenerator(rescale=1./255)

# Flow training images in batches of 20 using train_datagen generator
train_generator = train_datagen.flow_from_directory(
"/content/drive/My Drive/dataset/train",
batch_size=50,
class_mode='categorical',
target_size=(300,300))     

# Flow validation images in batches of 20 using test_datagen generator
validation_generator =  test_datagen.flow_from_directory( 
"/content/drive/My Drive/dataset/validation",
batch_size=20,
class_mode='categorical',
target_size=(300,300))

callbacks = myCallback()
history = model.fit_generator(
    train_generator,
    epochs=5,
    validation_data=validation_generator,
    callbacks=[callbacks],
               verbose=1
)

model.save("model.h5")
