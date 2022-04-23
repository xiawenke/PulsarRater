import os
import random
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage import io, color
from sklearn import svm, metrics
from sklearn.model_selection import train_test_split
from skimage.transform import resize

class load():
    def __init__(self, path = ""):
        self.path = path

        if(self.path.endswith('/') != True):
            self.path = self.path + '/'
    
    def load(self):
        # Load images from folder 0
        x0, _ = self.load_images(self.path + '0/')
        y0 = np.ones(len(x0)) * 0

        # Load images from folder 1
        x1, _ = self.load_images(self.path + '1/')
        y1 = np.ones(len(x1)) * 1

        # Concatenate all images
        x = np.concatenate((x0, x1))
        y = np.concatenate((y0, y1))
        
        # Shuffle data
        # x, y = self.shuffle(x, y)

        return x, y

    def repeat(self, num, val):
        '''
        Repeats the data num times
        '''
        ret = []
        for _ in range(num):
            ret.append([val])
        
        return ret

    def shuffle(self, x, y):
        '''
        Shuffles the data
        '''
        xy = list(zip(x, y))
        random.shuffle(xy)
        x, y = zip(*xy)
        return x, y
        
    def load_images(self, folder):
        '''
        Loads all images from a folder and returns a list of matrices
        '''
        # Get files from folder
        files = os.listdir(folder)
        # Load images
        img_list = []
        filenames = []
        for file in files:
            if(file.endswith('.png') or file.endswith('.jpg')):
                img_list.append(
                    self.img_to_matrix(folder + file)
                )
                filenames.append(file)

        return img_list, filenames

    def img_to_matrix(self, img_path):
        '''
        Loads an image and converts it to a matrix
        '''
        img = resize(io.imread(img_path), (256, 256))
        img = color.rgb2gray(img)
        img = img[20:256, :]
        reshaped =  self.flatten(img)

        '''
        print(img[:, 170])
        plt.matshow(img)
        flattened = self.flatten(img)
        plt.scatter(range(len(flattened)), flattened)
        raise NotImplementedError
        plt.scatter(range(len(reshaped)), reshaped)
        plt.show()
        print(img_path)
        print(reshaped)
        raise NotImplementedError
        '''
        return reshaped
    
    def flatten(self, x):
        '''
        Flattens the data
        '''
        flattened = np.ones(x.shape[1]) * 256
        for r in range(x.shape[1]):
            thisColumn = x[:, r]
            for i in range(len(thisColumn)):
                if(thisColumn[i] < 1):
                    flattened[r] = i
                    break
        
        return flattened
