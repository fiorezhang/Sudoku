#sudoku_rnn
#copyright: fiorezhang@sina.com

import numpy as np
from keras.models import Sequential
from keras import layers
from sudoku_dataset import load_data as load


#global variables for sudoku training/test data set
MATRIX_SIZE = 4
VISIBLE = 0.75
TRAIN_SIZE = 10000
TEST_SIZE = 1000

#transfer matrix to a one-hot serial
def oh_encode(m):
	s = m.shape[0]
	c = np.zeros((s*s, s+1), dtype='int8')
	
	for i in range(s*s):
		t = m[(int)(i/s), (int)(i%s)]
		c[i, t] = 1
		
	return c
	
#transfer one-hot serial to matrix
def oh_decode(c):
	s = (int)(np.sqrt(c.shape[0]))
	m = np.zeros((s, s), dtype='int8')
	
	for i in range(s*s):
		for j in range(s+1):
			if c[i, j] > 0:
				m[(int)(i/s), (int)(i%s)] = j
	
	return m

#generate matrix from sudoku generator/dataset functions	
print('-'*50),
print('Generating Data... '),
print('Matrix size: ', MATRIX_SIZE, ', visible percentage: ', VISIBLE*100, '%'),
print('Train samples: ', TRAIN_SIZE, ', test samples: ', TEST_SIZE),
(x_train_m, y_train_m), (x_test_m, y_test_m) = load(MATRIX_SIZE, VISIBLE, TRAIN_SIZE, TEST_SIZE)
x_train = np.zeros((TRAIN_SIZE, MATRIX_SIZE*MATRIX_SIZE, MATRIX_SIZE+1), dtype='int8')
y_train = np.zeros((TRAIN_SIZE, MATRIX_SIZE*MATRIX_SIZE, MATRIX_SIZE+1), dtype='int8')
for i in range (TRAIN_SIZE):
	x_train[i], y_train[i] = oh_encode(x_train_m[i]), oh_encode(y_train_m[i])
x_test = np.zeros((TEST_SIZE, MATRIX_SIZE*MATRIX_SIZE, MATRIX_SIZE+1), dtype='int8')
y_test = np.zeros((TEST_SIZE, MATRIX_SIZE*MATRIX_SIZE, MATRIX_SIZE+1), dtype='int8')
for i in range (TEST_SIZE):
	x_test[i], y_test[i] = oh_encode(x_test_m[i]), oh_encode(y_test_m[i])
	
#print(x_test_m.shape), 
#print(x_test.shape),
#print(x_test_m[0]),
#print(x_test[0]),
#print(y_test_m[0]),
#print(y_test[0]),
print('-'*50),	

#set parameters for keras model
RNN = layers.LSTM
HIDDEN_SIZE = 512
BATCH_SIZE = 128
LAYERS = 2

#Build the RNN model
print('-'*50),
print('Building Model... '),
model = Sequential()
#input the one-hot data transferred from a sudoku matrix, connect to a hidden layer
model.add(RNN(HIDDEN_SIZE, input_shape=(MATRIX_SIZE*MATRIX_SIZE, MATRIX_SIZE+1)))
#as we expect the output as also a one-hot data, say s*s output, so repeat s*s times.
model.add(layers.RepeatVector(MATRIX_SIZE*MATRIX_SIZE))
#connect again to RNN network, notice we expect a 3D output so set return_sequences to True
for _ in range(LAYERS):
	model.add(RNN(HIDDEN_SIZE, return_sequences=True))
#add a dense layer with the s*s vector flattened, then 3D turn to 2D, need a catagory for each output number in matrix
model.add(layers.TimeDistributed(layers.Dense(MATRIX_SIZE+1)))
model.add(layers.Activation('softmax'))
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
model.summary()
print('-'*50),

#train the model and print information during the process
print('-'*50), 
print('Training...'),
for iteration in range(1, 100):
	print(),
	print('-'*50),
	print('Iteration', iteration)
	model.fit(x_train, y_train,
          batch_size=BATCH_SIZE,
          epochs=1,
          validation_data=(x_test, y_test))
	#show result in the middle
	for i in range(1): 
		ind = np.random.randint(0, len(x_test))
		rowx, rowy = x_test[np.array([ind])], y_test[np.array([ind])]
		preds = model.predict_classes(rowx, verbose=0)
		question = oh_decode(rowx[0])
		correct = oh_decode(rowy[0])
		guess = preds[0].reshape(question.shape[0], question.shape[1])	
		print('Q','- '*25),
		print(question),
		print('A','- '*25),
		print(correct),
		print('G','- '*25),
		print(guess),
		print('- '*25),

####test functions
'''
print('Generate Data +'),
(x, y), (z, u) = load(9, 0.7, 10000, 1000)
print('Generate Data -'),
o_y = oh_encode(y[0])
print(y[0]),
print(o_y),
t = oh_decode(o_y)
print(t)
'''