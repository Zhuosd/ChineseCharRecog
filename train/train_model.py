# coding=utf-8

import pickle
from keras.layers import BatchNormalization, PReLU, Input, Conv2D, MaxPool2D, AveragePooling2D, Flatten, Dense, Dropout, Activation
from keras.models import Model
from keras.optimizers import SGD
import numpy as np


# bn + prelu
def bn_prelu(x):
    x = BatchNormalization()(x)
    x = PReLU()(x)
    return x

# build baseline model

def build_model(out_dims, input_shape=(128, 128, 3)):
    inputs_dim = Input(input_shape)

    x = Conv2D(32, (3, 3), strides=(2, 2), padding='valid')(inputs_dim)
    x = bn_prelu(x)

    x = Conv2D(32, (3, 3), strides=(1, 1), padding='valid')(x)
    x = bn_prelu(x)

    x = MaxPool2D(pool_size=(2, 2))(x)

    x = Conv2D(64, (3, 3), strides=(1, 1), padding='valid')(x)
    x = bn_prelu(x)

    x = Conv2D(64, (3, 3), strides=(1, 1), padding='valid')(x)
    x = bn_prelu(x)

    x = MaxPool2D(pool_size=(2, 2))(x)

    x = Conv2D(128, (3, 3), strides=(1, 1), padding='valid')(x)
    x = bn_prelu(x)

    x = MaxPool2D(pool_size=(2, 2))(x)

    x = Conv2D(128, (3, 3), strides=(1, 1), padding='valid')(x)
    x = bn_prelu(x)

    x = AveragePooling2D(pool_size=(2, 2))(x)
    x_flat = Flatten()(x)

    fc1 = Dense(512)(x_flat)
    fc1 = bn_prelu(fc1)

    dp_1 = Dropout(0.3)(fc1)

    fc2 = Dense(out_dims)(dp_1)
    fc2 = Activation('softmax')(fc2)

    model = Model(inputs=inputs_dim, outputs=fc2)

    return model


train_data = pickle.load(open('train_data.dat','rb'))

train_X = np.array([x[1] for x in train_data[0:len(train_data)]])
train_Y = np.array([x[2] for x in train_data[0:len(train_data)]])

model = build_model(100)
sgd = SGD(lr=0.1, momentum=0.9, decay=5e-4, nesterov=True)
model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])
history = model.fit(x=train_X, y=train_Y, batch_size=32, epochs=50, verbose=1, validation_split=0.1)

model.save_weights('base-model.h5')
