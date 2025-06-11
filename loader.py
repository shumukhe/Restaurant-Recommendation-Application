import pickle
import csv
import random
import pandas as pd
from model import create_collab_model
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
photos_json_path = os.path.join(BASE_DIR, "Data", "photos.json")
business_data_path = os.path.join(BASE_DIR, "Processed_Data", "business.csv")

# Global cache variables
_model = None
_user_cache = None
_user2idx = None
_idx2business = None

def load_encoders():
    with open(os.path.join(BASE_DIR, 'business_encoder.pickle'), 'rb') as b:
        business_encoder = pickle.load(b)
    with open(os.path.join(BASE_DIR, 'user_encoder.pickle'), 'rb') as b:
        user_encoder = pickle.load(b)
    return business_encoder, user_encoder, len(business_encoder.classes_), len(user_encoder.classes_)

def create_dict(business_encoder, user_encoder):
    business2idx = dict(zip(business_encoder.classes_, business_encoder.transform(business_encoder.classes_)))
    idx2business = dict(zip(business_encoder.transform(business_encoder.classes_), business_encoder.classes_))
    user2idx = dict(zip(user_encoder.classes_, user_encoder.transform(user_encoder.classes_)))
    idx2user = dict(zip(user_encoder.transform(user_encoder.classes_), user_encoder.classes_))
    return business2idx, idx2business, user2idx, idx2user

def load_cache():
    global _user_cache
    if _user_cache is None:
        try:
            with open(os.path.join(BASE_DIR, 'recommendation_cache.pickle'), 'rb') as b:
                _user_cache = pickle.load(b)
        except FileNotFoundError:
            _user_cache = {}
    return _user_cache

def load_content_scores():
    with open(os.path.join(BASE_DIR, 'content_based_scores.pickle'), 'rb') as b:
        content_based_scores = pickle.load(b)
    return content_based_scores

def load_data():
    global _model, _user2idx, _idx2business

    if _model is None or _user2idx is None or _idx2business is None:
        print("Loading model and encoders...")
        business_encoder, user_encoder, num_businesses, num_users = load_encoders()
        business2idx, idx2business, user2idx, idx2user = create_dict(business_encoder, user_encoder)

        model = create_collab_model(num_businesses, num_users)
        model.load_weights(os.path.join(BASE_DIR, 'model_weights.h5'))
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mae'])

        _model = model
        _user2idx = user2idx
        _idx2business = idx2business

    return _idx2business, _user2idx, _model, load_cache()

def get_photo(restaurant_id, df):
    filenames = list(df[df['business_id'] == restaurant_id]['photo_id'].values)
    try:
        filename = random.sample(filenames, 1)[0]
        filepath = f"https://res.cloudinary.com/dnsvyb8zc/image/upload/Home/{filename}.jpg"
    except:
        filepath = "https://cdn.dribbble.com/users/1012566/screenshots/4187820/media/985748436085f06bb2bd63686ff491a5.jpg"
    return filepath

def get_restaurant_data(restaurents):
    restaurant_data = []
    photos_df = pd.read_json(photos_json_path, lines=True)

    with open(business_data_path, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            restaurant_id = row['business_id']
            if restaurant_id in restaurents:
                restaurant_data.append({
                    'id': restaurant_id,
                    'name': row['name'],
                    'rating': row['stars'],
                    'image_url': get_photo(restaurant_id, photos_df),
                    'address': row['address'],
                    'hours': eval(row['hours']) if row['hours'] else {}
                })
    return restaurant_data

def load_categories():
    with open(os.path.join(BASE_DIR, 'search_category.pickle'), 'rb') as b:
        all_categories = pickle.load(b)
    random.shuffle(all_categories)
    return all_categories
