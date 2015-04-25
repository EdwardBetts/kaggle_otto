
from numpy import bincount, float64
from sklearn.metrics import confusion_matrix as calc_confusion_matrix
from validation.score import prob_to_cls


def confusion_matrix(predictions, classes_true):
	"""
		Generate the confusion matrix.
	"""
	return calc_confusion_matrix(classes_true, prob_to_cls(predictions), labels = range(1, 10))


def average_size_mismatch(predictions, classes_true):
	"""
		Calculate how big each calculated class is as a fraction of the true data size.
	"""
	return bincount(prob_to_cls(predictions))[1:] / float64(bincount(classes_true)[1:])

