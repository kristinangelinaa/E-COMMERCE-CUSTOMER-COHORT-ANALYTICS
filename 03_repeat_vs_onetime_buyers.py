"""
Repeat vs One-Time Buyers Analysis
Author: Analytics Team
Date: 2026-01-16

This script segments customers into one-time vs repeat buyers and analyzes:
- Customer distribution
- Revenue contribution
- Average order value
- Purchase frequency patterns
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("REPEAT VS ONE-TIME BUYERS ANALYSIS")
print("=" * 70)

# Load cleaned data
print("\nLoading data...")
df = pd.read_parquet('cleaned_ecommerce_data.parquet')
print(f"✓ Loaded {len(df):,} transactions")

# Step 1: Calculate purchase frequency per customer
print("\n" + "=" * 70)
print("Step 1: Calculating Purchase Frequency")
print("=" * 70)

# Count unique orders (invoices) per customer
customer_orders = df.groupby('Customer ID').agg({
    'Invoice': 'nunique',
    'InvoiceDate': ['min', 'max'],
    'TotalAmount': ['sum', 'mean', 'count']
}).reset_index()

# Flatten column names
customer_orders.columns = ['Customer_ID', 'OrderCount', 'FirstPurchase',
                           'LastPurchase', 'TotalRevenue', 'AvgTransactionValue',
                           'TotalTransactions']

print(f"✓ Analyzed {len(customer_orders):,} customers")

# Step 2: Segment customers
print("\n" + "=" * 70)
print("Step 2: Segmenting Customers")
print("=" * 70)

# Define customer segments based on order count
def classify_customer(order_count):
    if order_count == 1:
        return 'One-Time Buyer'
    elif order_count == 2:
        return 'Two-Time Buyer'
    elif order_count <= 5:
        return 'Occasional Buyer (3-5 orders)'
    elif order_count <= 10:
        return 'Regular Buyer (6-10 orders)'
    else:
        return 'Loyal Customer (10+ orders)'

customer_orders['CustomerSegment'] = customer_orders['OrderCount'].apply(classify_customer)

# Also create a simple binary classification
customer_orders['CustomerType'] = customer_orders['OrderCount'].apply(
    lambda x: 'One-Time Buyer' if x == 1 else 'Repeat Buyer'
)

print("Customer Segmentation:")
segment_counts = customer_orders['CustomerSegment'].value_counts().sort_index()
for segment, count in segment_counts.items():
    percentage = (count / len(customer_orders)) * 100
    print(f"  {segment}: {count:,} ({percentage:.2f}%)")

# Step 3: Revenue analysis by segment
print("\n" + "=" * 70)
print("Step 3: Revenue Analysis by Segment")
print("=" * 70)

revenue_by_segment = customer_orders.groupby('CustomerSegment').agg({
    'TotalRevenue': ['sum', 'mean'],
    'Customer_ID': 'count'
}).round(2)

revenue_by_segment.columns = ['TotalRevenue', 'AvgRevenuePerCustomer', 'CustomerCount']
revenue_by_segment['RevenueShare_%'] = (
    revenue_by_segment['TotalRevenue'] / revenue_by_segment['TotalRevenue'].sum() * 100
).round(2)

print("\nRevenue by Customer Segment:")
print(revenue_by_segment)

# Step 4: Binary comparison (One-Time vs Repeat)
print("\n" + "=" * 70)
print("Step 4: One-Time vs Repeat Buyers Comparison")
print("=" * 70)

binary_comparison = customer_orders.groupby('CustomerType').agg({
    'Customer_ID': 'count',
    'TotalRevenue': ['sum', 'mean'],
    'OrderCount': 'mean',
    'AvgTransactionValue': 'mean'
}).round(2)

binary_comparison.columns = ['CustomerCount', 'TotalRevenue', 'AvgRevenuePerCustomer',
                             'AvgOrdersPerCustomer', 'AvgTransactionValue']

# Add percentages
binary_comparison['Customer_%'] = (
    binary_comparison['CustomerCount'] / binary_comparison['CustomerCount'].sum() * 100
).round(2)

binary_comparison['Revenue_%'] = (
    binary_comparison['TotalRevenue'] / binary_comparison['TotalRevenue'].sum() * 100
).round(2)

print("\nOne-Time vs Repeat Buyers:")
print(binary_comparison)

# Step 5: Time-based analysis
print("\n" + "=" * 70)
print("Step 5: Customer Lifetime Analysis")
print("=" * 70)

# Calculate days between first and last purchase
customer_orders['CustomerLifetime_Days'] = (
    customer_orders['LastPurchase'] - customer_orders['FirstPurchase']
).dt.days

# Purchase frequency (orders per month for customers who made repeat purchases)
repeat_customers = customer_orders[customer_orders['OrderCount'] > 1].copy()
repeat_customers['PurchaseFrequency_DaysPerOrder'] = (
    repeat_customers['CustomerLifetime_Days'] / (repeat_customers['OrderCount'] - 1)
).round(2)

print(f"\nRepeat Buyers Analysis:")
print(f"  Total repeat buyers: {len(repeat_customers):,}")
print(f"  Avg customer lifetime: {repeat_customers['CustomerLifetime_Days'].mean():.0f} days")
print(f"  Avg purchase frequency: {repeat_customers['PurchaseFrequency_DaysPerOrder'].mean():.0f} days between orders")
print(f"  Median orders per repeat buyer: {repeat_customers['OrderCount'].median():.0f}")

# Step 6: RFM Analysis (Recency, Frequency, Monetary)
print("\n" + "=" * 70)
print("Step 6: RFM Analysis")
print("=" * 70)

# Calculate recency (days since last purchase from the dataset's last date)
analysis_date = df['InvoiceDate'].max()
customer_orders['Recency_Days'] = (analysis_date - customer_orders['LastPurchase']).dt.days

# Create RFM scores (1-5, where 5 is best)
# Using rank-based scoring to handle duplicates better
customer_orders['R_Score'] = pd.qcut(customer_orders['Recency_Days'].rank(method='first'),
                                      q=5, labels=[5, 4, 3, 2, 1])
customer_orders['F_Score'] = pd.qcut(customer_orders['OrderCount'].rank(method='first'),
                                      q=5, labels=[1, 2, 3, 4, 5])
customer_orders['M_Score'] = pd.qcut(customer_orders['TotalRevenue'].rank(method='first'),
                                      q=5, labels=[1, 2, 3, 4, 5])

# Create RFM segment
customer_orders['RFM_Score'] = (customer_orders['R_Score'].astype(str) +
                                customer_orders['F_Score'].astype(str) +
                                customer_orders['M_Score'].astype(str))

# Categorize customers based on RFM
def categorize_rfm(row):
    if row['F_Score'] >= 4 and row['M_Score'] >= 4:
        return 'Champions'
    elif row['F_Score'] >= 3 and row['M_Score'] >= 3:
        return 'Loyal Customers'
    elif row['R_Score'] >= 4:
        return 'Potential Loyalists'
    elif row['R_Score'] >= 3:
        return 'At Risk'
    else:
        return 'Lost'

customer_orders['RFM_Segment'] = customer_orders.apply(categorize_rfm, axis=1)

rfm_summary = customer_orders.groupby('RFM_Segment').agg({
    'Customer_ID': 'count',
    'TotalRevenue': 'sum'
}).sort_values('TotalRevenue', ascending=False)

print("\nRFM Segmentation:")
print(rfm_summary)

# Step 7: Export data for visualization
print("\n" + "=" * 70)
print("Step 7: Exporting Analysis Results")
print("=" * 70)

# Export main customer analysis
customer_orders_export = customer_orders.copy()
customer_orders_export['FirstPurchase'] = customer_orders_export['FirstPurchase'].dt.date
customer_orders_export['LastPurchase'] = customer_orders_export['LastPurchase'].dt.date
customer_orders_export.to_csv('customer_segmentation_analysis.csv', index=False)
print("✓ Saved: customer_segmentation_analysis.csv")

# Export segment summary
segment_summary = pd.DataFrame({
    'Segment': segment_counts.index,
    'CustomerCount': segment_counts.values,
    'Customer_%': (segment_counts.values / segment_counts.sum() * 100).round(2)
})

# Add revenue data
segment_revenue = customer_orders.groupby('CustomerSegment')['TotalRevenue'].sum()
segment_summary = segment_summary.merge(
    pd.DataFrame({'Segment': segment_revenue.index, 'TotalRevenue': segment_revenue.values}),
    on='Segment'
)
segment_summary['Revenue_%'] = (
    segment_summary['TotalRevenue'] / segment_summary['TotalRevenue'].sum() * 100
).round(2)

segment_summary.to_csv('segment_summary.csv', index=False)
print("✓ Saved: segment_summary.csv")

# Export binary comparison
binary_comparison.to_csv('onetime_vs_repeat_summary.csv')
print("✓ Saved: onetime_vs_repeat_summary.csv")

# Export RFM analysis
rfm_export = customer_orders[['Customer_ID', 'OrderCount', 'TotalRevenue',
                               'Recency_Days', 'R_Score', 'F_Score', 'M_Score',
                               'RFM_Score', 'RFM_Segment']].copy()
rfm_export.to_csv('rfm_customer_segmentation.csv', index=False)
print("✓ Saved: rfm_customer_segmentation.csv")

# Create a monthly trend of new vs repeat buyers
print("\n" + "=" * 70)
print("Step 8: Monthly Trends Analysis")
print("=" * 70)

# Get first purchase date for each customer
first_purchase = df.groupby('Customer ID')['InvoiceDate'].min().reset_index()
first_purchase.columns = ['Customer ID', 'FirstPurchaseDate']

# Merge back to main data
df_with_first = df.merge(first_purchase, on='Customer ID')

# Classify each transaction as from new or existing customer
df_with_first['IsFirstPurchase'] = (
    df_with_first['InvoiceDate'] == df_with_first['FirstPurchaseDate']
)
df_with_first['BuyerType'] = df_with_first['IsFirstPurchase'].apply(
    lambda x: 'New Customer' if x else 'Repeat Customer'
)

# Monthly summary
monthly_trend = df_with_first.groupby([df_with_first['InvoiceDate'].dt.to_period('M'),
                                       'BuyerType']).agg({
    'Customer ID': 'nunique',
    'TotalAmount': 'sum',
    'Invoice': 'nunique'
}).reset_index()

monthly_trend.columns = ['YearMonth', 'BuyerType', 'UniqueCustomers', 'Revenue', 'Orders']
monthly_trend['YearMonth'] = monthly_trend['YearMonth'].astype(str)

# Pivot for easier visualization
monthly_pivot = monthly_trend.pivot(index='YearMonth',
                                    columns='BuyerType',
                                    values=['UniqueCustomers', 'Revenue', 'Orders'])

monthly_pivot.to_csv('monthly_new_vs_repeat_trend.csv')
print("✓ Saved: monthly_new_vs_repeat_trend.csv")

print("\nMonthly trend sample (first 6 months):")
print(monthly_trend.head(12))

# Step 9: Summary statistics
print("\n" + "=" * 70)
print("Step 9: Key Metrics Summary")
print("=" * 70)

one_time = customer_orders[customer_orders['CustomerType'] == 'One-Time Buyer']
repeat = customer_orders[customer_orders['CustomerType'] == 'Repeat Buyer']

summary_metrics = {
    'Metric': [
        'Total Customers',
        'One-Time Buyers',
        'Repeat Buyers',
        'One-Time Buyers %',
        'Repeat Buyers %',
        'Revenue from One-Time Buyers',
        'Revenue from Repeat Buyers',
        'Revenue % from One-Time',
        'Revenue % from Repeat',
        'Avg Revenue per One-Time Buyer',
        'Avg Revenue per Repeat Buyer',
        'Avg Orders per Repeat Buyer',
        'Repeat Purchase Rate'
    ],
    'Value': [
        f"{len(customer_orders):,}",
        f"{len(one_time):,}",
        f"{len(repeat):,}",
        f"{len(one_time) / len(customer_orders) * 100:.2f}%",
        f"{len(repeat) / len(customer_orders) * 100:.2f}%",
        f"${one_time['TotalRevenue'].sum():,.2f}",
        f"${repeat['TotalRevenue'].sum():,.2f}",
        f"{one_time['TotalRevenue'].sum() / customer_orders['TotalRevenue'].sum() * 100:.2f}%",
        f"{repeat['TotalRevenue'].sum() / customer_orders['TotalRevenue'].sum() * 100:.2f}%",
        f"${one_time['TotalRevenue'].mean():.2f}",
        f"${repeat['TotalRevenue'].mean():.2f}",
        f"{repeat['OrderCount'].mean():.2f}",
        f"{len(repeat) / len(customer_orders) * 100:.2f}%"
    ]
}

summary_df = pd.DataFrame(summary_metrics)
summary_df.to_csv('repeat_buyers_summary_metrics.csv', index=False)
print("✓ Saved: repeat_buyers_summary_metrics.csv")

print("\nKey Metrics:")
print(summary_df.to_string(index=False))

print("\n" + "=" * 70)
print("REPEAT VS ONE-TIME BUYERS ANALYSIS COMPLETED!")
print("=" * 70)

print("\n🎯 KEY INSIGHTS:")
print(f"1. {len(repeat) / len(customer_orders) * 100:.1f}% of customers are repeat buyers")
print(f"2. Repeat buyers generate {repeat['TotalRevenue'].sum() / customer_orders['TotalRevenue'].sum() * 100:.1f}% of total revenue")
print(f"3. Average repeat buyer spends {repeat['TotalRevenue'].mean() / one_time['TotalRevenue'].mean():.1f}x more than one-time buyers")
print(f"4. Average repeat buyer makes {repeat['OrderCount'].mean():.1f} orders")
print(f"5. Most valuable segment: {revenue_by_segment.sort_values('TotalRevenue', ascending=False).index[0]}")

print("\n✓ All analysis files ready for visualization!")
