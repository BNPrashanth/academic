import json as j
import pandas as pd
import re
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, chi2
import nltk
import pickle


nltk.download('stopwords')

json_data = None
with open('../../resources/yelp_academic_dataset_review.json') as data_file:
    lines = data_file.readlines()
    joined_lines = "[" + ",".join(lines) + "]"

    json_data = j.loads(joined_lines)

# Creating data frame with the data
data = pd.DataFrame(json_data)
print("Data Frame created..")

stemmer = SnowballStemmer('english')
words = stopwords.words("english")

data['cleaned'] = data['text'].apply(lambda x: " ".join([i for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in words]).lower())

# X_train has text of train data and Y_train has lable of of train data along with post_id
# X_test has text of test data and Y_test has lable of of test data along with post_id
#training and test ration is 8:2
X_train, X_test, y_train, y_test = train_test_split(data['cleaned'], data.stars, shuffle=True, test_size=0.2)

#x_train is text and y_train is label
#ngram_range is(1,4)4 so quadragram
pipeline = Pipeline([('vect', TfidfVectorizer(ngram_range=(1, 4), stop_words="english", sublinear_tf=True)),
                     ('chi',  SelectKBest(chi2, k=400)),
                     ('clf', LinearSVC(C=1.0, penalty='l1', max_iter=3000, dual=False))])
print("Fitting Data.. Training..")
# for i in range(5):
model = pipeline.fit(X_train, y_train)
filename = '../../resources/SVM_model.pkl'
pickle.dump(model, open(filename, 'wb'))
SVM_model = pickle.load(open("SVM_model.pkl", 'rb'))
# print("[", i, "] accuracy score: " + str(model.score(X_test, y_test)))

print("Training Completed..")
vectorizer = SVM_model.named_steps['vect']
chi = SVM_model.named_steps['chi']
clf = SVM_model.named_steps['clf']

feature_names = vectorizer.get_feature_names()
feature_names = [feature_names[i] for i in chi.get_support(indices=True)]
feature_names = np.asarray(feature_names)

target_names = ['0', '1']
print("top 10 keywords per class:")
for i, label in enumerate(target_names):
    try:
        top10 = np.argsort(clf.coef_[i])[-10:]
        print("%s: %s" % (label, " ".join(feature_names[top10])))
    except IndexError:
        print("Error in Printing 10 words")

print("accuracy score: " + str(SVM_model.score(X_test, y_test)))

print(SVM_model.predict(['that was an awesome place. Great food!']))
