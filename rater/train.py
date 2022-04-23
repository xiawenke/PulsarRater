from skimage import io, color
from sklearn import svm, metrics
from sklearn.model_selection import train_test_split
from skimage.transform import resize
import joblib
from .load import load
from .config import config

class train():
    def __init__(self, dataset):
        print('Loading dataset...')
        self.load = load(dataset)
        self.config = config()
        self.x, self.y = self.load.load()

    def train(self):
        print('Training...')
        
        # Split data into training and test set
        x_train, x_test, y_train, y_test = train_test_split(self.x, self.y, test_size=0.2)

        # Train SVM
        clf = svm.SVC(gamma='scale')
        clf.fit(x_train, y_train)

        # Predict
        y_pred = clf.predict(x_test)

        # Print accuracy
        print('Accuracy:', metrics.accuracy_score(y_test, y_pred))

        # Save model
        joblib.dump(clf, self.config.model)

        return clf