# How this will work

- Record 10 second audio chunks continuously (until some threshold is reached for number of clips to evaluate)
- Check if there are any bird sounds in the audio.
  - If there are, save the clip & queue it for classifying.
  - If there aren't, delete that clip.
- Run bird sound clips through classifier to determine what bird said it.
- Run bird sound with additional info through classifier to determine why the bird said what it said.
  - This is the only part that really doesn't have precidence in literature. It's going to be fairly simplistic and maybe even a little make belief, but I think that will only make it funnier. Probably the least scientifically relevant part of this.

## Check if there are any bird sounds in the audio

- Try to shorten the sample length trained on. 40ms instead of 80.
- Further filter out some of the channels.. create fewer hanning filter windows to reduce number of features.
- Add a lot more convolutional layers as in birddet.py
- What is LeakyReLU?
- What is batch normalization?
- More max pooling?
- Why couldn't I end my dense layer in a 1?
- Activate final dense layer with sigmoid?
- Use binary cross-entropy instead of catagorical DUH
- Change the learning rate of Adam?
- Use the callback function to end when improvement stops.
  - Do many epochs. Run overnight.
- Actually export the model in the end !!!

Current model with notes above for improvement:

```python
model = Sequential()
    model.add(
        Conv2D(
            16,
            (3, 3),
            activation="relu",
            strides=(1, 1),
            padding="same",
            input_shape=input_shape,
        )
    )
    model.add(Conv2D(32, (3, 3), activation="relu", strides=(1, 1), padding="same"))
    model.add(Conv2D(64, (3, 3), activation="relu", strides=(1, 1), padding="same"))
    model.add(MaxPool2D((2, 2)))
    model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(Dense(64, activation="relu"))
    model.add(Dense(32, activation="relu"))
    model.add(Dense(2, activation="softmax"))
    model.summary()
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["acc"])
```

## Classify the bird sound

## Make belief sentiment analysis on the bird sound
