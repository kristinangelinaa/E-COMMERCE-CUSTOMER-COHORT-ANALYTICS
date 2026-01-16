"""
E-Commerce Data Cleaning Script
Author: Analytics Team
Date: 2026-01-16

This script cleans the Online Retail dataset for customer cohort analysis.
We'll handle missing values, remove duplicates, and prepare the data for analysis.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Let's load the data first
print("=" * 60)
print("E-COMMERCE DATA CLEANING PIPELINE")
print("=" * 60)
print("\nStep 1: Loading the dataset...")

df = pd.read_csv('online_retail_II UCI.csv', encoding='ISO-8859-1')

print(f"✓ Dataset loaded successfully!")
print(f"  - Total rows: {len(df):,}")
print(f"  - Total columns: {len(df.columns)}")

# Check the basic info
print("\n" + "=" * 60)
print("Step 2: Initial Data Exploration")
print("=" * 60)

print("\nColumn names and types:")
print(df.dtypes)

print("\nMissing values count:")
missing_data = df.isnull().sum()
print(missing_data[missing_data > 0])

print(f"\nDate range: {df['InvoiceDate'].min()} to {df['InvoiceDate'].max()}")

# Start cleaning process
print("\n" + "=" * 60)
print("Step 3: Data Cleaning Process")
print("=" * 60)

# Make a copy to preserve original
df_clean = df.copy()

# 3.1 - Remove rows with missing Customer ID (we need this for cohort analysis!)
print("\n3.1 Handling missing Customer IDs...")
before_count = len(df_clean)
df_clean = df_clean[df_clean['Customer ID'].notna()]
removed = before_count - len(df_clean)
print(f"  - Removed {removed:,} rows without Customer ID")
print(f"  - Remaining rows: {len(df_clean):,}")

# 3.2 - Clean up the Description column
print("\n3.2 Handling missing descriptions...")
missing_desc = df_clean['Description'].isna().sum()
print(f"  - Found {missing_desc:,} rows with missing descriptions")
df_clean['Description'] = df_clean['Description'].fillna('NO DESCRIPTION')

# 3.3 - Remove cancelled transactions (Invoice starts with 'C')
print("\n3.3 Removing cancelled transactions...")
before_count = len(df_clean)
df_clean = df_clean[~df_clean['Invoice'].astype(str).str.startswith('C')]
removed = before_count - len(df_clean)
print(f"  - Removed {removed:,} cancelled transactions")

# 3.4 - Remove negative quantities and prices
print("\n3.4 Cleaning quantities and prices...")
before_count = len(df_clean)
df_clean = df_clean[(df_clean['Quantity'] > 0) & (df_clean['Price'] > 0)]
removed = before_count - len(df_clean)
print(f"  - Removed {removed:,} rows with invalid quantity/price")

# 3.5 - Convert data types properly
print("\n3.5 Converting data types...")
df_clean['Customer ID'] = df_clean['Customer ID'].astype(int)
df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'])
df_clean['Invoice'] = df_clean['Invoice'].astype(str)
print("  ✓ Data types converted successfully")

# 3.6 - Create some useful calculated fields
print("\n3.6 Creating calculated fields...")
df_clean['TotalAmount'] = df_clean['Quantity'] * df_clean['Price']
df_clean['Year'] = df_clean['InvoiceDate'].dt.year
df_clean['Month'] = df_clean['InvoiceDate'].dt.month
df_clean['YearMonth'] = df_clean['InvoiceDate'].dt.to_period('M')
df_clean['Date'] = df_clean['InvoiceDate'].dt.date
print("  ✓ Added: TotalAmount, Year, Month, YearMonth, Date")

# 3.7 - Remove duplicate transactions (exact same transaction recorded twice)
print("\n3.7 Checking for duplicates...")
before_count = len(df_clean)
df_clean = df_clean.drop_duplicates()
removed = before_count - len(df_clean)
print(f"  - Removed {removed:,} duplicate rows")

# 3.8 - Sort the data
df_clean = df_clean.sort_values(['Customer ID', 'InvoiceDate'])
df_clean = df_clean.reset_index(drop=True)

# Final summary
print("\n" + "=" * 60)
print("Step 4: Cleaning Summary")
print("=" * 60)

print(f"\nOriginal dataset: {len(df):,} rows")
print(f"Cleaned dataset: {len(df_clean):,} rows")
print(f"Data reduction: {((len(df) - len(df_clean)) / len(df) * 100):.2f}%")

print("\nCleaned dataset overview:")
print(f"  - Unique customers: {df_clean['Customer ID'].nunique():,}")
print(f"  - Unique invoices: {df_clean['Invoice'].nunique():,}")
print(f"  - Unique products: {df_clean['StockCode'].nunique():,}")
print(f"  - Date range: {df_clean['InvoiceDate'].min()} to {df_clean['InvoiceDate'].max()}")
print(f"  - Total revenue: ${df_clean['TotalAmount'].sum():,.2f}")

# Save the cleaned data
print("\n" + "=" * 60)
print("Step 5: Saving Cleaned Data")
print("=" * 60)

# Save as CSV
df_clean.to_csv('cleaned_ecommerce_data.csv', index=False)
print("✓ Saved as: cleaned_ecommerce_data.csv")

# Also save as parquet for faster loading in the future
df_clean.to_parquet('cleaned_ecommerce_data.parquet', index=False)
print("✓ Saved as: cleaned_ecommerce_data.parquet")

print("\n" + "=" * 60)
print("DATA CLEANING COMPLETED SUCCESSFULLY!")
print("=" * 60)

# Quick data quality check
print("\nFinal Data Quality Check:")
print("Missing values per column:")
print(df_clean.isnull().sum())

print("\nSample of cleaned data:")
print(df_clean.head(10))

print("\nData is ready for cohort analysis!")
