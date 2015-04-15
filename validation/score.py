
"""
	Functions for assessing the performance of different classifiers.
"""

from numpy import array, all, ones, zeros
from numpy.random import uniform
from scipy import clip, log, subtract
from validation.normalize import rows_normalized, normalize_probabilities


def logloss(predictions, true_classes, epsilon = 1.e-15):
	"""
		The multiclass logarithmic loss function used in the competition, including the truncation.
		
		:param predictions: An Nx9 ndarray with prediction probabilities. Rows are samples in the same order as true_classes, and columns correspond to classes (from 1 to 9).
		:param true_classes: A 9 element vector with the correct class labels (integers from 1 to 9).
		:return: The logloss (float).
		
		Information: https://www.kaggle.com/c/otto-group-product-classification-challenge/details/evaluation
		Based on: https://www.kaggle.com/wiki/LogarithmicLoss   but actually changed completely
	"""
	assert rows_normalized(predictions), 'The predictions you submitted aren\'t normalized! You can use normalize_probabilities(..).'
	pred = clip(predictions, epsilon, 1 - epsilon)
	predictions_for_true = pred[range(predictions.shape[0]), true_classes - 1]
	ll = - log(predictions_for_true).sum() / len(true_classes)
	return ll


def accuracy():
	"""
		The accuracy of the predictions.
		
		Arguments are the same as those for logloss.
		:return: The accuracy as a fraction [0-1].
	"""
	#todo
	

if __name__ == '__main__':
	S, C = 21, 9
	true_classes = array([((2 * k) % C) + 1 for k in range(S)])
	predictions = normalize_probabilities(uniform(size = (S, C)))
	print 'random: ', logloss(predictions, true_classes)
	predictions = normalize_probabilities(ones((S, C)))
	print 'uniform:', logloss(predictions, true_classes)
	predictions = zeros((S, C))
	predictions[:, 0] = 1
	print 'certain:', logloss(predictions, true_classes)
	predictions = zeros((S, C))
	predictions[range(predictions.shape[0]), true_classes - 1] = 1
	print 'correct:', logloss(predictions, true_classes)


