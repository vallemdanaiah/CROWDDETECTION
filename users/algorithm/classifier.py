from users.algorithm import DataPrep
from users.algorithm import  FeatureSelection
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
# from sklearn.cross_validation import KFold
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.model_selection import KFold
from warnings import simplefilter

# string to test
doc_new = ['obama is running for president in 2016']

# the feature selection has been done in FeatureSelection.py module. here we will create models using those features for prediction

# first we will use bag of words techniques

# building classifier using naive bayes
nb_pipeline = Pipeline([
    ('NBCV', FeatureSelection.countV),
    ('nb_clf', MultinomialNB())])

nb_pipeline.fit(DataPrep.train_news['Statement'], DataPrep.train_news['Label'])
predicted_nb = nb_pipeline.predict(DataPrep.test_news['Statement'])
np.mean(predicted_nb == DataPrep.test_news['Label'])

# building classifier using logistic regression
logR_pipeline = Pipeline([('LogRCV', FeatureSelection.countV), ('LogR_clf', LogisticRegression())])

logR_pipeline.fit(DataPrep.train_news['Statement'], DataPrep.train_news['Label'])
predicted_LogR = logR_pipeline.predict(DataPrep.test_news['Statement'])
np.mean(predicted_LogR == DataPrep.test_news['Label'])

# building Linear SVM classfier
svm_pipeline = Pipeline([('svmCV', FeatureSelection.countV), ('svm_clf', svm.LinearSVC())])

svm_pipeline.fit(DataPrep.train_news['Statement'], DataPrep.train_news['Label'])
predicted_svm = svm_pipeline.predict(DataPrep.test_news['Statement'])
np.mean(predicted_svm == DataPrep.test_news['Label'])

# using SVM Stochastic Gradient Descent on hinge loss
sgd_pipeline = Pipeline([('svm2CV', FeatureSelection.countV), ('svm2_clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, max_iter=5))])

sgd_pipeline.fit(DataPrep.train_news['Statement'], DataPrep.train_news['Label'])
predicted_sgd = sgd_pipeline.predict(DataPrep.test_news['Statement'])
np.mean(predicted_sgd == DataPrep.test_news['Label'])

# random forest
random_forest = Pipeline([('rfCV', FeatureSelection.countV), ('rf_clf', RandomForestClassifier(n_estimators=200, n_jobs=3))])

random_forest.fit(DataPrep.train_news['Statement'], DataPrep.train_news['Label'])
predicted_rf = random_forest.predict(DataPrep.test_news['Statement'])
np.mean(predicted_rf == DataPrep.test_news['Label'])


# User defined functon for K-Fold cross validatoin
def build_confusion_matrix(classifier):
    # print('Total statements classified:', len(DataPrep.train_news))
    simplefilter(action='ignore', category=FutureWarning)
    k_fold = KFold(len(DataPrep.train_news), False)
    scores = []
    confusion = np.array([[0, 0], [0, 0]])

    for train_ind, test_ind in k_fold.split(DataPrep.train_news['Statement']):
        train_text = DataPrep.train_news.iloc[train_ind]['Statement']
        train_y = DataPrep.train_news.iloc[train_ind]['Label']

        test_text = DataPrep.train_news.iloc[test_ind]['Statement']
        test_y = DataPrep.train_news.iloc[test_ind]['Label']

        classifier.fit(train_text, train_y)
        predictions = classifier.predict(test_text)

        confusion += confusion_matrix(test_y, predictions)
        score = f1_score(test_y, predictions)
        scores.append(score)

    return (sum(scores) / len(scores)
            )






nb_pipeline_ngram = Pipeline([('nb_tfidf', FeatureSelection.tfidf_ngram), ('nb_clf', MultinomialNB())])
nb_pipeline_ngram.fit(DataPrep.train_news['Statement'], DataPrep.train_news['Label'])
predicted_nb_ngram = nb_pipeline_ngram.predict(DataPrep.test_news['Statement'])
np.mean(predicted_nb_ngram == DataPrep.test_news['Label'])

# logistic regression classifier
logR_pipeline_ngram = Pipeline([('LogR_tfidf', FeatureSelection.tfidf_ngram), ('LogR_clf', LogisticRegression(penalty="l2", C=1))])

logR_pipeline_ngram.fit(DataPrep.train_news['Statement'], DataPrep.train_news['Label'])
predicted_LogR_ngram = logR_pipeline_ngram.predict(DataPrep.test_news['Statement'])
np.mean(predicted_LogR_ngram == DataPrep.test_news['Label'])

# linear SVM classifier
svm_pipeline_ngram = Pipeline([('svm_tfidf', FeatureSelection.tfidf_ngram), ('svm_clf', svm.LinearSVC())])

svm_pipeline_ngram.fit(DataPrep.train_news['Statement'], DataPrep.train_news['Label'])
predicted_svm_ngram = svm_pipeline_ngram.predict(DataPrep.test_news['Statement'])
np.mean(predicted_svm_ngram == DataPrep.test_news['Label'])

# sgd classifier
sgd_pipeline_ngram = Pipeline([('sgd_tfidf', FeatureSelection.tfidf_ngram), ('sgd_clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, max_iter=5))])

sgd_pipeline_ngram.fit(DataPrep.train_news['Statement'], DataPrep.train_news['Label'])
predicted_sgd_ngram = sgd_pipeline_ngram.predict(DataPrep.test_news['Statement'])
np.mean(predicted_sgd_ngram == DataPrep.test_news['Label'])

# random forest classifier
random_forest_ngram = Pipeline([('rf_tfidf', FeatureSelection.tfidf_ngram), ('rf_clf', RandomForestClassifier(n_estimators=300, n_jobs=3))])

random_forest_ngram.fit(DataPrep.train_news['Statement'], DataPrep.train_news['Label'])
predicted_rf_ngram = random_forest_ngram.predict(DataPrep.test_news['Statement'])
np.mean(predicted_rf_ngram == DataPrep.test_news['Label'])





def runAlgorithm():
    naivClas = build_confusion_matrix(nb_pipeline)
    logRClas = build_confusion_matrix(logR_pipeline)
    svmClas = build_confusion_matrix(svm_pipeline)
    sgdClass = build_confusion_matrix(sgd_pipeline)
    rfClas = build_confusion_matrix(random_forest)

    # K-fold cross validation for all classifiers
    naiveBin = build_confusion_matrix(nb_pipeline_ngram)
    logiregreBin = build_confusion_matrix(logR_pipeline_ngram)
    svmBin = build_confusion_matrix(svm_pipeline_ngram)
    sgdBin = build_confusion_matrix(sgd_pipeline_ngram)
    rfBin = build_confusion_matrix(random_forest_ngram)
    dict = {
        'NiaveClassification': round(naivClas, 2),
        'LogicRegressionClassification': round(logRClas, 2),
        'SVMClassification': round(svmClas, 2),
        'SGDClassification': round(sgdClass, 2),
        'rfClassification': round(rfClas, 2),
        'naiveBinary': round(naiveBin, 2),
        'LogicRegreBina': round(logiregreBin, 2),
        'SVMBinary': round(svmBin, 2),
        'SGDBinary': round(sgdBin, 2),
        'randomeBinary': round(rfBin, 2)
    }
    return dict;


#print(dict)
