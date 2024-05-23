import streamlit as st
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from io import StringIO


from sklearn.metrics import classification_report,accuracy_score

from sklearn.feature_selection import chi2



df = pd.read_csv("7allV03.csv")  # verisetimizi okuyoruz

print(df.head(10))   # ilk 10 örnek,boyut ve uniqur sütun isimleri
print(df.shape)
print(df["category"].unique())



col = ['category', 'text']  # bizi ilgilendiren sütunlar
df = df[col]
df = df[pd.notnull(df['text'])]   # texti null olan gözlemler
df.columns = ['category', 'text']  # sütun adlarını değiştirme
df['category_id'] = df['category'].factorize()[0]  # her kategori için unique sayısal etiketler 0 1 2 3...
category_id_df = df[['category', 'category_id']].drop_duplicates().sort_values('category_id') # duplicate değerleri drop ediyoruz
category_to_id = dict(category_id_df.values) # category ve category_id içeren sözlükler oluşturduk
id_to_category = dict(category_id_df[['category_id', 'category']].values)
print(df.sample(5))


sw = pd.read_csv("turkce-stop-words.txt", header=None) # türkçe için stop wordsler
print(sw[0].values.tolist())








tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='utf-8', ngram_range=(1, 2), stop_words=sw[0].values.tolist())
# TF-IDF vektörleşmesi
features = tfidf.fit_transform(df.text).toarray()   # text verileri vektörlere dönüştürüyoruz
labels = df.category_id
print(features.shape) # vektörleşme sonrası oluşan sütun sayımız


# özellik seçimi için ki-kare testi
N = 2
for category, category_id in sorted(category_to_id.items()):
      features_chi2 = chi2(features, labels == category_id)
      indices = np.argsort(features_chi2[0])
      feature_names = np.array(tfidf.get_feature_names_out())[indices]
      unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
      bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
      print("# '{}':".format(category))
      print("  . En ilişkili unigram ifadeler:\n. {}".format('\n. '.join(unigrams[-N:])))
      print("  . En ilişkili bigram ifadeler:\n. {}".format('\n. '.join(bigrams[-N:])))
      print("---------------------------")



X_train, X_test, y_train, y_test = train_test_split(df['text'], df['category'], random_state = 0) # veriyi eğitim ve test olarak ayırdık

 #CountVectorizer ve TF-IDF Transformer kullanarak veriyi vektörlere dönüştürme
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)



best_model_name = None
best_accuracy = 0


# deniyeceğimiz farklı sınıflandırma modelleri
models = [
    ('MultinomialNB', MultinomialNB()),
    ('LogisticRegression', LogisticRegression()),
    ('RandomForestClassifier', RandomForestClassifier())
]


for model_name, model in models:
    pipeline = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', model)
    ])
    
   
    pipeline.fit(X_train, y_train)   # eğitiyoruz
    y_pred = pipeline.predict(X_test)  # tahmin işlemimiz
    
    # skorlarımız
    accuracy = accuracy_score(y_test, y_pred)
    class_report = classification_report(y_test, y_pred)
    
    print(f"Model: {model_name}")
    print(f"Accuracy: {accuracy}")
    print("Classification Report:")
    print(class_report)
    print("-------------------------------------")

    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_model_name = model_name

# En iyi model ve skoru yazdırma
print(f"En iyi model: {best_model_name}")
print(f"En iyi modelin accuracy skoru: {best_accuracy}")
    







Lr = LogisticRegression().fit(X_train_tfidf, y_train) # en iyi modelimiz




# oluşturduğumuz modeli ve vektörleştirmeleri kaydediyoruz
joblib.dump(Lr,"modellim.pkl")
joblib.dump(tfidf_transformer, 'tfidf_transformer.pkl')
joblib.dump(count_vect, 'count_vectorizer.pkl')



y_pred = Lr.predict(count_vect.transform(X_test))
class_report = classification_report(y_test, y_pred)
print("Classification Report:\n", class_report)


