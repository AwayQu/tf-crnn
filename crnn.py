from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf

tf.logging.set_verbosity(tf.logging.DEBUG)

HEIGHT = 32
nClass = 5000


def model_fn(features, labels, mode):
    input_layer = tf.reshape(features["img"], [-1, HEIGHT, -1, 1])

    conv1 = tf.layers.conv2d(inputs=input_layer, filters=64, kernel_size=[3, 3], padding="same", activation=tf.nn.relu,
                             name="conv1")
    pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2], strides=[2, 2], name='pool1')
    conv2 = tf.layers.conv2d(inputs=pool1, filters=128, kernel_size=[3, 3], padding="same", activation=tf.nn.relu,
                             name="conv2")
    pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[2, 2], strides=[2, 2], name='pool2')
    conv3 = tf.layers.conv2d(inputs=pool2, filters=256, kernel_size=[3, 3], padding="same", activation=tf.nn.relu,
                             name="conv3")
    conv4 = tf.layers.conv2d(inputs=conv3, filters=256, kernel_size=[3, 3], padding="same", activation=tf.nn.relu,
                             name="conv4")
    zero_padding1 = tf.contrib.ZeroPadding2D(padding=(0, 1), name="zero_padding1")(conv4)
    pool3 = tf.layers.max_pooling2d(inputs=zero_padding1, pool_size=[2, 2], strides=[2, 1], padding="valid",
                                    name="pool3")
    conv4 = tf.layers.conv2d(inputs=pool3, filters=512, kernel_size=[3, 3], padding="same", activation=tf.nn.relu,
                             name="conv4")
    normalization1 = tf.layers.batch_normalization(inputs=conv4, axis=1, name="normalization1")
    conv5 = tf.layers.conv2d(inputs=normalization1, filters=512, kernel_size=[3, 3], padding="same",
                             activation=tf.nn.relu,
                             name="conv5")
    normalization2 = tf.layers.batch_normalization(inputs=conv5, axis=1, name="normalization2")
    zero_padding2 = tf.contrib.ZeroPadding2D(padding=(0, 1), name="zero_padding2")(normalization2)
    pool4 = tf.layers.max_pooling2d(inputs=zero_padding2, pool_size=[2, 2], strides=[2, 1], padding="valid",
                                    name="pool4")
    conv7 = tf.layers.conv2d(inputs=pool4, filters=512, kernel_size=[3, 3], padding="valid",
                             activation=tf.nn.relu,
                             name="conv7")
    permute = tf.contrib.Permute((2, 1, 3), name='permute')(conv7)
    distribute = tf.contrib.TimeDistributed(tf.contrib.Flatten(), name='timedistrib')(permute)
    m = tf.contrib.Bidirectional(tf.contrib.LSTM(256, return_sequences=True), name='blstm1')(distribute)
    m = tf.contrib.Dense(256, name='blstm1_out', activation='linear')(m)
    m = tf.contrib.Bidirectional(tf.contrib.LSTM(256, return_sequences=True), name='blstm2')(m)
    logits = tf.contrib.Dense(nClass, name='blstm2_out', activation='softmax')(m)

    loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)
    if mode == tf.estimator.ModeKeys.TRAIN:
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
        train_op = optimizer.minimize(
            loss=loss,
            global_step=tf.train.get_global_step())
        return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

