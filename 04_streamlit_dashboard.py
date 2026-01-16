"""
E-Commerce Customer Analytics - 3D Interactive Dashboard
Author: Analytics Team
Date: 2026-01-16

This Streamlit app provides interactive 3D visualizations for:
- Customer acquisition cohort analysis
- Repeat vs one-time buyer patterns
- RFM segmentation
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="E-Commerce Customer Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    .stMetric label {
        color: #1f1f1f !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #0e1117 !important;
        font-size: 32px !important;
        font-weight: 700 !important;
    }
    .stMetric [data-testid="stMetricDelta"] {
        color: #0e1117 !important;
        font-weight: 600 !important;
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 20px;
    }
    h2 {
        color: #2c3e50;
        padding-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Helper function to load data with caching
@st.cache_data
def load_cohort_data():
    """Load all cohort analysis data"""
    try:
        retention = pd.read_csv('cohort_retention_matrix.csv', index_col=0)
        customer_count = pd.read_csv('cohort_customer_count.csv', index_col=0)
        revenue = pd.read_csv('cohort_revenue_matrix.csv', index_col=0)
        ltv = pd.read_csv('cohort_ltv_analysis.csv')
        return retention, customer_count, revenue, ltv
    except Exception as e:
        st.error(f"Error loading cohort data: {e}")
        return None, None, None, None

@st.cache_data
def load_customer_data():
    """Load customer segmentation data"""
    try:
        customers = pd.read_csv('customer_segmentation_analysis.csv')
        segment_summary = pd.read_csv('segment_summary.csv')
        rfm = pd.read_csv('rfm_customer_segmentation.csv')

        # Load monthly trend with proper handling of multi-level headers
        monthly_trend = pd.read_csv('monthly_new_vs_repeat_trend.csv', header=[0, 1])
        # Flatten the multi-level columns
        monthly_trend.columns = ['_'.join(col).strip('_') for col in monthly_trend.columns.values]
        monthly_trend = monthly_trend.rename(columns={'YearMonth_': 'YearMonth'})

        return customers, segment_summary, rfm, monthly_trend
    except Exception as e:
        st.error(f"Error loading customer data: {e}")
        return None, None, None, None

def apply_dark_mode_layout(fig):
    """Apply consistent dark mode styling to plotly figures"""
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        title_font=dict(size=16, color='white'),
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        ),
        xaxis=dict(
            gridcolor='rgba(128,128,128,0.2)',
            color='white'
        ),
        yaxis=dict(
            gridcolor='rgba(128,128,128,0.2)',
            color='white'
        )
    )
    return fig

# Main app
def main():
    # Title and introduction
    st.title("🛍️ E-Commerce Customer & Cohort Analytics Dashboard")
    st.markdown("### Advanced 3D Visualizations for Stakeholder Insights")

    # Sidebar navigation
    st.sidebar.title("📊 Navigation")
    page = st.sidebar.radio(
        "Select Analysis:",
        ["Overview", "Cohort Analysis", "Customer Segmentation", "RFM Analysis", "Revenue Deep Dive"]
    )

    # Load data
    retention, customer_count, revenue, ltv = load_cohort_data()
    customers, segment_summary, rfm, monthly_trend = load_customer_data()

    if retention is None or customers is None:
        st.error("Please run the analysis scripts first to generate the required data files.")
        return

    # Page routing
    if page == "Overview":
        show_overview(ltv, segment_summary)
    elif page == "Cohort Analysis":
        show_cohort_analysis(retention, customer_count, revenue, ltv)
    elif page == "Customer Segmentation":
        show_customer_segmentation(customers, segment_summary, monthly_trend)
    elif page == "RFM Analysis":
        show_rfm_analysis(rfm, customers)
    elif page == "Revenue Deep Dive":
        show_revenue_analysis(revenue, ltv, customers)

def show_overview(ltv, segment_summary):
    """Display executive summary with key metrics"""
    st.header("📈 Executive Summary")
    st.markdown("---")

    # Key metrics in columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_customers = ltv['CohortSize'].sum()
        st.metric("Total Customers", f"{int(total_customers):,}")

    with col2:
        avg_ltv = ltv['AvgLTV'].mean()
        st.metric("Avg Customer LTV", f"${avg_ltv:,.2f}")

    with col3:
        total_revenue = ltv['TotalRevenue'].sum()
        st.metric("Total Revenue", f"${total_revenue:,.0f}")

    with col4:
        num_cohorts = len(ltv)
        st.metric("Active Cohorts", f"{num_cohorts}")

    st.markdown("---")

    # Two column layout for charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Customer Distribution by Segment")

        # 3D Pie Chart for customer segments
        fig = go.Figure(data=[go.Pie(
            labels=segment_summary['Segment'],
            values=segment_summary['CustomerCount'],
            hole=0.3,
            marker=dict(
                colors=px.colors.qualitative.Set3,
                line=dict(color='white', width=2)
            ),
            textinfo='label+percent',
            textposition='auto'
        )])

        fig.update_layout(
            height=400,
            showlegend=True,
            title_text="Customer Segments Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("💰 Revenue by Customer Segment")

        # 3D Bar chart for revenue
        fig = px.bar(
            segment_summary,
            x='Segment',
            y='TotalRevenue',
            color='Revenue_%',
            color_continuous_scale='Viridis',
            title='Revenue Contribution by Segment'
        )

        fig.update_layout(
            height=400,
            xaxis_tickangle=-45
        )

        st.plotly_chart(fig, use_container_width=True)

    # Top insights
    st.markdown("---")
    st.subheader("🎯 Key Business Insights & Recommendations")
    st.markdown("*Data-driven findings that should guide your strategy*")

    # Calculate insights
    repeat_buyers = segment_summary[segment_summary['Segment'] != 'One-Time Buyer']
    repeat_revenue_pct = repeat_buyers['Revenue_%'].sum()
    best_segment = segment_summary.loc[segment_summary['TotalRevenue'].idxmax()]
    one_time_pct = segment_summary[segment_summary['Segment'] == 'One-Time Buyer']['Customer_%'].values[0]

    insight_col1, insight_col2, insight_col3 = st.columns(3)

    with insight_col1:
        st.info(f"""
        **💰 Revenue Concentration**

        Repeat buyers drive **{repeat_revenue_pct:.1f}%** of total revenue

        **What this means:**
        Your repeat customers are the lifeblood of the business. Every 1% increase in retention could significantly boost revenue.

        **Action:** Invest heavily in retention programs, loyalty rewards, and customer success initiatives.
        """)

    with insight_col2:
        st.success(f"""
        **🏆 Golden Segment**

        **{best_segment['Segment']}** generates the most revenue

        **Why it matters:**
        This segment represents ${best_segment['TotalRevenue']:,.0f} ({best_segment['Revenue_%']:.1f}% of revenue) from just {best_segment['CustomerCount']:,} customers.

        **Action:** Study their behavior, preferences, and create VIP programs to retain and replicate this segment.
        """)

    with insight_col3:
        st.warning(f"""
        **📊 Customer Value**

        Average LTV: **${ltv['AvgLTV'].mean():.2f}**

        **The opportunity:**
        With {one_time_pct:.0f}% still one-time buyers, there's huge potential to increase LTV through conversion campaigns.

        **Action:** Focus on first 90-day onboarding to convert one-timers into repeat buyers.
        """)

def show_cohort_analysis(retention, customer_count, revenue, ltv):
    """Display cohort analysis with 3D visualizations"""
    st.header("📅 Customer Acquisition Cohort Analysis")
    st.markdown("---")

    # Cohort selection
    cohorts = retention.index.tolist()
    selected_cohorts = st.multiselect(
        "Select Cohorts to Highlight:",
        cohorts,
        default=cohorts[:5] if len(cohorts) >= 5 else cohorts
    )

    # 3D Surface Plot - Retention Rate
    st.subheader("🌊 3D Retention Surface Map")
    st.markdown("*Visualize retention patterns across cohorts and time periods*")

    # Add explanation
    st.info("""
    **📖 Understanding the Retention Landscape:**
    Imagine this as a 3D map of customer loyalty. Each "mountain" represents a cohort's retention journey over time.

    **What you're seeing:**
    - Moving **left to right** = watching customers over months (Month 0 → Month 24)
    - Moving **front to back** = comparing different customer cohorts
    - **Height of the surface** = % of customers still active
    - **Colors:** 🟢 Green (strong retention) → 🟡 Yellow (moderate) → 🔴 Red (high churn)

    **Look for these patterns:**
    - **Steep cliffs** = danger zones where customers are leaving
    - **Plateaus** = stable, loyal customer periods
    - **Consistent mountain range** = your retention strategy is working!

    💡 **Interactive:** Drag to rotate | Scroll to zoom | Click and explore!
    """)

    # Prepare data for 3D surface
    x = list(range(retention.shape[1]))  # Months
    y = list(range(len(retention)))  # Cohorts
    z = retention.values

    fig = go.Figure(data=[go.Surface(
        x=x,
        y=y,
        z=z,
        colorscale='RdYlGn',
        colorbar=dict(title='Retention %'),
    )])

    fig.update_layout(
        title='Customer Retention Rate Over Time (3D Surface)',
        scene=dict(
            xaxis_title='Months Since Acquisition',
            yaxis_title='Cohort Index',
            zaxis_title='Retention %',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.3)
            )
        ),
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    # 3D Scatter Plot - LTV by Cohort
    st.subheader("💎 Cohort LTV 3D Visualization")

    st.info("""
    **📖 Finding Your Golden Cohorts:**
    Each bubble represents a customer cohort. Think of this as a treasure map - you're looking for the biggest, brightest bubbles in the top-right corner!

    **What each dimension tells you:**
    - **Horizontal position (X):** How many customers joined (cohort size)
    - **Vertical position (Y):** Total revenue they've generated
    - **Height (Z):** Average value per customer (LTV)
    - **Bubble size:** Confirms cohort size (bigger = more customers)
    - **Color:** 🟡 Bright yellow = highest value customers | 🟣 Purple = lower value

    **The jackpot cohorts:**
    - **Far right + high up** = Large groups bringing in serious revenue
    - **High on Z-axis** = Each customer is individually valuable
    - **Bright yellow bubbles** = Your most profitable customer segments!

    💎 Hover over bubbles to see exact cohort details.
    """)

    fig = go.Figure(data=[go.Scatter3d(
        x=ltv['CohortSize'],
        y=ltv['TotalRevenue'],
        z=ltv['AvgLTV'],
        mode='markers+text',
        marker=dict(
            size=ltv['CohortSize'] / 20,
            color=ltv['AvgLTV'],
            colorscale='Plasma',
            showscale=True,
            colorbar=dict(title='Avg LTV'),
            line=dict(width=0.5, color='white')
        ),
        text=ltv['CohortMonth'],
        textposition='top center',
        hovertemplate='<b>%{text}</b><br>' +
                     'Cohort Size: %{x}<br>' +
                     'Total Revenue: $%{y:,.0f}<br>' +
                     'Avg LTV: $%{z:,.2f}<br>' +
                     '<extra></extra>'
    )])

    fig.update_layout(
        scene=dict(
            xaxis_title='Cohort Size',
            yaxis_title='Total Revenue ($)',
            zaxis_title='Average LTV ($)',
            camera=dict(
                eye=dict(x=1.5, y=-1.5, z=1.2)
            )
        ),
        height=600,
        title='Cohort Performance: Size vs Revenue vs LTV'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Heatmap - Customer Count by Cohort-Period
    st.subheader("🔥 Customer Count Heatmap")

    st.info("""
    **📖 How to Read This Heatmap:**
    - **Rows:** Different customer cohorts (by acquisition month)
    - **Columns:** Months since acquisition (M0 = first month, M1 = second month, etc.)
    - **Color Intensity:** Darker blue = more active customers
    - **First column (M0)** always shows the initial cohort size
    - **Fading colors to the right** show customer drop-off over time

    🎯 **Key Insight:** The rate of color fade-out indicates your retention strength!
    """)

    fig = px.imshow(
        customer_count,
        labels=dict(x="Months Since Acquisition", y="Cohort", color="Customers"),
        x=[f'M{i}' for i in range(customer_count.shape[1])],
        y=customer_count.index,
        color_continuous_scale='Blues',
        aspect='auto'
    )

    fig.update_layout(
        title='Active Customers by Cohort and Month',
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    # Detailed cohort table
    st.subheader("📋 Cohort Performance Table")

    ltv_display = ltv.copy()
    ltv_display['AvgLTV'] = ltv_display['AvgLTV'].apply(lambda x: f"${x:,.2f}")
    ltv_display['TotalRevenue'] = ltv_display['TotalRevenue'].apply(lambda x: f"${x:,.0f}")
    ltv_display['CohortSize'] = ltv_display['CohortSize'].apply(lambda x: f"{int(x):,}")

    st.dataframe(ltv_display, use_container_width=True, height=400)

def show_customer_segmentation(customers, segment_summary, monthly_trend):
    """Display customer segmentation analysis"""
    st.header("👥 Customer Segmentation Analysis")
    st.markdown("---")

    # Key metrics
    one_time = customers[customers['CustomerType'] == 'One-Time Buyer']
    repeat = customers[customers['CustomerType'] == 'Repeat Buyer']

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("One-Time Buyers", f"{len(one_time):,}",
                 delta=f"{len(one_time)/len(customers)*100:.1f}%")

    with col2:
        st.metric("Repeat Buyers", f"{len(repeat):,}",
                 delta=f"{len(repeat)/len(customers)*100:.1f}%")

    with col3:
        avg_repeat_orders = repeat['OrderCount'].mean()
        st.metric("Avg Orders (Repeat)", f"{avg_repeat_orders:.1f}")

    with col4:
        revenue_ratio = repeat['TotalRevenue'].sum() / one_time['TotalRevenue'].sum()
        st.metric("Repeat/One-Time Revenue", f"{revenue_ratio:.1f}x")

    st.markdown("---")

    # 3D Scatter - Order Count vs Revenue vs Lifetime
    st.subheader("🎯 Customer Value 3D Distribution")

    st.success("""
    **📖 The Customer Journey in 3D:**
    Picture your customer base as a galaxy - each dot is a customer, and their position tells their story!

    **The three dimensions of customer behavior:**
    - **Left to Right (X):** Few orders → Many orders (buying frequency)
    - **Bottom to Top (Y):** Low spend → High spend (revenue contribution)
    - **Front to Back (Z):** New customer → Long-time loyal (relationship duration)
    - **Colors:** 🔴 Red/Orange = super frequent buyers | 🔵 Blue = one-timers or occasional shoppers

    **What the patterns reveal:**
    - **Big cluster at origin?** Lots of one-time buyers (opportunity to convert them!)
    - **Dots in back-top-right?** Your VIP champions - treasure them!
    - **Scattered middle zone?** Growing customers - nurture them into loyalists!
    - **Lone stars far out?** Unique high-value customers - study their behavior!

    💡 Showing a sample of {sample_size:,} customers for optimal performance.
    """.format(sample_size=min(2000, len(customers))))

    # Sample data for better performance (if too many customers)
    sample_size = min(2000, len(customers))
    customers_sample = customers.sample(n=sample_size, random_state=42)

    fig = go.Figure(data=[go.Scatter3d(
        x=customers_sample['OrderCount'],
        y=customers_sample['TotalRevenue'],
        z=customers_sample['CustomerLifetime_Days'],
        mode='markers',
        marker=dict(
            size=4,
            color=customers_sample['OrderCount'],
            colorscale='Turbo',
            showscale=True,
            colorbar=dict(title='Orders'),
            opacity=0.7
        ),
        text=customers_sample['CustomerSegment'],
        hovertemplate='<b>%{text}</b><br>' +
                     'Orders: %{x}<br>' +
                     'Revenue: $%{y:,.2f}<br>' +
                     'Lifetime: %{z} days<br>' +
                     '<extra></extra>'
    )])

    fig.update_layout(
        scene=dict(
            xaxis_title='Number of Orders',
            yaxis_title='Total Revenue ($)',
            zaxis_title='Customer Lifetime (Days)',
            camera=dict(
                eye=dict(x=1.3, y=1.3, z=1.3)
            )
        ),
        height=600,
        title=f'Customer Distribution (Sample of {sample_size:,} customers)'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Segment comparison - 3D Bar Chart
    st.subheader("📊 Segment Performance Comparison")

    col1, col2 = st.columns(2)

    with col1:
        # Customer count by segment - 3D effect
        fig = go.Figure(data=[go.Bar(
            x=segment_summary['Segment'],
            y=segment_summary['CustomerCount'],
            marker=dict(
                color=segment_summary['CustomerCount'],
                colorscale='Blues',
                showscale=False,
                line=dict(color='rgb(8,48,107)', width=1.5)
            ),
            text=segment_summary['Customer_%'].apply(lambda x: f"{x:.1f}%"),
            textposition='auto',
        )])

        fig.update_layout(
            title='Customer Count by Segment',
            xaxis_tickangle=-45,
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Revenue by segment
        fig = go.Figure(data=[go.Bar(
            x=segment_summary['Segment'],
            y=segment_summary['TotalRevenue'],
            marker=dict(
                color=segment_summary['TotalRevenue'],
                colorscale='Greens',
                showscale=False,
                line=dict(color='darkgreen', width=1.5)
            ),
            text=segment_summary['Revenue_%'].apply(lambda x: f"{x:.1f}%"),
            textposition='auto',
        )])

        fig.update_layout(
            title='Revenue by Segment',
            xaxis_tickangle=-45,
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    # Monthly trend
    if monthly_trend is not None and not monthly_trend.empty:
        st.subheader("📈 New vs Repeat Customers Trend")

        st.success("""
        **📖 Reading the Trend:** This chart tells the story of your customer acquisition over time.
        The **blue line** (New Customers) shows first-time buyers each month, while the **red line** (Repeat Customers) reveals how many existing customers came back to purchase again. A healthy business shows both lines growing, but the repeat line should ideally stay high - it means you're retaining customers!
        """)

        try:
            # Debug: Check available columns
            # st.write("Available columns:", monthly_trend.columns.tolist())

            # Extract the data properly - check for the actual column name
            if 'YearMonth' in monthly_trend.columns:
                year_months = monthly_trend['YearMonth'].dropna().values
            else:
                # Use index if YearMonth column doesn't exist
                year_months = monthly_trend.index.tolist()

            # Get unique customers data
            new_customers = monthly_trend['UniqueCustomers_New Customer'].dropna().values
            repeat_customers = monthly_trend['UniqueCustomers_Repeat Customer'].dropna().values

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=year_months,
                y=new_customers,
                mode='lines+markers',
                name='New Customer',
                line=dict(width=3, color='#636EFA'),
                marker=dict(size=8)
            ))

            fig.add_trace(go.Scatter(
                x=year_months,
                y=repeat_customers,
                mode='lines+markers',
                name='Repeat Customer',
                line=dict(width=3, color='#EF553B'),
                marker=dict(size=8)
            ))

            fig.update_layout(
                title='Monthly Customer Acquisition: New vs Repeat',
                xaxis_title='Month',
                yaxis_title='Unique Customers',
                hovermode='x unified',
                height=400,
                xaxis_tickangle=-45,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(gridcolor='rgba(128,128,128,0.2)'),
                yaxis=dict(gridcolor='rgba(128,128,128,0.2)')
            )

            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating monthly trend chart: {e}")

def show_rfm_analysis(rfm, customers):
    """Display RFM segmentation analysis"""
    st.header("🎯 RFM (Recency, Frequency, Monetary) Analysis")
    st.markdown("---")

    # RFM segment distribution
    rfm_segment_dist = rfm['RFM_Segment'].value_counts()

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("RFM Segment Distribution")

        fig = go.Figure(data=[go.Pie(
            labels=rfm_segment_dist.index,
            values=rfm_segment_dist.values,
            hole=0.4,
            marker=dict(
                colors=px.colors.qualitative.Pastel,
                line=dict(color='white', width=2)
            )
        )])

        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("RFM Segment Metrics")

        rfm_metrics = customers.groupby('RFM_Segment').agg({
            'Customer_ID': 'count',
            'TotalRevenue': 'sum',
            'OrderCount': 'mean'
        }).round(2)

        rfm_metrics.columns = ['Customers', 'Total Revenue', 'Avg Orders']
        rfm_metrics = rfm_metrics.sort_values('Total Revenue', ascending=False)

        st.dataframe(rfm_metrics, use_container_width=True)

    # 3D RFM Scatter Plot
    st.subheader("📍 3D RFM Customer Map")
    st.markdown("*Interactive 3D visualization of customer RFM scores*")

    # Add explanation
    st.info("""
    **📖 The RFM Customer Value Cube:**
    This is your customer segmentation in action! RFM scores customers on three critical behaviors. Imagine a cube where the best customers live in the top-back-right corner.

    **The three scores explained:**
    - **Recency (X-axis, Front→Back):** Bought yesterday (5) vs. ages ago (1) - Recent buyers are "warm leads"
    - **Frequency (Y-axis, Bottom→Top):** Rare shopper (1) vs. regular visitor (5) - Frequency = loyalty
    - **Monetary (Z-axis, Left→Right):** Small spender (1) vs. big spender (5) - Money talks!
    - **Color gradient:** 🔴 Red/Orange = highest total revenue | 🔵 Blue = lower revenue

    **Find your customer segments:**
    - **Top-back-right cluster?** 🏆 Champions - recent, frequent, big spenders (protect them!)
    - **Low on all axes?** 😴 Lost customers - they haven't bought in ages
    - **High F & M, but low R?** ⚠️ At-risk VIPs - win them back NOW!
    - **High R, low F & M?** 🌱 New customers - potential to grow!

    💡 Rotate the cube to spot your segments | Each dot is a customer story!
    """)

    # Sample for performance
    sample_size = min(2000, len(rfm))
    rfm_sample = rfm.sample(n=sample_size, random_state=42)

    fig = go.Figure(data=[go.Scatter3d(
        x=rfm_sample['R_Score'].astype(float),
        y=rfm_sample['F_Score'].astype(float),
        z=rfm_sample['M_Score'].astype(float),
        mode='markers',
        marker=dict(
            size=5,
            color=rfm_sample['TotalRevenue'],
            colorscale='Jet',
            showscale=True,
            colorbar=dict(title='Revenue ($)'),
            opacity=0.8,
            line=dict(width=0.5, color='white')
        ),
        text=rfm_sample['RFM_Segment'],
        hovertemplate='<b>%{text}</b><br>' +
                     'Recency Score: %{x}<br>' +
                     'Frequency Score: %{y}<br>' +
                     'Monetary Score: %{z}<br>' +
                     '<extra></extra>'
    )])

    fig.update_layout(
        scene=dict(
            xaxis_title='Recency Score (1-5)',
            yaxis_title='Frequency Score (1-5)',
            zaxis_title='Monetary Score (1-5)',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.3)
            )
        ),
        height=700,
        title=f'RFM Customer Distribution (Sample of {sample_size:,})'
    )

    st.plotly_chart(fig, use_container_width=True)

    # RFM Score distribution heatmap
    st.subheader("🔥 RFM Score Heatmap")

    st.success("""
    **📖 The Customer Concentration Map:**
    This heatmap reveals where most of your customers cluster based on their buying patterns. It's like a heat signature showing "hot zones" of customer concentration!

    **Reading the grid:**
    - **Vertical (Frequency Score):** How often they buy (1=rarely → 5=very often)
    - **Horizontal (Monetary Score):** How much they spend (1=low spender → 5=big spender)
    - **Color Intensity:** 🔴 **Dark Red** = lots of customers here | 🟡 **Light Yellow** = few customers

    **What the patterns tell you:**
    - **Dark bottom-left corner?** Most customers buy rarely and spend little (opportunity zone!)
    - **Hot spot in top-right?** You have a strong base of frequent, high-spending customers (jackpot!)
    - **Diagonal streak?** Balanced customer base - spending increases with frequency (healthy sign)
    - **Dark red anywhere unexpected?** That's your target segment to understand and replicate!

    🎯 **Strategic Play:** Find the biggest red squares - those are your most common customer types. Then ask: "How do we move customers UP and to the RIGHT?"
    """)

    rfm_pivot = rfm.pivot_table(
        index='F_Score',
        columns='M_Score',
        values='Customer_ID',
        aggfunc='count',
        fill_value=0
    )

    fig = px.imshow(
        rfm_pivot,
        labels=dict(x="Monetary Score", y="Frequency Score", color="Customers"),
        color_continuous_scale='YlOrRd',
        aspect='auto'
    )

    fig.update_layout(
        title='Customer Distribution by Frequency and Monetary Scores',
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

def show_revenue_analysis(revenue, ltv, customers):
    """Display detailed revenue analysis"""
    st.header("💰 Revenue Deep Dive")
    st.markdown("---")

    # Revenue metrics
    total_revenue = ltv['TotalRevenue'].sum()
    avg_revenue_per_cohort = ltv['TotalRevenue'].mean()
    best_cohort = ltv.loc[ltv['TotalRevenue'].idxmax()]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Revenue", f"${total_revenue:,.0f}")

    with col2:
        st.metric("Avg Revenue per Cohort", f"${avg_revenue_per_cohort:,.0f}")

    with col3:
        st.metric("Best Cohort", best_cohort['CohortMonth'],
                 delta=f"${best_cohort['TotalRevenue']:,.0f}")

    st.markdown("---")

    # 3D Revenue Surface
    st.subheader("🌊 Revenue Surface Map by Cohort")

    st.warning("""
    **📖 Your Revenue Landscape:**
    This 3D surface shows the money story of each cohort over time. Think of it as a topographic map where peaks = high revenue periods!

    **Reading the terrain:**
    - **X-axis (Left→Right):** Customer's journey from Month 0 (acquisition) onward
    - **Y-axis (Front→Back):** Different cohort groups (by acquisition date)
    - **Z-axis (Height):** Revenue generated in dollars 💰
    - **Colors:** 🟡 Yellow peaks = high revenue months | 🟣 Purple valleys = lower revenue periods

    **What healthy revenue looks like:**
    - **Tall peaks in early months?** Strong onboarding and initial sales!
    - **Sustained elevation over time?** Customers keep buying - excellent retention!
    - **Sudden drop-offs?** Identify which cohorts fell off and investigate why
    - **Consistent wave pattern?** Seasonal trends you can predict and plan for

    💡 Rotate to see which cohorts and months drive the most revenue!
    """)

    x = list(range(revenue.shape[1]))
    y = list(range(len(revenue)))
    z = revenue.fillna(0).values

    fig = go.Figure(data=[go.Surface(
        x=x,
        y=y,
        z=z,
        colorscale='Viridis',
        colorbar=dict(title='Revenue ($)'),
    )])

    fig.update_layout(
        title='Revenue Generation Pattern Across Cohorts',
        scene=dict(
            xaxis_title='Months Since Acquisition',
            yaxis_title='Cohort Index',
            zaxis_title='Revenue ($)',
            camera=dict(
                eye=dict(x=1.5, y=-1.5, z=1.3)
            )
        ),
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    # Revenue by customer segment - 3D Bars
    st.subheader("📊 Revenue Distribution by Customer Type")

    segment_revenue = customers.groupby('CustomerSegment').agg({
        'TotalRevenue': 'sum',
        'Customer_ID': 'count'
    }).reset_index()

    segment_revenue.columns = ['Segment', 'TotalRevenue', 'CustomerCount']
    segment_revenue = segment_revenue.sort_values('TotalRevenue', ascending=False)

    fig = go.Figure(data=[go.Bar(
        x=segment_revenue['Segment'],
        y=segment_revenue['TotalRevenue'],
        marker=dict(
            color=segment_revenue['TotalRevenue'],
            colorscale='Plasma',
            showscale=True,
            colorbar=dict(title='Revenue'),
            line=dict(color='black', width=1)
        ),
        text=segment_revenue['TotalRevenue'].apply(lambda x: f"${x/1e6:.1f}M"),
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>' +
                     'Revenue: $%{y:,.0f}<br>' +
                     '<extra></extra>'
    )])

    fig.update_layout(
        title='Total Revenue by Customer Segment',
        xaxis_tickangle=-45,
        height=500,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

    # Cohort LTV trend
    st.subheader("📈 Average LTV Trend by Cohort")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=ltv['CohortMonth'],
        y=ltv['AvgLTV'],
        mode='lines+markers',
        line=dict(color='royalblue', width=3),
        marker=dict(size=10, color='lightblue', line=dict(width=2, color='darkblue')),
        fill='tozeroy',
        fillcolor='rgba(65, 105, 225, 0.2)'
    ))

    fig.update_layout(
        title='Average Customer Lifetime Value by Acquisition Cohort',
        xaxis_title='Cohort Month',
        yaxis_title='Average LTV ($)',
        height=400,
        hovermode='x',
        xaxis_tickangle=-45
    )

    st.plotly_chart(fig, use_container_width=True)

# Run the app
if __name__ == "__main__":
    main()
