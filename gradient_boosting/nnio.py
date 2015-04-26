
from cPickle import dump, load
from os import makedirs
from os.path import dirname, join


def save_net(net, filepath):
	"""
		Save a neural network to disk in the current state.

		:param net: nolearn/lasagne network.

		This is not guaranteed to work between versions or computers!
	"""
	#todo: there has to be a better way
	with open(filepath, 'wb+') as fh:
		dump(obj = net, file = fh, protocol = -1)


def load_net(filepath):
	"""
		Load a neural network from disk.

		:return: nolearn/lasagne network including weights and parameters.
	"""
	with open(filepath, 'r') as fh:
		return load(file = fh)


class SnapshotSaver(object):
	def __init__(self, every = 500, base_name = ''):
		self.every = every
		self.base_path = join(base_name, dirname(base_name))
		try:
			makedirs(self.base_path)
		except IOError:
			pass

	def __call__(self, nn, train_history):
		epoch = train_history[-1]['epoch']
		if epoch % self.every == 0:
			save_net(nn, self.base_path)
			print 'saved network to "{0:s}" at iteration {1:d}'.format(self.base_path, epoch)

