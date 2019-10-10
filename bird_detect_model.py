from keras.models import Sequential
from keras.layers import Dense, Activation, Conv2D, MaxPool2D, Dropout, Flatten
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.utils import to_categorical

import numpy as np
import get_features


def get_conv_model(input_shape):
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

    return model

def train_model():
    X, y = get_features.run("all", generate_new_subset=False, overwrite_mel=False)
    # make into a 2 dim input
    y_train = to_categorical(y)

    input_shape = (X.shape[1], X.shape[2], X.shape[3])
    m = get_conv_model(input_shape)

    m.fit(x=X, y=y_train, epochs=30, batch_size=32, shuffle=True)
    m.save("final.h5")

if __name__ == "__main__":
    train_model()
