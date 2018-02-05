import tensorflow as tf
import numpy as np

centerword = tf.Variable(np.array([1,2,3]),dtype=tf.float32)
targetword = tf.Variable(np.array([4,5,6]),dtype=tf.float32)
negwords = tf.Variable(np.array([[7,8,9],[3,6,9]]),dtype=tf.float32)


全是Variable也可以相乘

matmul和multiply不同

Variable要指定dtype

第一，不能[3]x[1,3]
要都是rank 2
用expand_dims

全部要初始化一次才可以

一篇with session怎么使用

以及 语义化的重要性，和短小 单一职责的函数

单元测试 和 单元函数的重要性

从大局开始 声明式的规划 + 从小处 进行函数式单一职责的编程

def grad_of_being_closer(a,b):
    activated_dot = tf.sigmoid(tf.matmul(tf.transpose(tf.expand_dims(b,1)),tf.expand_dims(a,1))) # 相乘越大 越接近1， log的绝对值越小(0,1)， -log的值越小， cost越小
    return (- tf.log(activated_dot))
def grad_of_being_farther(a,b):
    dot = a * tf.transpose(b)
    activated_dot = tf.sigmoid(- dot)
    return (- tf.log(activated_dot))
def get_cost(centerword,targetword,negwords):
    # 循环所有negwords
    negword_costs = [ grad_of_being_farther(centerword,negword) for negword in negwords ]
    # 把cost加起来
    J_negSample = grad_of_being_closer(centerword,targetword) + tf.reduce_sum(negword_costs)
    return J_negSample

sess = tf.Session()
init_op = tf.global_variables_initializer()
sess.run(init_op)
print(sess.run(grad_of_being_closer(centerword,targetword)))
# print(get_cost(centerword,targetword,negwords))