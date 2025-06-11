import numpy as np
import os
import random
import pickle
import csv
from loader import load_data, load_content_scores

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
business_data_path = os.path.join(BASE_DIR, "Processed_Data", "business.csv")

def collab_recommend_restaurants(user_id, idx2business, user2idx, model, user_cache):
    if user_id in user_cache.keys():
        sorted_scores = user_cache[user_id]
    else:
        useridx = user2idx[user_id]
        business_ids = list(idx2business.keys())
        user_input = np.full(len(business_ids), useridx)
        business_input = np.array(business_ids)
        preds = model.predict([user_input, business_input], batch_size=256)
        scores = dict(zip(business_ids, preds.flatten()))
        sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        user_cache[user_id] = sorted_scores
        with open('recommendation_cache.pickle', 'wb') as f:
            pickle.dump(user_cache, f)
    top_25 = sorted_scores[:25]
    top_10_restaurants = random.sample(top_25, 10)
    return [t[0] for t in top_10_restaurants]


def hybrid_recommend_restaurants(user_id, business_id, idx2business, user2idx, model, user_cache):
    content_based_scores = load_content_scores()
    business_pool = content_based_scores[business_id].sort_values(ascending=False)[:30].index
    useridx = user2idx[user_id]
    filtered_businesses = [b for b in idx2business.keys() if b in business_pool]
    user_input = np.full(len(filtered_businesses), useridx)
    business_input = np.array(filtered_businesses)
    preds = model.predict([user_input, business_input], batch_size=256)
    scores = dict(zip(filtered_businesses, preds.flatten()))
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    top_12 = sorted_scores[:12]
    top_6_restaurants = random.sample(top_12, 6)
    return [t[0] for t in top_6_restaurants]


def get_search_restaurants(cuisine):
    matching = {}
    with open(business_data_path, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            restaurant_id = row['business_id']
            if cuisine.lower() in row['categories'].lower(): 
                matching[restaurant_id] = float(row['stars'])
    matching_rating = sorted(matching.items(), key=lambda item: item[1], reverse=True)
    matching = matching_rating[:15]
    return [m[0] for m in matching]
