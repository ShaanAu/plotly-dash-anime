import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
#matplotlib.use('TkAgg')
plt.interactive(False)
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
# Import the model we are using
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.cluster import KMeans

class MakeModel:

    def __init__(self, X, y, data):
        self.X = X
        self.y = y
        self.data = data

    def logisticRegression(self, scale=True, confusion_Matrix=False, Metrics=False, roc_Curve=False):
        """
        Creates a logistic regression model
        """
        X= self.X
        y = self.y
        X_convert = X
        y_convert = y
        X_train, X_test, y_train, y_test = train_test_split(X_convert, y_convert, stratify=y_convert, test_size=0.3, random_state=42)
        # fit the model with data
        if scale is True:
            sc = StandardScaler()
            X_train = sc.fit_transform(X_train)
            X_test = sc.transform(X_test)

        lr = LogisticRegression()
        lr.fit(X_train, y_train)
        y_pred = lr.predict(X_test)
        #print(y_pred)

        if confusion_Matrix is True:

            cnf_matrix = metrics.confusion_matrix(y_test, y_pred)

            class_names = [0, 1]  # name  of classes
            fig, ax = plt.subplots()
            tick_marks = np.arange(len(class_names))
            plt.xticks(tick_marks, class_names)
            plt.yticks(tick_marks, class_names)

            # create heatmap
            h_map = sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu", fmt='g')
            ax.xaxis.set_label_position("top")
            plt.tight_layout()
            plt.title('Confusion matrix', y=1.1)
            plt.ylabel('Actual label')
            plt.xlabel('Predicted label')
            plt.show()

        if Metrics is True:
            print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
            print("Precision:", metrics.precision_score(y_test, y_pred))
            print("Recall:", metrics.recall_score(y_test, y_pred))

        if roc_Curve is True:
            y_pred_proba = lr.predict_proba(X_test)[::, 1]
            fpr, tpr, _ = metrics.roc_curve(y_test, y_pred_proba)
            auc = metrics.roc_auc_score(y_test, y_pred_proba)
            plt.plot(fpr, tpr, label="data 1, auc=" + str(auc))
            plt.legend(loc=4)
            plt.show()


path = '/Users/shaanaucharagram/Documents/repos'
anime_df = pd.read_csv(path + "/big_data/anime.csv")
df = pd.get_dummies(anime_df, columns=['type'])
df_anime_new

anime_df.type.value_counts()

import seaborn as sns

sns.heatmap(df_anime_new.corr())


X = df_anime_new[['rating', '']]
y = s
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

lr = LogisticRegression()
lr.fit(X_train, y_train)
y_pred = lr.predict(X_test)
