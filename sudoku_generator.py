#sudoku_generator
#copyright: fiorezhang@sina.com

import numpy as np

#calculate the remainder for x in range: 1~y
def remainder(x, y):
	return (x-1)%y+1

''' #comment out the original matrix generator as generate in a function
#define the size of matrix
SIZE = 3

m_basic = np.zeros((SIZE * SIZE, SIZE * SIZE), dtype='int8')
'''

'''too complicated, easier way as below
#generate the 1st piece with SIZE * SIZE size
temp = 0
for i in range(SIZE):
	for j in range(SIZE):
		temp += 1
		m_basic[i, j] = temp
		
#generate the 1st line of pieces with (SIZE*SIZE) * SIZE size
for i in range(SIZE):
	for k in range(SIZE):
		for j in range(SIZE):
			m_basic[i, k*SIZE+j] = remainder((m_basic[i, j] + k*SIZE), SIZE*SIZE)
		
#generate the whole matrix
for k in range(SIZE):
	for i in range(SIZE):
		for j in range(SIZE*SIZE):
			m_basic[k*SIZE+i, j] = remainder((m_basic[i, j] + k), SIZE*SIZE)
'''
'''
#generate one matrix which fulfill the sudoku rule, as the basic for others
for i in range(SIZE*SIZE):
	for j in range(SIZE*SIZE):
		m_basic[i, j] = remainder((1 + SIZE*(i%SIZE) + int(i/SIZE) + j), SIZE*SIZE)
#print(m_basic)
'''


'''define some functions to generate new matrix based from the original matrix, 
	including swap rows within same bundle, or swap two bundles of rows, 
	similarlly to the columns, finally we make a re-map from 1~n to a random sort of 1~n
'''
#swap rows within a bundle, check the row number
def swap_row(m, x, y):
	s = m.shape[0]#columns/rows in matrix
	b = (int)(np.sqrt(s))#bundles of columns/rows in matrix
	t = np.zeros(s)#use to buffer the data to be swap
	#check whether x and y in a bundle
	if (int(x/b) != int(y/b)) or (x < 0) or (x >= s) or (y < 0) or (y >= s) or (x == y):
		print('ERROR'),
		return m
	
	for j in range(s):
		t[j] = m[x, j]
		m[x, j] = m[y, j]
		m[y, j] = t[j]
		
	#print(m)
	return m

#swap bundles of rows, check the bundle number
def swap_row_b(m, x, y):
	s = m.shape[0]#columns/rows in matrix
	b = (int)(np.sqrt(s))#bundles of columns/rows in matrix
	t = np.zeros(s)#use to buffer the data to be swap
	#check x and y
	if (x < 0) or (x >= b) or (y < 0) or (y >= b) or (x == y): 
		print('ERROR'),
		return m
		
	for k in range(b):
		for j in range(s):
			t[j] = m[x*b+k, j]
			m[x*b+k, j] = m[y*b+k, j]
			m[y*b+k, j] = t[j]
			
	#print(m)
	return m

#swap columns within a bundle, check the colunm number
def swap_col(m, x, y):
	s = m.shape[0]#columns/rows in matrix
	b = (int)(np.sqrt(s))#bundles of columns/rows in matrix
	t = np.zeros(s)#use to buffer the data to be swap
	#check whether x and y in a bundle
	if (int(x/b) != int(y/b)) or (x < 0) or (x >= s) or (y < 0) or (y >= s) or (x == y):
		print('ERROR'),
		return m
	
	for i in range(s):
		t[i] = m[i, x]
		m[i, x] = m[i, y]
		m[i, y] = t[i]
		
	#print(m)
	return m

#swap bundles of columns, check the bundle number
def swap_col_b(m, x, y):
	s = m.shape[0]#columns/rows in matrix
	b = (int)(np.sqrt(s))#bundles of columns/rows in matrix
	t = np.zeros(s)#use to buffer the data to be swap
	#check x and y
	if (x < 0) or (x >= b) or (y < 0) or (y >= b) or (x == y): 
		print('ERROR'),
		return m
		
	for k in range(b):
		for i in range(s):
			t[i] = m[i, x*b+k]
			m[i, x*b+k] = m[i, y*b+k]
			m[i, y*b+k] = t[i]
			
	#print(m)
	return m

#remap 1~n in matrix into a random shuffled serial of 1~n, ex: [123456789]->[597326841]
def remap(m):
	s = m.shape[0]
	n = np.zeros((s, s), dtype='int8')#new a matrix to contain the remapped data
	t = np.zeros(s, dtype='int8')
	
	for i in range(s):
		t[i] = i+1
	np.random.shuffle(t)
	#print(t)
	
	for i in range(s):
		for j in range(s):
			n[i, j] = t[(m[i, j]-1)]
	
	#print(n)		
	return n
	
#shuffle a matrix with swap rows/columns and remap the cell
def shuffle(m):
	s = m.shape[0]
	b = (int)(np.sqrt(s))
	
	m = remap(m)

	for i in range(s):
		l = np.random.randint(b, size=1)
		[j, k] = np.random.randint(l*b, l*b+b, size=2)
		#print(j, k)
		if j != k:
			m = swap_row(m, j, k)
	
	for i in range(b):
		[j, k] = np.random.randint(b, size=2)
		#print(j, k)
		if j != k: 
			m = swap_row_b(m, j, k)

	for i in range(s):
		l = np.random.randint(b, size=1)
		[j, k] = np.random.randint(l*b, l*b+b, size=2)
		#print(j, k)
		if j != k:
			m = swap_col(m, j, k)

	for i in range(b):
		[j, k] = np.random.randint(b, size=2)
		#print(j, k)
		if j != k:
			m = swap_col_b(m, j, k)

	return m

#generate a matrix with some cell masked as 0, the visible cells close to the percentage given
def mask(m, v):
	s = m.shape[0]
	
	n = np.random.rand(s, s)
	#print(n)
	#o = np.where(n<=v, 1, 0) #calculate how many '1' in the sparse matrix
	#print(o)
	#print(o.sum(), "/", s*s, " -- ", o.sum()/(s*s), v)
	m = np.where(n<=v, m, 0)

	return m

#generate a pair of matrix, return the matrix and the masked matrix. Size: must be a square number, how many rows. Visible: a float within 0~1, percentage for how many visible(unmasked)
def generator(size, visible):
	s = size
	v = visible
	b = (int)(np.sqrt(s))
	m = np.zeros((s, s), dtype='int8')
	for i in range(s):
		for j in range(s):
			m[i, j] = remainder((1 + b*(i%b) + int(i/b) + j), s)
			
	m = shuffle(m)
	n = mask(m, v)
	return (n, m)

####test functions
'''
ans, que = generator(9, 0.9)
print(ans),
print(que),
'''