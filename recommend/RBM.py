#!/usr/bin/env python3

import numpy as np
import pickle


def logistic(x):
    return 0.5 * (1 + np.tanh(0.5 * x))


class RBM(object):
    def __init__(self, n_visible, n_hidden, k = 1, learn_rate = 0.1, learn_batch = 100, max_step = 2000, eps = 1e-4):
        self.n_visible = n_visible
        self.n_hidden = n_visible
        self.k = k
        self.learn_rate = learn_rate
        self.learn_batch = learn_batch
        self.max_step = max_step
        self.eps = eps
        
        self.w = np.random.randn(n_hidden, n_visible)
        self.bv = np.random.randn(n_visible)
        self.bh = np.random.randn(n_hidden)
        
    def fit(self, train_data):
        tot_num = train_data.shape[0]
        for step in range(self.max_step):
            error = 0.0
            for i in range(0, tot_num, self.learn_batch):
                cur_num = min(self.learn_batch, tot_num - i)
                v0 = train_data[i : i + cur_num, : ]
                h0 = logistic(np.dot(v0, self.w.T) + self.bh)
                
                hk = h0
                for j in range(self.k):
                    vk = logistic(np.dot(hk, self.w) + self.bv)
                    hk = logistic(np.dot(vk, self.w.T) + self.bh)
                
                self.w += self.learn_rate * (np.dot(h0.T, v0) - np.dot(hk.T, vk)) / cur_num
                self.bh += self.learn_rate * np.mean(h0 - hk, axis = 0)
                self.bv += self.learn_rate * np.mean(v0 - vk, axis = 0)
                
                error += np.sum((v0 - vk) ** 2)
            
            if error < self.eps:
                break
            
            print("iteration = %d, error = %f" % (step, error))
    
    def predict(self, data):
        v0 = data
        h0 = logistic(np.dot(v0, self.w.T) + self.bh)
        
        v1 = logistic(np.dot(h0, self.w) + self.bv)
        return v1
        
    def save(self, file_name):
        np.savez(file_name, w = self.w, bh = self.bh, bv = self.bv)
    
    def load(self, file_name):
        raw_data = np.load(file_name + '.npz')
        self.w = raw_data['w']
        self.bh = raw_data['bh']
        self.bv = raw_data['bv']

if __name__ == '__main__':
    rbm = RBM(n_visible = 6, n_hidden = 2, k = 1)
    # '''
    rating_data = np.array([[1, 1, 1, 0, 0, 0], [1, 0, 1, 0, 0, 0], [1, 1, 1, 0, 0, 0], 
                            [0, 0, 1, 1, 1, 0], [0, 0, 1, 1, 0, 0], [0, 0, 1, 1, 1, 0]])
    rbm.fit(rating_data)
    rbm.save('data')
    # '''
    
    '''
    rbm.load('data')
    rating = np.array([[0, 0, 0, 1, 1, 0]])
    print('推荐得分:', rbm.predict(rating))
    '''
