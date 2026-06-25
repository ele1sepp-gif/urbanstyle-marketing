import logging
import time

from data_fetcher import fetch_sales, fetch_customers
from transform import (
    clean_data,
    validate_data,
    calculate_weekly_aggregates,
    calculate_kpis,
    merge_datasets
)
from visualize_export import export_results


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_pipeline():

    try:
        logging.info("PIPELINE START")

        # -------------------
        # 1. EXTRACT
        # -------------------
        logging.info("Step 1: Fetching data")

        df_sales = fetch_sales("2023-01-01", "2025-03-31")
        df_customers = fetch_customers()

        logging.info(f"Sales rows: {len(df_sales)}")
        logging.info(f"Customer rows: {len(df_customers)}")

        # -------------------
        # 2. TRANSFORM
        # -------------------
        logging.info("Step 2: Cleaning data")

        df_sales_clean = clean_data(df_sales)

        logging.info("Step 2.1: Validation")
        validate_data(df_sales_clean)

        logging.info("Step 2.2: Weekly aggregates")
        weekly = calculate_weekly_aggregates(df_sales_clean)

        logging.info("Step 2.3: KPIs")
        kpis = calculate_kpis(df_sales_clean)

        logging.info("Step 2.4: Merge datasets")
        merged = merge_datasets(df_sales, df_customers)

        # -------------------
        # 3. LOAD / VISUALIZE
        # -------------------
        export_results(weekly, kpis)

        logging.info(
            f"Pipeline completed. "
            f"Processed {len(df_sales_clean)} clean sales rows"
        )

        logging.info("PIPELINE SUCCESS")

        return weekly, kpis, merged


    except Exception as e:
        logging.error(f"PIPELINE FAILED: {e}")
        raise


if __name__ == "__main__":

    start_time = time.time()

    run_pipeline()

    elapsed = time.time() - start_time

    logging.info(f"Total runtime: {elapsed:.2f} seconds")