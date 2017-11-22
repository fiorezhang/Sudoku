#sudoku_dataset
#copyright: fiorezhang@sina.com

import numpy as np
from sudoku_generator import generator as gen

def load_data(size, visible, num):
	x = np.zeros((num, size, size), dtype='int8')
	y = np.zeros((num, size, size), dtype='int8')
	
	for i in range(num):
		x[i], y[i] = gen(size, visible)
				
	return x, y
