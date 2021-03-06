
from nnet.oldstyle.base_optimize import optimize_NN


optimize_NN(debug = False, **{
	'dense1_size': 128,
	'dense2_size': None,
	'dense3_size': None,
	'learning_rate': 0.01,
	'dropout1_rate': 0,
	'max_epochs': 3,
	'extra_feature_count': 20,
	'pretrain': None,
})


