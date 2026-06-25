import os
import pandas as pd

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def get_data(table_name):

    data = []

    page_size = 1000
    page = 0

    while True:

        response = (
            supabase
            .table(table_name)
            .select("*")
            .range(
                page * page_size,
                (page + 1) * page_size - 1
            )
            .execute()
        )

        data.extend(response.data)

        if len(response.data) < page_size:
            break

        page += 1

    return pd.DataFrame(data)



def fetch_customers():

    try:
        df = get_data("customers")

        print(f"Customer rows: {len(df)}")

        return df

    except Exception as e:

        print(f"Customer error: {e}")

        return pd.DataFrame()



def fetch_products():

    try:

        df = get_data("products")

        print(f"Product rows: {len(df)}")

        return df

    except Exception as e:

        print(f"Product error: {e}")

        return pd.DataFrame()
    

 

def fetch_sales(start_date, end_date):

    try:

        df = get_data("sales")

        df["sale_date"] = pd.to_datetime(df["sale_date"])

        df = df[
            (df["sale_date"] >= start_date) &
            (df["sale_date"] <= end_date)
        ]

        print(f"Sales rows: {len(df)}")

        return df

    except Exception as e:

        print(f"Sales error: {e}")

        return pd.DataFrame()
    
# TEST

df_customers = fetch_customers()
print(df_customers.head())


df_products = fetch_products()
print(df_products.head())


df_sales = fetch_sales(
    "2023-01-01",
    "2025-03-31"
)

print(df_sales.head())