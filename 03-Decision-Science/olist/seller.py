import numpy as np
import pandas as pd
from olist.data import Olist
from olist.order import Order


class Seller:

    def __init__(self):
        self.data = Olist().get_data()
        self.order = Order()

    def get_seller_features(self):
        order_items = self.data["order_items"].copy()
        seller_features = (
            order_items.groupby("seller_id")
            .agg(
                quantity=("order_item_id", "count"),
                n_orders=("order_id", "nunique"),
                sales=("price", "sum"),
                freight=("freight_value", "sum"),
            )
            .reset_index()
        )
        return seller_features

    def get_review_score(self):
        order_items = self.data["order_items"].copy()
        orders = self.order.get_training_data()

        seller_orders = order_items[
            ["seller_id", "order_id"]
        ].drop_duplicates()
        df = seller_orders.merge(
            orders[["order_id", "review_score"]], on="order_id", how="inner"
        )

        cost_map = {1: 100, 2: 50, 3: 40, 4: 0, 5: 0}
        df["cost_of_reviews"] = df["review_score"].map(cost_map)

        seller_reviews = (
            df.groupby("seller_id")
            .agg(
                cost_of_reviews=("cost_of_reviews", "sum"),
                share_of_one_star_reviews=(
                    "review_score",
                    lambda x: (x == 1).mean(),
                ),
                share_of_five_star_reviews=(
                    "review_score",
                    lambda x: (x == 5).mean(),
                ),
                review_score=("review_score", "mean"),
            )
            .reset_index()
        )

        return seller_reviews

    def get_training_data(self):
        seller_features = self.get_seller_features()
        seller_reviews = self.get_review_score()

        sellers = seller_features.merge(
            seller_reviews, on="seller_id", how="inner"
        )

        matching_table = self.data["order_items"][
            ["seller_id", "order_id"]
        ].drop_duplicates()
        orders_df = self.data["orders"][
            ["order_id", "order_approved_at"]
        ].dropna()

        orders_df["order_approved_at"] = pd.to_datetime(
            orders_df["order_approved_at"]
        )

        seller_dates = matching_table.merge(
            orders_df, on="order_id", how="inner"
        )

        seller_months = (
            seller_dates.groupby("seller_id")["order_approved_at"]
            .agg(lambda x: max(1, np.ceil((x.max() - x.min()).days / 30)))
            .reset_index(name="months_active")
        )

        sellers = sellers.merge(seller_months, on="seller_id", how="left")
        sellers["months_active"] = sellers["months_active"].fillna(1)

        sellers["revenues"] = (sellers["sales"] * 0.10) + (
            sellers["months_active"] * 80
        )
        sellers["profits"] = sellers["revenues"] - sellers["cost_of_reviews"]

        return sellers
