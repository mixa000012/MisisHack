import re
import nltk
import pandas as pd
import pickle

from gensim.models import Word2Vec
from nltk.corpus import stopwords

ROOT_PATH = 'ml/'

pca = pickle.load(open(ROOT_PATH + "pca.pkl",'rb'))
kmeans = pickle.load(open(ROOT_PATH + "knn.pkl",'rb'))
model = Word2Vec.load(ROOT_PATH + 'word2vec.model')

class Model:
    def __init__(self, pca, kmeans, model):
        self.pca = pca
        self.kmeans = kmeans
        self.model = model

        self.stop_words = stopwords.words("russian")

    def _text_tokenizer(self, texts: list[str]):
        tokenized_text = []
        for text in texts:

            text = text.lower()
            text = ' '.join(text.split())  # remove multiple whitespaces
            text = re.sub('[()]', ' ', text)
            text = re.sub(',', '', text)
            text = text.replace('.', ' ') # удаляем точки
            text = ' '.join([word for word in text.split() if word not in self.stop_words])
            tokenized_text.append(text.split())
        return tokenized_text

    def _get_features(self, tokenized_texts):
        df_features = pd.DataFrame( index = [i for i in range(len(tokenized_texts))])

        df_features['len_words_stack'] = 0
        df_features['mobyle_score'] = 0
        df_features['backend_score'] = 0
        df_features['frontend_score'] = 0
        df_features['ml_score'] = 0
        df_features['designer_score'] = 0
        df_features['analytic_score'] = 0
        for i in range(len(tokenized_texts)):

            for j in range(len(tokenized_texts[i])):
                df_features.loc[i, 'len_words_stack'] += 1  # переделать эту хуйню
                if tokenized_texts[i][j] not in model.wv.index_to_key: continue
                scores = {model.wv.similarity(tokenized_texts[i][j],'backend'): 'backend_score', # и эту тоже
                        model.wv.similarity(tokenized_texts[i][j],'frontend') : 'frontend_score',
                        model.wv.similarity(tokenized_texts[i][j],'машинное-обучение'): 'ml_score',
                        model.wv.similarity(tokenized_texts[i][j],'мобильные-приложения'): 'mobyle_score',
                        model.wv.similarity(tokenized_texts[i][j],'дизайн'): 'designer_score',
                        model.wv.similarity(tokenized_texts[i][j],'аналитика'): 'analytic_score',
                        }
                df_features.loc[i,scores[max(scores.keys())]] +=1


        specs_scores = ['backend_score',
                        'ml_score','mobyle_score', 'designer_score','analytic_score', 'frontend_score']
        df_features['experience_techs'] = df_features.apply(lambda x: x[specs_scores].sum(), axis = 1)


        ordered_columns = ['backend_score',
                            'ml_score',
                            'mobyle_score',
                            'designer_score',
                            'analytic_score',
                            'frontend_score',
                            'experience_techs']
        df_features = df_features[ordered_columns]

        return df_features

    def _predict(self, df_features):

        return self.kmeans.predict(pca.transform(df_features))

    def _find_final_spec(self,x):
        specs = ['backend', 'frontend', 'designer', 'ml', 'analytic']
        max_value = -1
        best_spec = ''
        for i in specs:
            if x[i] and max_value < x[f'{i}_score']:
                max_value = x[f'{i}_score']
                best_spec = i
        return (best_spec, max_value)

    async def get_predictions(self, df: dict):
        '''
        df: в df должны лежать столбцы text - стэк юзера и spec - выбранные направления
        return: возвращает примерный уровень юзера (3 - самый хуевый, 0 - средне-низкий, 2 - средний, 1 - пиздатый)
        '''
        df = pd.DataFrame(df)
        texts = df['text'].to_list()
        tokenized_texts = self._text_tokenizer(texts)
        X = self._get_features(tokenized_texts)
        rating = self._predict(X)

        track_dict = {
                    'backend': 'Бэкенд',
                    'frontend': 'Фронтенд',
                    'designer': 'Дизайнер',
                    'ml': 'ML/DS/AI',
                    'analytic': 'Аналитик(презентации и прочее)'
                    }
        df.spec = df.spec.apply(lambda x: [i.lstrip().rstrip() for i in x.split(',')])
        for i in track_dict:
            df[i] = df.spec.apply(lambda x: track_dict[i] in x)
        df = pd.merge(df,X,how = 'left', left_index=True, right_index=True)

        specs = df.apply(lambda x: self._find_final_spec(x), axis = 1).to_list()

        return list(self._predict(X)), specs

dct = {'spec': ['Бэкенд, Фронтенд'],
       'text': 'я ебу собак и готов трахнуть сразу несколько котов backend frontend tenorflow fastapi pytorch'}
rating_system = Model(pca, kmeans, model)
print(rating_system.get_predictions(dct))


