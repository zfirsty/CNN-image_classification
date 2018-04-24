import os
import struct
import numpy as np

def load_mnist(path, kind='train'):
    """Load MNIST data from `path`"""
    labels_path = os.path.join(path,
                               '%s-labels.idx1-ubyte'
                               % kind)
    images_path = os.path.join(path,
                               '%s-images.idx3-ubyte'
                               % kind)
    with open(labels_path, 'rb') as lbpath:
        magic, n = struct.unpack('>II',
                                 lbpath.read(8))
        labels = np.fromfile(lbpath,
                             dtype=np.uint8)

    with open(images_path, 'rb') as imgpath:
        magic, num, rows, cols = struct.unpack('>IIII',imgpath.read(16))
        print('%d * %d * %d' % (num, rows, cols))
        images = np.fromfile(imgpath,
                             dtype=np.uint8).reshape(len(labels), 784)

    return np.reshape(images,[-1,28,28,1]), (np.arange(10)==labels[:,None]).astype(np.uint8)

def printImg(img,n=0):
    s = '';
    if n >= len(img):
        return
    for i in range(784):
        if i % 28 == 0:
            print('\n' + s)
            s = ''
        s += '%3s' % img[n][i]

    print('\n')
    return

pos = 0
def getbatch(x,y,batch_size,n=1):
    total = len(y)
    global pos
    for i in range(n):
        start = pos
        end = (pos + batch_size) % total
        turn = (pos + batch_size) // total - 1
        if(pos + batch_size >= total):
            curx = np.vstack((x[start:total],x[0:end]))
            cury = np.vstack((y[start:total],y[0:end]))
        else:
            curx = x[start:end]
            cury = y[start:end]
        while turn > 0:
            curx = np.vstack((curx,x[start:total],x[0:start]))
            cury = np.vstack((cury, y[start:total], y[0:start]))
            turn -= 1
        pos = end
        yield curx, cury

def generatebatch(X,Y,batch_size):
    n_examples = len(Y)
    for batch_i in range(n_examples // batch_size):
        start = batch_i*batch_size
        end = start + batch_size
        batch_xs = X[start:end]
        batch_ys = Y[start:end]
        yield batch_xs, batch_ys
