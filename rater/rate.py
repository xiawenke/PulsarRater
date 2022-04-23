from skimage import io, color
from sklearn import svm, metrics
from sklearn.model_selection import train_test_split
from skimage.transform import resize
import joblib
from .config import config
from .load import load
from .train import train

class rate(load, train):
    def __init__(self):
        self.config = config()
        self.clf = joblib.load(self.config.model)

    def rate(self, img_path):
        img = self.img_to_matrix(img_path)

        return self.clf.predict([img])[0]
