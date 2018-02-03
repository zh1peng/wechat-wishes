# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 08:21:52 2018

@author: 懒麻蛇
"""

import collections
import numpy as np
import tensorflow as tf

poetry_file =r'E:\Git\wechat-wishes\poetry.txt'

# 诗集
poetrys = []
with open(poetry_file, "r", encoding='utf-8',) as f:
	for line in f:
		try:
			title, content = line.strip().split(':')
			content = content.replace(' ','')
			if '_' in content or '(' in content or '（' in content or '《' in content or '[' in content:
				continue
			if len(content) < 5 or len(content) > 79:
				continue
			content = '[' + content + ']'
			poetrys.append(content)
		except Exception as e: 
			pass
# 按诗的字数排序
poetrys = sorted(poetrys,key=lambda line: len(line))
print('唐诗总数: ', len(poetrys))


all_words = []
for poetry in poetrys:
	all_words += [word for word in poetry]
counter = collections.Counter(all_words)
count_pairs = sorted(counter.items(), key=lambda x: -x[1])
words, _ = zip(*count_pairs)

# 取前多少个常用字
words = words[:len(words)] + (' ',)
# 每个字映射为一个数字ID
word_num_map = dict(zip(words, range(len(words))))
# 把诗转换为向量形式，参考TensorFlow练习1
to_num = lambda word: word_num_map.get(word, len(words))
poetrys_vector = [ list(map(to_num, poetry)) for poetry in poetrys]

# 每次取64首诗进行训练  
batch_size = 64
n_chunk = len(poetrys_vector) // batch_size  

class DataSet(object):
    def __init__(self,data_size):
        self._data_size = data_size
        self._epochs_completed = 0
        self._index_in_epoch = 0
        self._data_index = np.arange(data_size)

    def next_batch(self,batch_size):
        start = self._index_in_epoch
        if start + batch_size > self._data_size:
            np.random.shuffle(self._data_index)
            self._epochs_completed = self._epochs_completed + 1
            self._index_in_epoch = batch_size
            full_batch_features ,full_batch_labels = self.data_batch(0,batch_size)
            return full_batch_features ,full_batch_labels 
        else:
            self._index_in_epoch += batch_size
            end = self._index_in_epoch
            full_batch_features ,full_batch_labels = self.data_batch(start,end)
            if self._index_in_epoch == self._data_size:
                self._index_in_epoch = 0
                self._epochs_completed = self._epochs_completed + 1
                np.random.shuffle(self._data_index)
            return full_batch_features,full_batch_labels

    def data_batch(self,start,end):
        batches = []
        for i in range(start,end):
            batches.append(poetrys_vector[self._data_index[i]])

        length = max(map(len,batches))

        xdata = np.full((end - start,length), word_num_map[' '], np.int32)  
        for row in range(end - start):  
            xdata[row,:len(batches[row])] = batches[row]  
        ydata = np.copy(xdata)  
        ydata[:,:-1] = xdata[:,1:]  
        return xdata,ydata

#---------------------------------------RNN--------------------------------------#  

input_data = tf.placeholder(tf.int32, [batch_size, None])  
output_targets = tf.placeholder(tf.int32, [batch_size, None])  
# 定义RNN  
def neural_network(model='lstm', rnn_size=128, num_layers=2):  
    if model == 'rnn':  
        cell_fun = tf.nn.rnn_cell.BasicRNNCell  
    elif model == 'gru':  
        cell_fun = tf.nn.rnn_cell.GRUCell  
    elif model == 'lstm':  
        cell_fun = tf.nn.rnn_cell.BasicLSTMCell  

    cell = cell_fun(rnn_size, state_is_tuple=True)  
    cell = tf.nn.rnn_cell.MultiRNNCell([cell] * num_layers, state_is_tuple=True)  

    initial_state = cell.zero_state(batch_size, tf.float32)  

    with tf.variable_scope('rnnlm'):  
        softmax_w = tf.get_variable("softmax_w", [rnn_size, len(words)])  
        softmax_b = tf.get_variable("softmax_b", [len(words)])  
        with tf.device("/cpu:0"):  
            embedding = tf.get_variable("embedding", [len(words), rnn_size])  
            inputs = tf.nn.embedding_lookup(embedding, input_data)  

    outputs, last_state = tf.nn.dynamic_rnn(cell, inputs, initial_state=initial_state, scope='rnnlm')  
    output = tf.reshape(outputs,[-1, rnn_size])  

    logits = tf.matmul(output, softmax_w) + softmax_b  
    probs = tf.nn.softmax(logits)  
    return logits, last_state, probs, cell, initial_state 


#-------------------------------生成古诗---------------------------------#  
# 使用训练完成的模型  

def gen_head_poetry(heads, type):
    if type != 5 and type != 7:
        print('The second para has to be 5 or 7!')
        return   
    def to_word(weights):  
        t = np.cumsum(weights)  
        s = np.sum(weights)  
        sample = int(np.searchsorted(t, np.random.rand(1)*s))  
        return words[sample]  

    _, last_state, probs, cell, initial_state = neural_network()
    Session_config = tf.ConfigProto(allow_soft_placement = True)
    Session_config.gpu_options.allow_growth=True 

    with tf.Session(config=Session_config) as sess: 
        with tf.device('/cpu:0'): 

            sess.run(tf.global_variables_initializer())  

            saver = tf.train.Saver(tf.global_variables())  
            saver.restore(sess, 'model/poetry.module-99')
            poem = ''
            for head in  heads:
                flag = True
                while flag:

                    state_ = sess.run(cell.zero_state(1, tf.float32)) 

                    x = np.array([list(map(word_num_map.get, u'['))])  
                    [probs_, state_] = sess.run([probs, last_state], feed_dict={input_data: x, initial_state: state_})  

                    sentence = head

                    x = np.zeros((1,1))  
                    x[0,0] = word_num_map[sentence]  
                    [probs_, state_] = sess.run([probs, last_state], feed_dict={input_data: x, initial_state: state_})  
                    word = to_word(probs_)
                    sentence += word  

                    while word != u'。':  
                        x = np.zeros((1,1))  
                        x[0,0] = word_num_map[word]  
                        [probs_, state_] = sess.run([probs, last_state], feed_dict={input_data: x, initial_state: state_})  
                        word = to_word(probs_)
                        sentence += word  

                    if len(sentence) == 2 + 2 * type:
                        sentence += u'\n'
                        poem += sentence
                        flag = False

            return poem

print(gen_head_poetry(u'天下之大',5)) 



