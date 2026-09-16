import pandas as pd
import numpy as np
from olist.data import Olist
from olist.utils import haversine_distance

class Order:

    def __init__(self):
        self.data = Olist().get_data()

    def get_wait_time(self, is_delivered=True):
        orders = self.data['orders'].copy()

        if is_delivered:
            orders = orders[orders['order_status'] == 'delivered'].copy()

        orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
        orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
        orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])

        orders['wait_time'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']).dt.total_seconds() / 86400
        orders['expected_wait_time'] = (orders['order_estimated_delivery_date'] - orders['order_purchase_timestamp']).dt.total_seconds() / 86400
        orders['delay_vs_expected'] = (orders['order_delivered_customer_date'] - orders['order_estimated_delivery_date']).dt.total_seconds() / 86400
        orders['delay_vs_expected'] = orders['delay_vs_expected'].clip(lower=0)

        return orders[['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected', 'order_status']]

    def get_review_score(self):
        reviews = self.data['order_reviews'].copy()
        reviews['dim_is_five_star'] = reviews['review_score'].apply(lambda x: 1 if x == 5 else 0)
        reviews['dim_is_one_star'] = reviews['review_score'].apply(lambda x: 1 if x == 1 else 0)
        return reviews[['order_id', 'dim_is_five_star', 'dim_is_one_star', 'review_score']]

    def get_number_items(self):
        return self.data['order_items'].groupby('order_id').size().reset_index(name='number_of_items')

    def get_number_sellers(self):
        return self.data['order_items'].groupby('order_id')['seller_id'].nunique().reset_index(name='number_of_sellers')

    def get_price_and_freight(self):
        return self.data['order_items'].groupby('order_id').agg({'price': 'sum', 'freight_value': 'sum'}).reset_index()

    def get_distance_seller_customer(self):
        matching = self.data['order_items'][['order_id', 'seller_id']].drop_duplicates()
        orders = self.data['orders'][['order_id', 'customer_id']]
        sellers = self.data['sellers'][['seller_id', 'seller_zip_code_prefix']]
        customers = self.data['customers'][['customer_id', 'customer_zip_code_prefix']]

        geo = self.data['geolocation'].groupby('geolocation_zip_code_prefix').agg({
            'geolocation_lat': 'mean',
            'geolocation_lng': 'mean'
        }).reset_index()

        df = matching.merge(orders, on='order_id')\
                     .merge(sellers, on='seller_id')\
                     .merge(customers, on='customer_id')\
                     .merge(geo, left_on='seller_zip_code_prefix', right_on='geolocation_zip_code_prefix')\
                     .rename(columns={'geolocation_lat': 'seller_lat', 'geolocation_lng': 'seller_lng'})\
                     .drop(columns=['geolocation_zip_code_prefix'])\
                     .merge(geo, left_on='customer_zip_code_prefix', right_on='geolocation_zip_code_prefix')\
                     .rename(columns={'geolocation_lat': 'customer_lat', 'geolocation_lng': 'customer_lng'})\
                     .drop(columns=['geolocation_zip_code_prefix'])

        df = df.dropna(subset=['seller_lng', 'seller_lat', 'customer_lng', 'customer_lat']).copy()
        df['distance_seller_customer'] = np.vectorize(haversine_distance)(
            df['seller_lng'],
            df['seller_lat'],
            df['customer_lng'],
            df['customer_lat']
        )

        return df.groupby('order_id')['distance_seller_customer'].mean().reset_index()
    def get_training_data(self, is_delivered=True, with_distance_seller_customer=False):
        training_set = self.get_wait_time(is_delivered=is_delivered)\
            .merge(self.get_review_score(), on='order_id', how='inner')\
            .merge(self.get_number_items(), on='order_id', how='inner')\
            .merge(self.get_number_sellers(), on='order_id', how='inner')\
            .merge(self.get_price_and_freight(), on='order_id', how='inner')

        if with_distance_seller_customer:
            training_set = training_set.merge(self.get_distance_seller_customer(), on='order_id', how='left')

        return training_set.dropna()
