import os
import time
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL või SUPABASE_KEY puudub .env failist.")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_with_pagination(table_name, start_date=None, end_date=None, retries=3, page_size=1000):
    all_data = []
    page = 0

    while True:
        for attempt in range(retries):
            try:
                query = supabase.table(table_name).select("*")

                if start_date and table_name == "sales":
                    query = query.gte("sale_date", start_date)

                if end_date and table_name == "sales":
                    query = query.lte("sale_date", end_date)

                response = query.range(page * page_size, (page + 1) * page_size - 1).execute()

                rows = response.data if response.data else []
                all_data.extend(rows)

                if len(rows) < page_size:
                    return pd.DataFrame(all_data)

                page += 1
                break

            except Exception as e:
                if attempt < retries - 1:
                    wait_time = 2 ** attempt
                    print(f"Viga tabeli {table_name} päringul, proovin uuesti {wait_time} sek pärast...")
                    time.sleep(wait_time)
                else:
                    raise Exception(f"Supabase päring ebaõnnestus tabelile '{table_name}': {e}")


def fetch_sales(start_date=None, end_date=None):
    try:
        df = fetch_with_pagination("sales", start_date=start_date, end_date=end_date)
        print(f"Sales andmed laaditud: {len(df)} rida")
        return df
    except Exception as e:
        print(f"Viga fetch_sales funktsioonis: {e}")
        return pd.DataFrame()


def fetch_customers():
    try:
        df = fetch_with_pagination("customers")
        print(f"Customers andmed laaditud: {len(df)} rida")
        return df
    except Exception as e:
        print(f"Viga fetch_customers funktsioonis: {e}")
        return pd.DataFrame()


def fetch_products():
    try:
        df = fetch_with_pagination("products")
        print(f"Products andmed laaditud: {len(df)} rida")
        return df
    except Exception as e:
        print(f"Viga fetch_products funktsioonis: {e}")
        return pd.DataFrame()


if __name__ == "__main__":
    sales_df = fetch_sales("2023-01-01", "2025-03-31")
    customers_df = fetch_customers()
    products_df = fetch_products()

    print("\nSALES HEAD:")
    print(sales_df.head())

    print("\nCUSTOMERS HEAD:")
    print(customers_df.head())

    print("\nPRODUCTS HEAD:")
    print(products_df.head())