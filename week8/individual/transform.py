import pandas as pd
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

def validate_data(df):

    errors = []

    # kontrollime, kas vajalikud veerud olemas
    required_columns = [
        "customer_id",
        "sale_date",
        "total_price"
    ]

    for column in required_columns:
        if column not in df.columns:
            errors.append(
                f"Puudub veerg: {column}"
            )


    # kontrollime hinnaväärtuseid
    if "total_price" in df.columns:
        if (df["total_price"] < 0).any():
            errors.append(
                "Leiti negatiivseid hindu"
            )


    # kontrollime kuupäeva tüüpi
    if "sale_date" in df.columns:
        if not pd.api.types.is_datetime64_any_dtype(
            df["sale_date"]
        ):
            errors.append(
                "sale_date ei ole datetime formaadis"
            )


    if errors:
        print("Valideerimise vead:")
        for error in errors:
            print("-", error)

        return False

    else:
        print("Valideerimine edukas")
        return True
    
def clean_data(df):

    df_clean = df.copy()

    # eemaldame duplikaadid
    df_clean = df_clean.drop_duplicates()

    # eemaldame read, kus olulised andmed puuduvad
    df_clean = df_clean.dropna(
        subset=[
            "customer_id",
            "sale_date",
            "total_price"
        ]
    )

    # muudame kuupäeva datetime formaati
    df_clean["sale_date"] = pd.to_datetime(
        df_clean["sale_date"]
    )

    # eemaldame negatiivsed hinnad
    df_clean = df_clean[
        df_clean["total_price"] > 0
    ]

    print("Puhastamine tehtud")
    print(f"Ridu alles: {len(df_clean)}")

    return df_clean

def calculate_weekly_aggregates(df):

    weekly = (
        df
        .resample(
            "W",
            on="sale_date"
        )
        .agg(
            {
                "total_price": "sum",
                "sale_id": "count"
            }
        )
    )

    weekly = weekly.rename(
        columns={
            "total_price": "weekly_revenue",
            "sale_id": "order_count"
        }
    )

    weekly["average_order_value"] = (
        weekly["weekly_revenue"] /
        weekly["order_count"]
    )

    print("Nädala koondnäitajad arvutatud")
    
    return weekly

def calculate_kpis(df):

    kpis = {
        "total_revenue": df["total_price"].sum(),
        "unique_customers": df["customer_id"].nunique(),
        "avg_order_value": df["total_price"].mean()
    }

    print("KPI-d arvutatud")

    return kpis

def merge_datasets(df_sales, df_customers):

    merged = pd.merge(
        df_sales,
        df_customers,
        on="customer_id",
        how="left"
    )

    print("Andmestikud ühendatud")
    print(f"Ridu: {len(merged)}")

    return merged

# TEST

#from data_fetcher import (
#    fetch_sales,
#    fetch_customers
#)#df_sales = fetch_sales(#    "2023-01-01",
#    "2025-12-31"
#)

#df_customers = fetch_customers()


#df_sales_clean = clean_data(df_sales)
##validate_data(df_sales_clean)

#weekly = calculate_weekly_aggregates(df_sales_clean)

#kpis = calculate_kpis(df_sales_clean)

#merged = merge_datasets(
#    df_sales,
#    df_customers
#)


#print("\nKPI tulemused:")
#print(kpis)

#print("\nWeekly:")
#print(weekly.head())

#print("\nMerged:")
#print(merged.head())