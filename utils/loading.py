
"""
	Load train and test data.

	Performance for me (Mark):
	- first load with this method:   9.5s
	- later loads with this method:  0.3s
	- any load with previous method: 8.8s
	So the initial loading can be faster, but there's no need.
"""

from tempfile import gettempdir
from numpy import uint16, load, save, empty
from os.path import join
from settings import VERBOSITY, TRAIN_DATA_PATH, TEST_DATA_PATH, TRAINSIZE, TESTSIZE, RAW_NFEATS


def load_training_data(filepath):
	"""
		Load training data.

		:return: data[ndarray], classes[array], features[list]

		Notes:
		* I tried using Pandas to have a dataframe with labels, but it seems I can't skip class label column. -Mark
		* The samples are numbered from 1 because the data file does that. Sorry.
	"""
	with open(filepath, 'r') as fh:
		cells = [line.split(',') for line in fh.read().splitlines()]
	features = cells[0][1:-1]
	classes = empty((TRAINSIZE,), dtype = uint16)
	data = empty((TRAINSIZE, RAW_NFEATS), dtype = uint16)
	for k, row in enumerate(cells[1:]):
		classes[k] = row[-1].split('_')[-1]
		data[k, :] = row[1:-1]
	return data, classes, features


def load_testing_data(filepath):
	"""
		Load testing data.

		:return: data[ndarray], features[list]
	"""
	with open(filepath, 'r') as fh:
		cells = [line.split(',') for line in fh.read().splitlines()]
	features = cells[0][1:]
	data = empty((TESTSIZE, RAW_NFEATS), dtype = uint16)
	for k, row in enumerate(cells[1:]):
		data[k, :] = row[1:]
	return data, features


def get_training_data(filepath = TRAIN_DATA_PATH):
	"""
		Gets the training data from the CSV file, caching it in temporary directory for speed.
	"""
	try:
		data = load(join(gettempdir(), 'cache_train_data.npy'))
		features = load(join(gettempdir(), 'cache_train_features.npy'))
		classes = load(join(gettempdir(), 'cache_train_classes.npy'))
		if VERBOSITY >= 1:
			print 'loaded train data from cache in "{0:s}"'.format(gettempdir())
	except IOError:
		data, classes, features = load_training_data(filepath = filepath)
		save(join(gettempdir(), 'cache_train_data.npy'), data)
		save(join(gettempdir(), 'cache_train_features.npy'), features)
		save(join(gettempdir(), 'cache_train_classes.npy'), classes)
		if VERBOSITY >= 1:
			print 'loaded train data directly'
	return data, classes, features


def get_testing_data(filepath = TEST_DATA_PATH):
	"""
		Gets the test data from the CSV file, caching it in temporary directory for speed.
	"""
	try:
		data = load(join(gettempdir(), 'cache_test_data.npy'))
		features = load(join(gettempdir(), 'cache_test_features.npy'))
		if VERBOSITY >= 1:
			print 'loaded test data from cache in "{0:s}"'.format(gettempdir())
	except IOError:
		data, features = load_testing_data(filepath = filepath)
		save(join(gettempdir(), 'cache_test_data.npy'), data)
		save(join(gettempdir(), 'cache_test_features.npy'), features)
		if VERBOSITY >= 1:
			print 'loaded test data directly'
	return data, features


def get_preproc_data(pipeline, train_filepath = TRAIN_DATA_PATH, test_filepath = TEST_DATA_PATH, expand_confidence = None):
	"""
		Load pre-processed version of train and test data using caching.
	"""
	from utils.expand_train import expand_from_test
	key = '_'.join([c[0] for c in (pipeline.steps if pipeline else [])]) + ('' if expand_confidence is None else ('_etc' + '{0:.3f}'.format(expand_confidence)[2:]))
	try:
		train = load(join(gettempdir(), 'cache_pp_train_{0:s}.npy'.format(key)))
		labels = load(join(gettempdir(), 'cache_pp_labels_{0:s}.npy'.format(key)))
		test = load(join(gettempdir(), 'cache_pp_test_{0:s}.npy'.format(key)))
		if VERBOSITY >= 1:
			print 'loaded transformed NN train and test data from cache in "{0:s}" with key "{1:s}"'.format(gettempdir(), key)
	except IOError:
		if VERBOSITY >= 1:
			print 'transforming NN train and test data and saving to cache with key "{0:s}"'.format(key)
		train, labels = get_training_data(filepath = train_filepath)[:2]
		test = get_testing_data(filepath = test_filepath)[0]
		if expand_confidence:
			train, labels = expand_from_test(train, labels, test, confidence = expand_confidence)
		if pipeline:
			train = pipeline.fit_transform(train, labels)
			test = pipeline.transform(test)
		save(join(gettempdir(), 'cache_pp_train_{0:s}.npy'.format(key)), train)
		save(join(gettempdir(), 'cache_pp_labels_{0:s}.npy'.format(key)), labels)
		save(join(gettempdir(), 'cache_pp_test_{0:s}.npy'.format(key)), test)
	return train, labels, test


"""
	Sorry for removing the TEST, TRAIN and LABELS globals. It is a bad idea to load train and test data if only one of them might be needed.
"""


if __name__ == '__main__':
	train_data, classes, features = get_training_data()
	test_data, features = get_testing_data()


