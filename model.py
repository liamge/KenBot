import tensorflow as tf

# TODO: find picture size and decide on correct format
# Make the model

class Model:
    '''
    Code inspired by https://www.tensorflow.org/get_started/mnist/pros
    '''
    def __init__(self, config):
        self.conf = config

    def _build_placeholders(self):
        '''
        :return: edges of the computational graph to be filled by actual data values during the train step
        '''
        self.train_input = tf.placeholder(tf.int32, shape=[self.conf.batch_size, 320 * 240])
        self.train_labels = tf.placeholder(tf.int32, shape=[self.conf.batch_size])

    def _build_loss(self):
        with tf.name_scope('loss'):
            # 1st conv layer
            # change 1 to 3 if rgb
            x_image = tf.reshape(self.train_input, [-1, 320, 240, 1]) # batch_size x 320 x 240 x depth
            with tf.name_scope('conv1'):
                # change 1 to 3 if rgb
                W_conv1 = self.weight_variable([5, 5, 1, 32])
                b_conv1 = self.bias_variable([32])

                h_conv1 = tf.nn.relu(self.conv_2d(x_image, W_conv1) + b_conv1)
                h_pooled1 = self.max_pool_2d(h_conv1) # batch_size x 160 x 120 x depth

            # Second conv layer
            with tf.name_scope('conv2'):
                W_conv2 = self.weight_variable([5, 5, 32, 64])
                b_conv2 = self.bias_variable([64])

                h_conv2 = tf.nn.relu(self.conv_2d(h_pooled1, W_conv2) + b_conv2)
                h_pooled2 = self.max_pool_2d(h_conv2) # batch_size x 80 x 60 x depth

            # Dense layer 1
            with tf.name_scope('dense1'):
                W_fc1 = self.weight_variable([80 * 60 * 64, 1024])
                b_fc1 = self.bias_variable([1024])

                h_pool2_flat = tf.reshape(h_pooled2, [-1, 80 * 60 * 64])
                h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

            # Optional dropout
            if self.conf.dropout:
                with tf.name_scope('dropout'):
                    h_fc1_drop = tf.nn.dropout(h_fc1, self.conf.keep_prob)
            else:
                h_fc1_drop = h_fc1

            # Output layer
            with tf.name_scope('output'):
                W_fc2 = self.weight_variable([1024, 4])
                b_fc2 = self.bias_variable([4])

                y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2

            self.logits = y_conv
            self.loss = tf.reduce_mean(
                tf.nn.softmax_cross_entropy_with_logits(labels=self.train_labels, logits=y_conv)
            )

            correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(self.train_labels, 1))
            self.accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    def _build_optimizer(self):
        with tf.name_scope('optimizer'):
            self.optimizer = tf.train.AdamOptimizer(1e-4).minimize(self.loss)

    def build_graph(self):
        self._build_placeholders()
        self._build_loss()
        self._build_optimizer()

    def conv_2d(self, x, W):
        return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

    def max_pool_2d(self, x):
        tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                       strides=[1, 2, 2, 1], padding='SAME')

    def weight_variable(self, shape):
        init = tf.truncated_normal(shape, stddev=0.1)
        return tf.Variable(init)

    def bias_variable(self, shape):
        init = tf.constant(0.1, shape=shape)
        return tf.Variable(init)
