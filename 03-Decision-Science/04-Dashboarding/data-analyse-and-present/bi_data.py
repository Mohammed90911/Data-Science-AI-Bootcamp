"""
Utilities to load, clean and aggregate the Olist dataset for analysis and visualization.

This module builds on the Olist package to fetch raw tables and provides a set of
functions that:
- clean and enrich order and customer tables,
- aggregate order items at the order level,
- produce a consolidated "sales" order-level table,
- expose ready-made aggregation tables for dashboards and plots.

Global state
------------
data : dict
    Loaded once at module import via Olist().get_data(). Expected keys (at least):
    'orders', 'order_items', 'customers', 'sellers'. Each value is a pandas DataFrame.

Main functions
--------------
sales_by_period(period='D')
    Aggregate order-level sales metrics by customer_state and a time period (e.g. 'D', 'W', 'ME').

sales_by_customer_state()
    Aggregate total sales and number of orders by customer_state.

sales_by_seller_state()
    Aggregate sales metrics by seller_state.

Examples
--------
>>> from bi_data import sales, sales_by_period
>>> monthly = sales_by_period('ME')       # aggregated by month and customer state
"""

import numpy as np
import pandas as pd
from olist.data import Olist


# #############################################################################
# DATA PREPARATION
# #############################################################################

data = Olist().get_data()


def orders_cleaned():
    """
    Clean and enrich the orders table.

    This function:
    - Copies the raw orders table from the global `data` dict.
    - Converts timestamp columns to datetimes.
    - Computes duration columns (in days) as floats:
        - wait_time: delivery to customer - purchase
        - expected_wait_time: estimated delivery - purchase
        - time_to_carrier: delivered to carrier - purchase
        - shipping_time: delivered to customer - delivered to carrier
    - Reduces datetime columns to date precision (drops time-of-day).

    Returns:
        pandas.DataFrame: cleaned orders dataframe with additional columns:
            - order_purchase_timestamp (datetime64[ns], date precision)
            - order_approved_at (date)
            - order_delivered_carrier_date (date)
            - order_delivered_customer_date (date)
            - order_estimated_delivery_date (date)
            - wait_time, expected_wait_time, time_to_carrier, shipping_time (float, days)

    Notes:
        - Relies on `data['orders']` being present in the notebook namespace.
    """
    df = data["orders"].copy()

    # Convert timestamps to datetime
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    df["order_approved_at"] = pd.to_datetime(df["order_approved_at"])
    df["order_delivered_carrier_date"] = pd.to_datetime(
        df["order_delivered_carrier_date"]
    )
    df["order_delivered_customer_date"] = pd.to_datetime(
        df["order_delivered_customer_date"]
    )
    df["order_estimated_delivery_date"] = pd.to_datetime(
        df["order_estimated_delivery_date"]
    )

    # Calculate times
    df["wait_time"] = (
        df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
    ) / np.timedelta64(1, "D")
    df["expected_wait_time"] = (
        df["order_estimated_delivery_date"] - df["order_purchase_timestamp"]
    ) / np.timedelta64(1, "D")
    df["time_to_carrier"] = (
        df["order_delivered_carrier_date"] - df["order_purchase_timestamp"]
    ) / np.timedelta64(1, "D")
    df["shipping_time"] = (
        df["order_delivered_customer_date"] - df["order_delivered_carrier_date"]
    ) / np.timedelta64(1, "D")

    # Round datetime to the date (loose the time information)
    df["order_purchase_timestamp"] = df["order_purchase_timestamp"].dt.round("D")
    df["order_approved_at"] = df["order_approved_at"].dt.round("D")
    df["order_delivered_carrier_date"] = df["order_delivered_carrier_date"].dt.round(
        "D"
    )
    df["order_delivered_customer_date"] = df["order_delivered_customer_date"].dt.round(
        "D"
    )
    df["order_estimated_delivery_date"] = df["order_estimated_delivery_date"].dt.round(
        "D"
    )

    return df


def customers_cleaned():
    """
    Clean and return the customers table.
    """
    df = data["customers"]
    return df.drop(columns="customer_zip_code_prefix")


def order_items_grouped():
    """
    Aggregate order_items at the order level.

    Returns a DataFrame indexed by order_id with the following columns:
    - nb_items: count of order items in the order
    - nb_uniqe_products: number of unique products in the order
    - nb_uniqe_sellers: number of unique sellers in the order
    - sales: sum of price for the order
    - freight_value: sum of freight_value for the order
    """
    df = data["order_items"]

    df_agg = df.groupby("order_id").agg(
        nb_items=pd.NamedAgg(column="order_item_id", aggfunc="count"),
        nb_uniqe_products=pd.NamedAgg(column="product_id", aggfunc="nunique"),
        nb_uniqe_sellers=pd.NamedAgg(column="seller_id", aggfunc="nunique"),
        sales=pd.NamedAgg(column="price", aggfunc="sum"),
        freight_value=pd.NamedAgg(column="freight_value", aggfunc="sum"),
    )
    return df_agg


# #############################################################################
# COMBINED TABLE FOR ANALYSIS
# #############################################################################


def sales():
    """
    Build the sales dataset by joining cleaned orders, customers and aggregated order items.

    This function:
    - Calls orders_cleaned(), customers_cleaned() and order_items_grouped().
    - Merges orders (left) with customers on 'customer_id', then with order_items on 'order_id'.
    - Drops columns that are redundant for analysis ('customer_id', 'customer_city').
    - Returns a DataFrame containing order-level information enriched with:
        - customer_unique_id, customer_state (from customers)
        - wait_time, expected_wait_time, time_to_carrier, shipping_time (from orders_cleaned)
        - nb_items, nb_uniqe_products, nb_uniqe_sellers, sales, freight_value (from order_items_grouped)

    Returns:
        pandas.DataFrame: merged sales dataframe ready for aggregation/plotting.
    """
    orders = orders_cleaned()
    customers = customers_cleaned()
    order_items = order_items_grouped()

    df = orders.merge(customers, on="customer_id", how="inner").merge(
        order_items, on="order_id", how="inner"
    )

    # `customer_id` is different for every order.
    # The real customer identificator is `customer_unique_id`.
    df = df.drop(columns=["customer_id", "customer_city"])

    return df


# #############################################################################
# READY-MADE TABLES FOR VISUALIZATION
# #############################################################################


def sales_by_period(period="D"):
    """
    Aggregate order-level sales metrics by customer state and resampled time period.

    Parameters
    ----------
    period : str, optional
    A pandas offset alias used by DataFrame.resample (e.g. 'D', 'W', 'ME', 'QE', 'YE'), by default "D".

    Returns
    -------
    pandas.DataFrame
        DataFrame with one row per (customer_state, period) containing:
        - order_purchase_timestamp: period timestamp (after reset_index)
        - customer_state
        - nb_orders
        - nb_unique_customers
        - nb_items
        - avg_nb_uniqe_products
        - avg_nb_uniqe_sellers
        - sales
        - freight_value

    Notes
    -----
    - Missing periods are filled with zeros (.fillna(0)) and the result index is reset.
    """
    df = (
        sales()
        .set_index("order_purchase_timestamp")
        .groupby("customer_state")
        .resample(period)
        .agg(
            nb_orders=pd.NamedAgg(column="order_id", aggfunc="count"),
            nb_unique_customers=pd.NamedAgg(
                column="customer_unique_id", aggfunc="nunique"
            ),
            nb_items=pd.NamedAgg(column="nb_items", aggfunc="sum"),
            avg_nb_uniqe_products=pd.NamedAgg(
                column="nb_uniqe_products", aggfunc="mean"
            ),
            avg_nb_uniqe_sellers=pd.NamedAgg(column="nb_uniqe_sellers", aggfunc="mean"),
            sales=pd.NamedAgg(column="sales", aggfunc="sum"),
            freight_value=pd.NamedAgg(column="freight_value", aggfunc="sum"),
        )
        .fillna(0)
        .reset_index()
    )

    return df


def sales_by_customer_state():
    """
    Aggregate total sales and number of orders by customer state.

    This function:
    - Calls the notebook's sales() function to obtain order-level data.
    - Groups the data by 'customer_state' and computes:
        - sales: total sales (sum of the 'sales' column)
        - nb_orders: number of orders (count of 'order_id')
    - Resets the index and returns a DataFrame with one row per state.

    Returns
    -------
    pandas.DataFrame
        Columns:
        - customer_state (object): state code
        - sales (float): total sales for the state
        - nb_orders (int): number of orders for the state
    """
    df = (
        sales()
        .groupby("customer_state")[["sales", "order_id", "customer_unique_id"]]
        .agg(
            sales=pd.NamedAgg(column="sales", aggfunc="sum"),
            nb_orders=pd.NamedAgg(column="order_id", aggfunc="count"),
            nb_customers=pd.NamedAgg(column="customer_unique_id", aggfunc="nunique"),
        )
        .reset_index()
    )
    return df


def sales_by_seller_state():
    """
    Aggregate sales metrics by seller state.

    This function:
    - Reads `order_items` and `sellers` from the global `data` dict.
    - Joins order items with seller metadata on 'seller_id'.
    - Groups by 'seller_state' and computes:
        - sales: total price (sum of 'price')
        - nb_items: number of order items (count of 'order_id')
        - nb_sellers: number of distinct sellers in that state (nunique of 'seller_id')

    Returns:
        pandas.DataFrame: aggregated DataFrame indexed by 'seller_state' with columns
        ['sales', 'nb_items', 'nb_sellers'].

    """
    order_items = data["order_items"]
    sellers = data["sellers"]

    df = pd.merge(order_items, sellers, on="seller_id", how="inner")

    df_agg = (
        df.groupby(["seller_state"])
        .agg(
            sales=pd.NamedAgg(column="price", aggfunc="sum"),
            nb_items=pd.NamedAgg(column="order_id", aggfunc="count"),
            nb_sellers=pd.NamedAgg(column="seller_id", aggfunc="nunique"),
        )
        .reset_index()
    )

    return df_agg
