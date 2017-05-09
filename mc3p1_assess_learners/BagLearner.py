import numpy as np
import RTLearner
from random import randint

class BagLearner(object):
    N_PRIME_PERCENT = 0.6
    def __init__(self, learner=RTLearner,
                 kwargs={"leaf_size": 1},
                 bags=20,
                 boost=False,
                 verbose=False):
        self.learners = []
        for i in xrange(bags):
            self.learners.append(learner(**kwargs))

    @staticmethod
    def get_random_indices(n, n_prime_percent):
        indices = []
        for i in xrange(int(n_prime_percent * n)):
            indices.append(randint(0, n - 1))
        return indices

    def addEvidence(self, Xtrain, Ytrain):
        for learner in self.learners:
            idxs = BagLearner.get_random_indices(Xtrain.shape[0], self.N_PRIME_PERCENT)
            current_x_train = []
            current_y_train = []
            for idx in idxs:
                current_x_train.append(Xtrain[idx])
                current_y_train.append(Ytrain[idx])
            learner.addEvidence(np.array(current_x_train), np.array(current_y_train))

    def query(self, Xtest):
        results = None
        for learner in self.learners:
            current_result = learner.query(Xtest)
            if results is None:
                results = current_result
            else:
                results = np.add(results, current_result)
        return result / len(self.learners)