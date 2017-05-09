import numpy as np
from random import randint

class RTLearner(object):

    def __init__(self, leaf_size, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.tree = np.array([])

    def split_feature(self, x_train):
        feature_idx = randint(0, x_train.shape[0])
        split_idx1 = randint(0, feature_idx - 1)
        split_idx2 = randint(0, feature_idx - 1)

        split_val = (x_train[split_idx1][feature_idx] + \
                     x_train[split_idx2][feature_idx]) / 2
        left_idxs = [i for i in xrange(feature_idx)
                    if x_train[i][feature_idx] <= split_val]
        right_idxs = [i for i in xrange(feature_idx)
                     if x_train[i][feature_idx] > split_val]
        return left_idxs, right_idxs, feature_idx, split_val

    def build_tree(self, x_train, y_train):
        # If only one feature, take the mean of the labels
        num_feature = x_train.shape[0]
        if num_feature == 0:
            print 'all -1s'
            return np.array([-1, -1, -1, -1])
        if num_feature <= self.leaf_size:
            return np.array([-1, np.mean(y_train), -1, -1])

        # If all instances have the same label, return the label
        values = np.unique(y_train)
        if len(values) == 1:
            return np.array([-1,y_train[0], -1, -1])

        while True:
            left_idxs, right_idxs, feature_idx, split_val = self.split_feature(x_train)
            if len(left_idxs) >= 1 and len(right_idxs) >= 1:
                break

        left_x_train = np.array([x_train[i] for i in left_idxs])
        left_y_train = np.array([y_train[i] for i in left_idxs])
        right_x_train = np.array([x_train[i] for i in right_idxs])
        right_y_train = np.array([y_train[i] for i in right_idxs])

        left_tree = self.build_tree(left_x_train, left_y_train)
        right_tree = self.build_tree(right_x_train, right_y_train)
        if len(left_tree.shape) == 1:
            num_left_feature = 2
        else:
            num_left_feature = left_tree.shape[0] + 1

        root = [feature_idx, split_val, 1, num_left_feature]
        return np.vstack((root, np.vstack((left_tree, right_tree))))

    def addEvidence(self, Xtrain, Ytrain):
        self.tree = self.build_tree(Xtrain, Ytrain)

    def traverse_tree(self, instance, row=0):
        feature_idx = int(self.tree[row][0])
        if feature_idx == -1:
            return self.tree[row][1]
        if instance[feature_idx] <= self.tree[row][1]:
            return self.traverse_tree(instance, row + int(self.tree[row][2]))
        else:
            return self.traverse_tree(instance, row + int(self.tree[row][3]))

    def query(self, Xtest):
        result = []
        for instance in Xtest:
            result.append(self.traverse_tree(instance))
        return np.array(result)
