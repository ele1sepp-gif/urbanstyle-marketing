import pandas as pd


def clean_data(df):
    try:
        df = df.copy()

        print(f"Enne puhastust ridu: {len(df)}")

        df = df.drop_duplicates()

        if "sale_date" in df.columns:
            df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")

        if "total_price" in df.columns:
            df["total_price"] = pd.to_numeric(df["total_price"], errors="coerce")

        df = df.dropna(how="all")

        if "customer_id" in df.columns:
            df = df.dropna(subset=["customer_id"])

        if "total_price" in df.columns:
            df = df[df["total_price"].fillna(0) >= 0]

        print(f"Pärast puhastust ridu: {len(df)}")
        return df

    except Exception as e:
        print(f"Viga clean_data funktsioonis: {e}")
        return pd.DataFrame()


def calculate_weekly_aggregates(df):
    try:
        df = df.copy()

        if "sale_date" not in df.columns or "total_price" not in df.columns:
            raise ValueError("DataFrame peab sisaldama 'sale_date' ja 'total_price' veerge.")

        df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")
        df["total_price"] = pd.to_numeric(df["total_price"], errors="coerce")

        df = df.dropna(subset=["sale_date", "total_price"])

        weekly = (
            df.resample("W", on="sale_date")
            .agg(
                revenue=("total_price", "sum"),
                order_count=("sale_id", "nunique") if "sale_id" in df.columns else ("total_price", "count"),
                avg_order_value=("total_price", "mean")
            )
            .reset_index()
        )

        return weekly

    except Exception as e:
        print(f"Viga calculate_weekly_aggregates funktsioonis: {e}")
        return pd.DataFrame()


def calculate_kpis(df):
    try:
        df = df.copy()

        if "total_price" in df.columns:
            df["total_price"] = pd.to_numeric(df["total_price"], errors="coerce")

        kpis = {
            "total_revenue": float(df["total_price"].sum()) if "total_price" in df.columns else 0,
            "unique_customers": int(df["customer_id"].nunique()) if "customer_id" in df.columns else 0,
            "avg_order_value": float(df["total_price"].mean()) if "total_price" in df.columns else 0
        }

        return kpis

    except Exception as e:
        print(f"Viga calculate_kpis funktsioonis: {e}")
        return {}


def merge_datasets(df_sales, df_customers):
    try:
        if "customer_id" not in df_sales.columns or "customer_id" not in df_customers.columns:
            raise ValueError("Mõlemas DataFrame'is peab olema customer_id veerg.")

        merged_df = pd.merge(df_sales, df_customers, on="customer_id", how="left")
        return merged_df

    except Exception as e:
        print(f"Viga merge_datasets funktsioonis: {e}")
        return pd.DataFrame()


if __name__ == "__main__":
    sample_sales = pd.DataFrame({
        "sale_id": [1, 2, 2, 3],
        "customer_id": [101, 102, 102, 103],
        "sale_date": ["2025-03-01", "2025-03-02", "2025-03-02", "2025-03-08"],
        "total_price": [100, 150, 150, 200]
    })

    sample_customers = pd.DataFrame({
        "customer_id": [101, 102, 103],
        "first_name": ["Anna", "Marko", "Liisa"]
    })

    clean_df = clean_data(sample_sales)
    weekly_df = calculate_weekly_aggregates(clean_df)
    kpis = calculate_kpis(clean_df)
    merged_df = merge_datasets(clean_df, sample_customers)

    print("\nPUHASTATUD:")
    print(clean_df.head())

    print("\nNÄDALASED KOONDID:")
    print(weekly_df.head())

    print("\nKPI-d:")
    print(kpis)

    print("\nLIIDETUD:")
    print(merged_df.head())