import tensorflow as tf 
from tensorflow.compat.v1 import get_variable, add
import tfops 
import horovod.tensorflow as hvd

def ops():
    hvd.init()
    by2 = tf.random.uniform((2,2))
    tallreduce_mean_sum = (tfops.allreduce_sum(by2) * tfops.allreduce_mean(by2))/sum(by2.shape)
    tfops.int_shape(by2)
    tfops.actnorm("by2",by2)

def add_namescope(nc):
    n = nc("default", 10)
    for i in range(1,int(len(n)/2)- 2):
        add(n[i], n[i+1][:n[i].shape[0]])
         
@add_namescope
def namescope(name, count=None):
    with tf.name_scope(name) as s:
        if count is None:
            return tf.Variable([1,2], name=name)
        else:
            ranges=[ tf.range(i) for i in range(1,count)]
            tensors = {}
            for i in range(1,count-1):
                tensors[i] = (tf.Variable(ranges[i],"%s%d" % (name, i)))
                tensors["%d1" % i] = get_variable("%s%d" % (name, i), ranges[i])
            
            return tensors
            
namescope
#ops()




