from data_fetcher import fetch_sales, fetch_customers, fetch_products
from transform import clean_data, calculate_weekly_aggregates, calculate_kpis, merge_datasets
from visualize_export import create_weekly_chart, create_kpi_summary, export_results
from notifier import send_email_notification


def main():
    print("1. Laen andmed Supabase API-st...")
    sales_df = fetch_sales("2023-01-01", "2025-03-31")
    customers_df = fetch_customers()
    products_df = fetch_products()

    print("\n2. Puhastan müügiandmed...")
    sales_clean = clean_data(sales_df)

    print("\n3. Liidan müügi- ja kliendiandmed...")
    merged_df = merge_datasets(sales_clean, customers_df)

    print("\n4. Arvutan nädalased koondid...")
    weekly_df = calculate_weekly_aggregates(sales_clean)

    print("\n5. Arvutan KPI-d...")
    kpis = calculate_kpis(sales_clean)

    print("\n6. Loon visualiseeringud...")
    weekly_chart = create_weekly_chart(weekly_df)
    kpi_summary = create_kpi_summary(kpis)

    if weekly_chart is not None:
        weekly_chart.show()

    if kpi_summary is not None:
        kpi_summary.show()

    print("\n7. Ekspordin tulemused...")
    export_results(
        weekly_df,
        output_dir="output",
        file_prefix="weekly_aggregates",
        figures={
            "weekly_revenue_chart": weekly_chart,
            "kpi_summary": kpi_summary
        }
    )

    subject = "UrbanStyle pipeline õnnestus ✅"

    notification_message = f"""
Pipeline õnnestus ✅

Total revenue: €{kpis['total_revenue']:.2f}
Unique customers: {kpis['unique_customers']}
Average order value: €{kpis['avg_order_value']:.2f}

Sales rows: {sales_df.shape[0]}
Customers rows: {customers_df.shape[0]}
Products rows: {products_df.shape[0]}
Weekly rows: {weekly_df.shape[0]}
""".strip()

    send_email_notification(subject, notification_message)

    print("\nKPI tulemused:")
    print(kpis)

    print("\nAndmete kontroll:")
    print("Sales:", sales_df.shape)
    print("Customers:", customers_df.shape)
    print("Products:", products_df.shape)
    print("Merged:", merged_df.shape)
    print("Weekly:", weekly_df.shape)


if __name__ == "__main__":
    main()