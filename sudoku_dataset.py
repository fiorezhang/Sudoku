#sudoku_dataset
#copyright: fiorezhang@sina.com

import numpy as np
from sudoku_generator import generator as gen

def load_data(size, visible, num_train, num_test):
	x_train = np.zeros((num_train, size, size), dtype='int8')
	y_train = np.zeros((num_train, size, size), dtype='int8')
	x_test  = np.zeros((num_test,  size, size), dtype='int8')
	y_test  = np.zeros((num_test,  size, size), dtype='int8')
	
	for i in range(num_train):
		x_train[i], y_train[i] = gen(size, visible)
		
	for i in range(num_test):
		x_test[i], y_test[i] = gen(size, visible)
		
	return (x_train, y_train), (x_test, y_test)

####test functions	
'''
(x_train, y_train), (x_test, y_test) = load_data(9, 0.7, 20, 5)
print(x_test),
print(y_test),
'''