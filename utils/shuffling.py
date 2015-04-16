
"""
	These functions let you pseudo-randomly shuffle data. The result is consistently the same for the same data. The
	functions also return a key that can be used to undo the shuffling, useful for cross-validation.
"""

from numpy import zeros, array
from random import shuffle as pyshuffle
from numpy.random.mtrand import random_integers


def get_sample_key(N, k, seed):
	"""
		Get a pseudorandom key for sampling from data.

		:param N: Number of items in population.
		:param k: Number of samples to draw.
		:param seed: The seed for shuffling (best leave unchanged to compare results).
		:return: Key for sampling.
	"""
	return random_integers(low = 0, high = N, size = k)


def get_permutation_key(N, seed):
	"""
		Get a pseudorandom key for shuffling data.

		:param N: Number of items in population.
		:param seed: The seed for shuffling (best leave unchanged to compare results).
		:return: Key for permutatoin.
	"""
	key = array(range(N))
	pyshuffle(key, random = lambda: seed)
	return key


def shuffle(data, classes = None, seed = 4242):
	"""
		Shuffle the rows of data. For training data, which is ordered. Key can be used to unshuffle it before cross-validation or submission.

		:param data: A data ndarray.
		:param classes: Optionally, the true classes [ndarray of ints].
		:param seed: The seed for shuffling (best leave unchanged to compare results).
		:return: shuffled_data, unshuffle_key
	"""
	key = get_permutation_key(N = data.shape[0], seed = (seed / 10000.) % 10000)
	data = data[key, :]
	if classes is not None:
		classes = classes[key, :]
	return data, classes, key


def get_inverse_key(key):
	"""
		Given a shuffle key, create a key that will undo that shuffling.
	"""
	invkey = zeros(key.shape, dtype = int)
	for indx, val in enumerate(key):
		invkey[val] = indx
	return invkey


def unshuffle(data, classes = None, key = None):
	"""
		Unshuffle data that has been shuffled with the shuffle method.

		:param data: A data ndarray.
		:param classes: Optionally, the true classes.
		:key: The key generated by the shuffle method.
		:return: unshuffled_data
	"""
	assert key is not None, 'Argument "key" should be provided (it\'s the third argument, or use keyword)'
	invkey = get_inverse_key(key)
	data = data[invkey, :]
	if classes is not None:
		classes = classes[invkey, :]
	return data, classes


if __name__ == '__main__':
	"""
		Test / demonstration of sorting and unsorting.
	"""
	data = zeros((8, 3))
	for k in range(8):
		data[k, :] = k
	sdata, classes, key = shuffle(data)
	print 'shuffled'
	print sdata
	udata, classes = unshuffle(sdata, key = key)
	print 'unshuffled'
	print udata
	print 'shuffle key:  ', key
	print 'unshuffle key:', get_inverse_key(key)
	print 'sampling:', get_sample_key(10, 12, 4242)


