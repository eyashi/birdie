from keras.models import Sequential
from keras.layers import Dense, Activation, Conv2D, MaxPool2D, Dropout, Flatten
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.utils import to_categorical

import numpy as np
import getfeatures


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


if __name__ == "__main__":
    X, y = getfeatures.run("all", generate_new_subset=False, overwrite_mel=False)

    # make into a 2 dim input
    X_train = np.reshape(X, (X.shape[0], X.shape[1], X.shape[2], 1))
    y_train = to_categorical(y)

    input_shape = (X_train.shape[1], X_train.shape[2], X_train.shape[3])
    m = get_conv_model(input_shape)

    m.fit(x=X_train, y=y_train, epochs=10, batch_size=32, shuffle=True)
