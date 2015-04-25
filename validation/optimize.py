
"""
	General code to optimize parameters to a model.
"""

from collections import Iterable, OrderedDict
from json import dumps, loads
from os.path import isdir, join
from itertools import product
from numpy import zeros, prod
from settings import OPTIMIZE_RESULTS_DIR, VERBOSITY


def is_nonstr_iterable(obj):
	"""
		http://stackoverflow.com/questions/19943654/type-checking-an-iterable-type-that-is-not-a-string
	"""
	return not isinstance(obj, str) and isinstance(obj, Iterable)


class GridOptimizer(object):

	def __init__(self, validator, use_caching = True, **params):
		"""
			Create a grid optimizer to do a grid search for optimal parameter vaues.

			:param validator: A validator to use for getting the score for each parameter.
			:param params: The parameters you want to compare, with a list of the values to try:

				GridOptimizer(validator, learning_rate = [1, 0.1, 0.01], hidden_layer_size = [30, 50], momentum = 0.9)

			Results are cached in the directory set by settings.OPTIMIZE_RESULTS_DIR
		"""
		assert isdir(OPTIMIZE_RESULTS_DIR), 'Make sure that "{0:s}" exists, it change it\'s value in settings'.format(OPTIMIZE_RESULTS_DIR)
		self.validator = validator
		self.use_caching = bool(use_caching)
		self.fixed_params = {key: val for key, val in params.items() if not is_nonstr_iterable(val)}
		self.iter_params = OrderedDict((key, val) for key, val in params.items() if is_nonstr_iterable(val))
		self.labels, self.indices = zip(*[(key, val) for key, val in params.items() if is_nonstr_iterable(val)])
		self.dims = tuple(len(li) for li in self.indices)
		self._remaining_dim = [prod(self.dims[k+1:], dtype = int) for k in range(len(self.dims))]
		print self.dims
		self.results = zeros(self.dims)
		#euclidean_product = list(product(*self.iter_params.values()))
		#""" Generate every possible combination of parameters. """
		#self.euclidean_params = []
		#for batch in euclidean_product:
		#	params = {key: val for key, val in zip(self.iter_params.keys(), batch)}
		#	params.update(self.fixed_params)
		#	self.euclidean_params.append(params)
		print 'grid optimize: {0:s} comparisons x {1:d} rounds = {2:d} iterations'.format(' x '.join(str(d) for d in self.dims), self.validator.rounds, prod(self.dims) * self.validator.rounds)
		for k in range(prod(self.dims)):
			print k, self.to_coordinate(k), self.from_coordinate(self.to_coordinate(k))
		exit()

	def params_name(self, params):
		params = OrderedDict(sorted(params.items()))
		return (
			'_'.join('{0:s}-{1:}'.format(key, val) for key, val in params.items()),
			', '.join('{0:s} = {1:}'.format(key, val) for key, val in params.items()),
		)

	def _store_results(self, filepath, logloss, accuracy, duration):
		with open(filepath, 'w+') as fh:
			fh.write(dumps({'logloss': logloss, 'accuracy': accuracy, 'duration': duration}, indent = 4, sort_keys = True))

	def _load_results(self, filepath):
		"""
			:return: (logloss, accuracy, duration) tuple
		"""
		with open(filepath, 'r') as fh:
			d = loads(fh.read())
		return d['logloss'], d['accuracy'], d['duration'],

	def to_coordinate(self, index):
		"""
			Convert from 'element N' to 'result matrix coordinate [x, y, z]'.
		"""
		return [index // self._remaining_dim[k] % dim for k, dim in enumerate(self.dims)]

	def from_coordinate(self, coordinate):
		"""
			Convert from 'result matrix coordinate [x, y, z]' to 'element N'.
		"""
		return sum(tuple(coordinate[k] * self._remaining_dim[k] for k in range(len(self.dims))))

	def get_single_batch(self, params, round, name):
		"""
			Return a single batch (intended for internal use).
		"""
		train_data, train_classes, test_data = self.validator.start_round(round)
		if VERBOSITY >= 2:
			print 'calculate: %s, round #%d/%d' % (name, round + 1, self.validator.rounds)
		return params, train_data, train_classes, test_data

	def yield_batches(self):
		"""
			Iterator that goes over the different training parameters and the different cross validation rounds for each of them.

			:return: An iterator with (parameters, train_data, train_classes, test_data) tuple on each iteration.
		"""
		""" Create every combination of parameter. """
		for self.current, params in enumerate(self.euclidean_params):
			""" Do a validator iteration for each parameter combination. """
			self.validator.reset()
			filename, dispname = self.params_name(params)
			print 'calculating {0:d} rounds for parameters {1:s}'.format(self.validator.rounds, dispname)
			for round in range(self.validator.rounds):
				if self.use_caching:
					try:
						""" Try to load cache. """
						self._load_results(join(OPTIMIZE_RESULTS_DIR, filename))
					except IOError:
						""" No cache; yield the data (storage happens elsewhere). """
						yield self.get_single_batch(params, round, dispname)
					else:
						""" Cache loaded; handle. """
						if VERBOSITY >= 2:
							print 'cache: %s, round #%d/%d' % (dispname, round + 1, self.validator.rounds)
				else:
					yield self.get_single_batch(params, round, dispname)

	def register_results(self, prediction):
		assert self.current is not None, 'You should start iterating using .yield_batches() before registering any results.'
		params = self.euclidean_params[self.current]
		filename, dispname = self.params_name(params)
		results = self.validator.add_prediction(prediction)
		self._store_results(join(OPTIMIZE_RESULTS_DIR, filename), *results)

	def print_plot_results(self):
		pass

