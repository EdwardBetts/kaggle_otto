
from numpy import zeros, array
from random import shuffle as pyshuffle


def shuffle(data, classes = None, seed = 4242):
    """
        Shuffle the rows of data. For training data, which is ordered. Key can be used to unshuffle it before cross-validation or submission.
        
        :param data: A data ndarray.
        :param classes: Optionally, the true classes.
        :param seed: The seed for shuffling (best leave unchanged to compare results).
        :return: shuffled_data, unshuffle_key
    """
    key = array(range(data.shape[0]))
    pyshuffle(key, random = lambda: (seed / 10000.) % 10000)
    data = data[key, :]
    if classes is not None:
		classes = classes[key]
    return data, key


def get_inverse_key(key):
    """ Not intended for direct use. """
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
		classes = classes[invkey]
    return data


if __name__ == '__main__':
    """
        Test / demonstration of sorting and unsorting.
    """
    data = zeros((8, 3))
    for k in range(8):
        data[k, :] = k
    sdata, key = shuffle(data)
    print 'shuffled'
    print sdata
    udata = unshuffle(sdata, key = key)
    print 'unshuffled'
    print udata
    print 'shuffle key:  ', key
    print 'unshuffle key:', get_inverse_key(key)


