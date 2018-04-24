import tensorflow as tf
import loadmnist as lm

tx,ty = lm.load_mnist('C:\\Users\\Zy\\Desktop\\MNIST','t10k')
saver = tf.train.import_meta_graph('saves/classify3-40000.meta')
graph = tf.get_default_graph()
def Test(input_x,input_y):
    global  graph
    if len(input_x) == len(input_y) and len(input_x) > 0:
        x = graph.get_tensor_by_name('x:0')
        y = graph.get_tensor_by_name('y:0')
        keep_prob = graph.get_tensor_by_name('keep_prob:0')

        accuracy = graph.get_tensor_by_name('accuracy:0')
        pred_pos = graph.get_tensor_by_name('pred_pos:0')
        with tf.Session() as sess:
            saver.restore(sess, tf.train.latest_checkpoint('saves/'))
            if len(input_x) == 1:
                rs = sess.run(pred_pos, feed_dict={x: input_x, y: input_y, keep_prob: 1})
                print(input_y)
                print('result : %d' % (rs[0]+1))
            else:
                rs = sess.run(accuracy, feed_dict={x: input_x, y: input_y, keep_prob: 1})
                print('data(%d) : ac is %f'%(len(input_x),rs*100))
    else:
        print('wrong format you input')

