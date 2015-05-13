
from nnet.nnio import save_knowledge
from os.path import isfile
from nnet.make_net import make_net
from nnet.prepare import conormalize_data
from sklearn.calibration import CalibratedClassifierCV
from sklearn.cross_validation import ShuffleSplit
from utils.features import chain_feature_generators
from utils.outliers import filter_data
from utils.postprocess import scale_to_priors
from numpy import bincount, float64
from validation.optimize import is_nonstr_iterable
from validation.score import calc_logloss


def train_NN(train, labels, test, outlier_frac = 0, outlier_method = 'OCSVM', use_calibration = False, normalize_log = True,
		use_rescale_priors = False, extra_feature_count = 0, extra_feature_seed = 0, **parameters):
	"""
		Train a neural network, for internal use by other functions in this file.
	"""
	train, test = chain_feature_generators(train, labels, test, extra_features = extra_feature_count, seed = extra_feature_seed)
	train, test = conormalize_data(train, test, use_log = normalize_log)
	if outlier_frac:
		train, labels = filter_data(train, labels, cut_outlier_frac = outlier_frac, method = outlier_method)
	net = make_net(NFEATS = train.shape[1], **parameters)
	if use_calibration:
		net = CalibratedClassifierCV(net, method = 'sigmoid', cv = ShuffleSplit(train.shape[0], n_iter = 1, test_size = 0.2))
	net.fit(train, labels - 1)
	return net, train, test


def train_test_NN(train, labels, test, use_rescale_priors = False, normalize_log = True, extra_feature_count = 0,
		extra_feature_seed = 0, **parameters):
	"""
		Train and test a neural network given a set of parameters (which should contain no iterables). Returns test data probabilities for use in (parallel) optimizer.
	"""
	net, train, test = train_NN(train, labels, test, use_rescale_priors = use_rescale_priors,
		normalize_log = normalize_log, extra_feature_count = extra_feature_count,
		extra_feature_seed = extra_feature_seed, **parameters)
	prediction = net.predict_proba(test)
	if use_rescale_priors:
		prediction = scale_to_priors(prediction, priors = bincount(labels)[1:] / float64(len(labels)))
	return prediction


def make_pretrain(pretrain_path, data, labels, minimum_train_loss = 0.7, **params):
	"""
		Make a pretrain file given parameters. If there are iterable parameters, a 'random' one is chosen.
	"""
	if not pretrain_path or isfile(pretrain_path):
		return
	print 'pretraining file not found, pretraining a network now'
	pretrain_params = {
		'dense1_nonlinearity': 'leaky20',
		'dense1_init': 'glorot_uniform',
		'dense1_size': params['dense1_size'],
		'dense2_size': params['dense2_size'],
		'dense3_size': params['dense3_size'],
		'learning_rate': params['learning_rate'],
		'learning_rate_scaling': 10,
		'momentum': 0.9,
		'momentum_scaling': 10,
		'dropout1_rate': 0.5 if params['dense2_size'] else 0,
		'dropout2_rate': 0.5 if params['dense3_size'] else 0,
		'max_epochs': 1000,
		'extra_feature_count': params['extra_feature_count'],
	}
	for key, val in pretrain_params.items():
		if is_nonstr_iterable(val):
			pretrain_params[key] = val[0]
	net, train, duplicate = train_NN(data, labels, data[0:1, :], **pretrain_params)
	train_err = calc_logloss(net.predict_proba(train), labels)
	assert train_err < minimum_train_loss, 'Pre-training did not converge ({0:.4f} >= {1:.4f})'.format(train_err, minimum_train_loss)
	save_knowledge(net, pretrain_path)

