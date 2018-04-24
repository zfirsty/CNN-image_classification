from skimage import data, io ,img_as_ubyte,transform
import numpy as np
import tensorflow as tf

saver = tf.train.import_meta_graph('../final/classify-40000.meta')
graph = tf.get_default_graph()

def run_model(input_x):
    global graph
    if input_x.shape == (1,28,28,1):
        x = graph.get_tensor_by_name('x:0')
        keep_prob = graph.get_tensor_by_name('keep_prob:0')
        is_training = graph.get_tensor_by_name('is_training:0')

        pred_pos = graph.get_tensor_by_name('pred_pos:0')
        with tf.Session() as sess:
            saver.restore(sess, tf.train.latest_checkpoint('../final/'))
            rs = sess.run(pred_pos, feed_dict={x: input_x, keep_prob: 1,is_training:False})
            return rs[0]
    else:
        return 'wrong format you input'

def guess():
    img = io.imread('imgout.png',as_grey=True)
    img = img_as_ubyte(img)
    img = transform.resize(img, (28, 28))
    img = img_as_ubyte(img)
    img = np.reshape(img,[1,28,28,1])
    return run_model(img)
