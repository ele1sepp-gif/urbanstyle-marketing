import os
from datetime import datetime
import plotly.express as px


# 1. Weekly chart
def create_weekly_chart(df_weekly):

    fig = px.line(
        df_weekly,
        x=df_weekly.index,
        y="weekly_revenue",
        title="Nädalane tulu"
    )

    return fig


# 2. KPI summary (tabelina)
def create_kpi_summary(kpis):

    from plotly.subplots import make_subplots
    import plotly.graph_objects as go

    fig = make_subplots(
        rows=1,
        cols=3,
        specs=[[{"type": "indicator"},
                {"type": "indicator"},
                {"type": "indicator"}]]
    )

    fig.add_trace(
        go.Indicator(
            mode="number",
            value=kpis["total_revenue"],
            title={"text": "Total Revenue (€)"},
            number={"valueformat": ",.2f"}
        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Indicator(
            mode="number",
            value=kpis["unique_customers"],
            title={"text": "Unique Customers"}
        ),
        row=1,
        col=2
    )

    fig.add_trace(
        go.Indicator(
            mode="number",
            value=kpis["avg_order_value"],
            title={"text": "Average Order Value (€)"},
            number={"valueformat": ",.2f"}
        ),
        row=1,
        col=3
    )

    fig.update_layout(
        title="KPI Dashboard",
        height=300
    )

    return fig


# 3. export funktsioon
def export_results(df_weekly, kpis):

    # output kaust
    os.makedirs("output", exist_ok=True)

    date_str = datetime.now().strftime("%Y%m%d")

    # CSV export (weekly data)
    csv_path = f"output/weekly_{date_str}.csv"
    df_weekly.to_csv(csv_path)

    # KPI HTML
    kpi_fig = create_kpi_summary(kpis)
    kpi_html = f"output/kpis_{date_str}.html"
    kpi_fig.write_html(kpi_html)

    # Weekly chart HTML
    weekly_fig = create_weekly_chart(df_weekly)
    weekly_html = f"output/weekly_{date_str}.html"
    weekly_fig.write_html(weekly_html)

    print("Export tehtud!")
    print("Failid loodud output/ kausta")

if __name__ == "__main__":

    from transform import (
        weekly,
        kpis
    )

    export_results(
        weekly,
        kpis
    )
