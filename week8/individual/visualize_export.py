import os
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def create_weekly_chart(df_weekly):
    try:
        fig = px.line(
            df_weekly,
            x="sale_date",
            y="revenue",
            title="Nädalane tulu",
            markers=True
        )

        fig.update_layout(
            xaxis_title="Nädal",
            yaxis_title="Tulu (€)"
        )

        return fig

    except Exception as e:
        print(f"Viga create_weekly_chart funktsioonis: {e}")
        return None


def create_kpi_summary(kpis):
    try:
        fig = go.Figure()

        fig.add_trace(go.Indicator(
            mode="number",
            value=kpis.get("total_revenue", 0),
            title={"text": "Total Revenue"},
            number={"prefix": "€"},
            domain={"x": [0, 0.33], "y": [0, 1]}
        ))

        fig.add_trace(go.Indicator(
            mode="number",
            value=kpis.get("unique_customers", 0),
            title={"text": "Unique Customers"},
            domain={"x": [0.34, 0.66], "y": [0, 1]}
        ))

        fig.add_trace(go.Indicator(
            mode="number",
            value=kpis.get("avg_order_value", 0),
            title={"text": "Avg Order Value"},
            number={"prefix": "€"},
            domain={"x": [0.67, 1], "y": [0, 1]}
        ))

        fig.update_layout(title="KPI kokkuvõte")
        return fig

    except Exception as e:
        print(f"Viga create_kpi_summary funktsioonis: {e}")
        return None


def export_results(df, output_dir="output", file_prefix="results", figures=None):
    try:
        os.makedirs(output_dir, exist_ok=True)

        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = os.path.join(output_dir, f"{file_prefix}_{date_str}.csv")
        df.to_csv(csv_path, index=False)

        print(f"CSV salvestatud: {csv_path}")

        if figures:
            for fig_name, fig in figures.items():
                if fig is not None:
                    html_path = os.path.join(output_dir, f"{fig_name}_{date_str}.html")
                    fig.write_html(html_path)
                    print(f"HTML salvestatud: {html_path}")

    except Exception as e:
        print(f"Viga export_results funktsioonis: {e}")


if __name__ == "__main__":
    sample_df = pd.DataFrame({
        "sale_date": pd.to_datetime(["2025-03-02", "2025-03-09", "2025-03-16"]),
        "revenue": [1200, 1800, 1500],
        "order_count": [12, 15, 11],
        "avg_order_value": [100, 120, 136]
    })

    sample_kpis = {
        "total_revenue": 4500,
        "unique_customers": 35,
        "avg_order_value": 118
    }

    weekly_fig = create_weekly_chart(sample_df)
    kpi_fig = create_kpi_summary(sample_kpis)

    export_results(
        sample_df,
        output_dir="output",
        file_prefix="weekly_report",
        figures={
            "weekly_chart": weekly_fig,
            "kpi_summary": kpi_fig
        }
    )