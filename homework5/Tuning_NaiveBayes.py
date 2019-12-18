# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import csv
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import BernoulliNB
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

# Load data
def load_csv_data(filename):
    file = pd.read_csv(filename)

    data = file[['Elevation', 'Aspect', 'Slope', 'Horizontal_Distance_To_Hydrology', 'Vertical_Distance_To_Hydrology',
                 'Horizontal_Distance_To_Roadways', 'Hillshade_9am', 'Hillshade_Noon', 'Hillshade_3pm', 'Horizontal_Distance_To_Fire_Points',
                 'Wilderness_Area1', 'Wilderness_Area2', 'Wilderness_Area3', 'Wilderness_Area4', 'Soil_Type1',
                 'Soil_Type2', 'Soil_Type3', 'Soil_Type4', 'Soil_Type5', 'Soil_Type6',
                 'Soil_Type7', 'Soil_Type8', 'Soil_Type9', 'Soil_Type10', 'Soil_Type11',
                 'Soil_Type12', 'Soil_Type13', 'Soil_Type14', 'Soil_Type15', 'Soil_Type16',
                 'Soil_Type17', 'Soil_Type18', 'Soil_Type19', 'Soil_Type20', 'Soil_Type21',
                 'Soil_Type22', 'Soil_Type23', 'Soil_Type24', 'Soil_Type25', 'Soil_Type26',
                 'Soil_Type27', 'Soil_Type28', 'Soil_Type29', 'Soil_Type30', 'Soil_Type31',
                 'Soil_Type32', 'Soil_Type33', 'Soil_Type34', 'Soil_Type35', 'Soil_Type36',
                 'Soil_Type37', 'Soil_Type38', 'Soil_Type39', 'Soil_Type40']]
    labels = file['Cover_Type']
    data = np.array(data)
    labels = np.array(labels)
    return data, labels

# Load data
def load_csv_test(filename):
    file = pd.read_csv(filename)

    data = file[['Elevation', 'Aspect', 'Slope', 'Horizontal_Distance_To_Hydrology', 'Vertical_Distance_To_Hydrology',
                 'Horizontal_Distance_To_Roadways', 'Hillshade_9am', 'Hillshade_Noon', 'Hillshade_3pm', 'Horizontal_Distance_To_Fire_Points',
                 'Wilderness_Area1', 'Wilderness_Area2', 'Wilderness_Area3', 'Wilderness_Area4', 'Soil_Type1',
                 'Soil_Type2', 'Soil_Type3', 'Soil_Type4', 'Soil_Type5', 'Soil_Type6',
                 'Soil_Type7', 'Soil_Type8', 'Soil_Type9', 'Soil_Type10', 'Soil_Type11',
                 'Soil_Type12', 'Soil_Type13', 'Soil_Type14', 'Soil_Type15', 'Soil_Type16',
                 'Soil_Type17', 'Soil_Type18', 'Soil_Type19', 'Soil_Type20', 'Soil_Type21',
                 'Soil_Type22', 'Soil_Type23', 'Soil_Type24', 'Soil_Type25', 'Soil_Type26',
                 'Soil_Type27', 'Soil_Type28', 'Soil_Type29', 'Soil_Type30', 'Soil_Type31',
                 'Soil_Type32', 'Soil_Type33', 'Soil_Type34', 'Soil_Type35', 'Soil_Type36',
                 'Soil_Type37', 'Soil_Type38', 'Soil_Type39', 'Soil_Type40']]
    data = np.array(data)
    return data

# Load labels
def load_csv_labels(filename):
    file = pd.read_csv(filename)
    test_labels = file['Cover_Type']
    test_labels = np.array(test_labels)
    return test_labels

# NaiveBayes
def testNaiveBayes(features, labels, features_test, alpha):

    NB = BernoulliNB(alpha=alpha)

    # preprocessing the data
    scaler = StandardScaler().fit(features)
    features = scaler.transform(features)
    features_test = scaler.transform(features_test)

    # train
    NB.fit(features, labels)
    k = 5
    c = cross_val_score(NB, features, labels, cv = k)
    c = np.mean(c)
    print('Traing accuracy of', k, '-', 'fold validation is: %.03f' % c)
    with open("NB_tuning_process.csv", "a") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([alpha,c])
        print([alpha,c])

    # predict
    predict = NB.predict(features_test)

    # write csv
    with open("predict_NB.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ["Id", "Cover_Type"])
        for i in range(0, len(predict)):
            writer.writerow([(15121 + i), predict[i]])

if __name__ == '__main__':
    print('NaiveBayes:')
    with open("NB_tuning_process.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['alpha', 'accuracy'])
    features, labels = load_csv_data('train.csv')
    features_test = load_csv_test('test.csv')

    from numpy import arange
    for alpha in arange (0,1,0.1):
        testNaiveBayes(features, labels, features_test, alpha)
        '''
        features_test_labels = load_csv_labels('predict_labels.csv')
        features_test_predict = load_csv_labels('predict_NB.csv')
        testing_accuracy = accuracy_score(features_test_labels, features_test_predict)

        print('Testing accuracy is: %.03f' % testing_accuracy)
        '''
