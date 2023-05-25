from libreco.data import DataInfo
from libreco.algorithms import NCF, BPR
import tensorflow as tf
import os
import warnings
warnings.filterwarnings('ignore')

def load_ncf_model():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    reco_models_dir = os.path.join(base_dir, 'static', 'reco_models')
    ncf_anime_dir = os.path.join(reco_models_dir, 'ncf_anime')
    # important to reset graph if model is loaded in the same shell.
    tf.compat.v1.reset_default_graph()
    # load data_info
    data_info = DataInfo.load(ncf_anime_dir, model_name="ncf_model_anime")
    model = NCF.load(path=ncf_anime_dir, model_name="ncf_model_anime", data_info=data_info, manual=False)
    return model

def load_bpr_model():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    reco_models_dir = os.path.join(base_dir, 'static', 'reco_models')
    bpr_anime_dir = os.path.join(reco_models_dir, 'bpr_anime')
    # important to reset graph if model is loaded in the same shell.
    tf.compat.v1.reset_default_graph()
    # load data_info
    data_info = DataInfo.load(bpr_anime_dir, model_name="bpr_model_anime")
    model = BPR.load(path=bpr_anime_dir, model_name="bpr_model_anime", data_info=data_info, manual=False)
    return model


# load models
ncf_model = load_ncf_model()
bpr_model = load_bpr_model()


# get recommendations
def get_ncf_recommendations(user_id, num_items=10):
    recommendations = ncf_model.recommend_user(user=user_id, n_rec=num_items)
    return list(recommendations.values())[0].tolist()

def get_bpr_recommendations(user_id, num_items=10):
    recommendations = bpr_model.recommend_user(user=user_id, n_rec=num_items)
    return list(recommendations.values())[0].tolist()
