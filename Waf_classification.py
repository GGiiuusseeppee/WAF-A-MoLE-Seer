from sklearn.metrics import accuracy_score
from sklearn import svm
from sklearn.linear_model import RidgeClassifier, LogisticRegression
from sklearn import svm
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.utils import shuffle
from sklearn.metrics import roc_curve, roc_auc_score, RocCurveDisplay, auc
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
import joblib
import seaborn as sns
from sklearn.metrics import confusion_matrix

class SeerBox:
    def __init__(self, X, y, model=None):
        self.X = X
        self.y = y
        self.model = model

        self._xtr = None
        self._ytr = None
        self._xts = None
        self._yts = None

    def shuffle_split(self):

        self.X, self.y = shuffle(self.X, self.y)
        self._xtr, self._xts, self._ytr, self._yts = train_test_split(
            self.X, self.y, test_size=0.40)

    def compute_sum_of_regex_triggers(self):

        return self._xts.sum(axis=1)

    def fit_model(self):

      if self.model:
            self._xtr, self._xts, self._ytr, self._yts = train_test_split(self.X, self.y, test_size=0.40)
            self.model.fit(self._xtr, self._ytr)

      else:
        pass


    def predict_and_evaluate(self):

        if self.model:        
            y_pred = self.model.predict(self._xts)
            print('true lavbel',self._yts[:33])
            print('preedict label',y_pred[:33])
            print(f"Accuracy: {accuracy_score(self._yts, y_pred):.3f}")
            y_pred_proba = self.model.decision_function(self._xts)

            print(f"AUC: {roc_auc_score(self._yts, y_pred_proba):.3f}")
            cm = confusion_matrix(self._yts, y_pred)
            plt.figure(figsize=(6, 4))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Greens', cbar=False)
            plt.xlabel('Predicted Label')
            plt.ylabel('True Label')
            plt.title("Confusion Matrix")
            plt.show()

        else:
            y_scores = self.compute_sum_of_regex_triggers()
            print(f"AUC: {roc_auc_score(self._yts, y_scores):.3f}")


    def plot_roc_curve(self):

      if self.model:
        y_scores = self.model.decision_function(self._xts)
        
        fpr, tpr, thr = roc_curve(self._yts, y_scores)
        
        auc = roc_auc_score(self._yts, y_scores)
        plt.plot(fpr, tpr, marker='.', label='SVM (AUC = %0.3f)' %auc)
        plt.title("ROC con sum Curve")
        plt.xlabel("False positive rate")
        plt.ylabel("True positive rate")
        plt.legend()
        plt.plot([0, 1], [0, 1], 'k--', label='Chance')
        plt.show()
       

      else:

        y_scores = self.compute_sum_of_regex_triggers()
        fpr, tpr, thr = roc_curve(self._yts, y_scores)
        auc = roc_auc_score(self._yts, y_scores)
        plt.plot(fpr, tpr, marker='.', label='SVM (AUC = %0.3f)' %auc)
        plt.title("ROC con sum Curve")
        plt.xlabel("False positive rate")
        plt.ylabel("True positive rate")
        plt.legend()

        plt.show()


    def run(self):

        self.shuffle_split()

        if self.model:

            self.fit_model()
        else:
            self.compute_sum_of_regex_triggers()
        
        self.predict_and_evaluate()

        self.plot_roc_curve()


