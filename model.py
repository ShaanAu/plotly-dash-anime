# import packages and libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
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

path = '/Users/shaanaucharagram/Documents/repos'
anime_df = pd.read_csv(path + "/big_data/anime.csv")
rating_df = pd.read_csv(path + "/big_data/rating.csv")
df = pd.get_dummies(anime_df)
df_anime_new = pd.merge(anime_df, df)
df_anime_new_corr = df_anime_new.corr()

rating_df['did_rate'] = np.where(rating_df['rating']!=-1, 1, 0)
test_df = anime_df.merge(rating_df, on='anime_id', how='left')
test_df['count'] = test_df['anime_id'].map(test_df['anime_id'].value_counts())

genres = pd.DataFrame(anime_df.genre.str.split(',', expand=True).stack(), columns=['genre'])
genres = genres.reset_index(drop=True)
genre_count = pd.DataFrame(genres.groupby(by=['genre']).size(), columns=['count'])
genre_count = genre_count.reset_index()

top_20 = genre_count.nlargest(20, 'count')
top_10 = genre_count.nlargest(10, 'count')
top_5 = genre_count.nlargest(5, 'count')

df_anime_new['episodes'] = df_anime_new.episodes.fillna(0)
df_anime_new.episodes.replace(('Unknown'), (0), inplace=True)
df_anime_new['episodes'] = df_anime_new.episodes.astype(int)
df_anime_new['episodes']=df_anime_new['episodes'].replace(0,df_anime_new['episodes'].mean())

df_anime_new = df_anime_new[df['rating'].notna()]

feature_list = list(df_anime_new.columns)
feature_list = ['episodes', 'members']




X = df_anime_new[['episodes', 'members']]
y = df_anime_new.rating

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)

print('Training Features Shape:', X_train.shape)
print('Training Labels Shape:', y_train.shape)
print('Testing Features Shape:', X_test.shape)
print('Testing Labels Shape:', y_test.shape)

# Import the model we are using
from sklearn.ensemble import RandomForestRegressor
# Instantiate model with 1000 decision trees
rf = RandomForestRegressor(n_estimators = 1000, random_state = 42)
# Train the model on training data
rf.fit(X_train, y_train)


# Use the forest's predict method on the test data
predictions = rf.predict(X_test)
# Calculate the absolute errors
errors = abs(predictions - y_test)
# Print out the mean absolute error (mae)
print('Mean Absolute Error:', round(np.mean(errors), 2), 'degrees.')

# Calculate mean absolute percentage error (MAPE)
mape = 100 * (errors / y_test)
# Calculate and display accuracy
accuracy = 100 - np.mean(mape)
print('Accuracy:', round(accuracy, 2), '%.')


# Get numerical feature importances
importances = list(rf.feature_importances_)
# List of tuples with variable and importance
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
# Sort the feature importances by most important first
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
# Print out the feature and importances
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances];


