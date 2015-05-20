
from nnet.base_optimize import optimize_NN


optimize_NN(debug = False, **{
	'dense1_nonlinearity': 'rectify',   # tanh, sigmoid, rectify, leaky2, leaky20, softmax
	'dense1_init': 'glorot_normal',     # orthogonal, sparse, glorot_normal, glorot_uniform, he_normal, he_uniform
	'dense1_size': 256,                 # hidden neurons in layer (30~1000)
	'dense2_size': 0,
	'dense3_size': None,
	'learning_rate': 0.001,             # initial learning rate (learning rate is effectively higher for higher momentum)
	'learning_rate_scaling': 100,       # progression over time; 0.1 scaled by 10 is 0.01
	'momentum': 0.9,                    # initial momentum
	'momentum_scaling': 10,             # 0.9 scaled by 10 is 0.99
	'dropout1_rate': 0.5,               # [0, 0.5]
	'dropout2_rate': None,              # inherit dropout1_rate if dense2 exists
	'dropout3_rate': None,              # inherit dropout2_rate if dense3 exist
	'weight_decay': 0.00006,            # constrain the weights to avoid overfitting
	'max_epochs': 500,                  # it terminates when overfitting or increasing, so just leave high
	'auto_stopping': False,             # stop training automatically if it seems to be failing
	'extra_feature_count': 0,
	'pretrain': 'results/pretrain/single_pretrain_256_0_0.net.npz',
	'save_snapshots_stepsize': 500,
	'rounds': 3,
})

