import tensorflow as tf
import loadmnist as lm
import numpy as np

def getW(shape,name):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial,name=name)
def getB(num,name):
    initial = tf.constant(0.1, shape=[num])
    return tf.Variable(initial,name=name)

def get_mean_var(ema,batch_mean,batch_var):
    ema_apply_op = ema.apply([batch_mean, batch_var])
    with tf.control_dependencies([ema_apply_op]):
        return tf.identity(batch_mean), tf.identity(batch_var)

def bn_layer(input,num):
    ema = tf.train.ExponentialMovingAverage(decay=0.5)
    batch_mean, batch_var = tf.nn.moments(input, [0, 1, 2], keep_dims=True)
    mean, var = tf.cond(is_training, lambda:(get_mean_var(ema,batch_mean,batch_var)), lambda: (ema.average(batch_mean), ema.average(batch_var)))
    shift = tf.Variable(tf.zeros([num]))
    scale = tf.Variable(tf.ones([num]))
    epsilon = 1e-3
    return tf.nn.batch_normalization(input, mean, var, shift, scale, epsilon)

# 训练数据集和测试数据集
ox, oy = lm.load_mnist('C:\\Users\\Zy\\Desktop\\MNIST', 'train')
tx, ty = lm.load_mnist('C:\\Users\\Zy\\Desktop\\MNIST', 't10k')

y = tf.placeholder(tf.float32, [None,10],name='y')
x = tf.placeholder(tf.float32, [None,28,28,1],name='x')
is_training = tf.placeholder(tf.bool,name='is_training')
keep_prob = tf.placeholder("float",name='keep_prob')

#第一层 conv + pool
w1 = getW([5,5,1,24],'w1')
b1 = getB(24,'b1')
relu_out1 = tf.nn.relu(tf.nn.conv2d(x,w1,strides=[1,1,1,1],padding='SAME')+b1)
BN_out1 = bn_layer(relu_out1,24)
maxpool_out1 = tf.nn.max_pool(BN_out1,[1,2,2,1],strides=[1,2,2,1],padding='SAME')

#第二层 conv + pool
w2 = getW([4,4,24,64],'w2')
b2 = getB(64,'b2')
conv_out2 = tf.nn.conv2d(maxpool_out1,w2,strides=[1,1,1,1],padding='SAME')+b2
BN_out2 = bn_layer(tf.nn.relu(conv_out2),64)
maxpool_out2 = tf.nn.max_pool(BN_out2,[1,2,2,1],strides=[1,2,2,1],padding='SAME')

#FC layer 1
maxpool_reshape = tf.reshape(maxpool_out2, [-1, 7*7*64])
w3 = getW([7*7*64,1024],'w3')
b3 = getB(1024,'b3')
full_out1 = tf.nn.relu(tf.matmul(maxpool_reshape, w3) + b3)

h_fc1_drop = tf.nn.dropout(full_out1, keep_prob)

#FC layer 2
w4 = getW([1024,10],'w4')
b4 = getB(10,'b4')
full_out2 = tf.matmul(h_fc1_drop, w4) + b4
pred = tf.nn.softmax(full_out2,name="pred")

loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=y,logits=full_out2))
#tf.summary.scalar('CROSS ENTROPY',loss)
train = tf.train.AdamOptimizer(1.5e-3).minimize(loss)

pred_pos = tf.argmax(pred,1,name="pred_pos")
y_pos = tf.argmax(y,1)
accuracy = tf.reduce_mean(tf.cast(tf.equal(pred_pos,y_pos),tf.float32),name="accuracy")
tf.summary.scalar('TRAIN ACCURACY',accuracy)

merged = tf.summary.merge_all()
init = tf.global_variables_initializer()
saver = tf.train.Saver()

with tf.Session() as sess:
    writer = tf.summary.FileWriter('/myrecord/test4', sess.graph)
    sess.run(init)
    for i in range(40000):
        for curx, cury in lm.getbatch(ox,oy,8):
            t = sess.run(train, feed_dict={x: curx, y: cury,keep_prob:0.7,is_training:True})
        if (i+1) % 1000 == 0:
            ac = sess.run(accuracy,feed_dict={x:tx,y:ty,keep_prob:1,is_training:False})
            print('%d times is %f%%'%(i+1,ac*100))
       #writer.add_summary(ac,i)
        if  (i+1)  == 40000:
            saver.save(sess,"final/classify",global_step=40000)

