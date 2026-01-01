import os
import pickle
from functools import lru_cache

from django.conf import settings

@lru_cache(maxsize=1)
def load_bundle():
     pkl_path = os.path.join(settings.BASE_DIR, 'recommender', 'ml', 'crop_recommendatio_best_model.pkl')
     
     with open(pkl_path, 'rb') as f:
         model_bundle = pickle.load(f)
         
     assert 'model' in model_bundle and "feature_cols" in model_bundle, "Invalid model bundle structure."
     return model_bundle


def predict_one(feature_dict):
     model_bundle = load_bundle()
     model = model_bundle['model']
     feature_cols = model_bundle['feature_cols']
     
     X = [[float(feature_dict[col]) for col in feature_cols]]
     
     pred = model.predict(X)
     return pred[0]

