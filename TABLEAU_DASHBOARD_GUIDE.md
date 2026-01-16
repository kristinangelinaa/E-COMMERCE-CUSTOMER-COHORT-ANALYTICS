# 📊 Tableau Dashboard Guide: E-Commerce Customer & Cohort Analytics

## 🎯 Dashboard Objectives

This guide will help you create a professional, insight-driven Tableau dashboard that clearly communicates:
1. **Customer Acquisition Cohorts** - How different customer cohorts perform over time
2. **Retention Patterns** - Which cohorts have the best retention rates
3. **Repeat vs One-Time Buyers** - The distribution and value of customer segments
4. **Revenue Analysis** - Where revenue is coming from and trends over time
5. **RFM Segmentation** - Customer value segments for targeted strategies

---

## 📁 Data Files You'll Need

Before starting, ensure you have these CSV files in your Tableau data folder:

### Core Data Files:
- `cleaned_ecommerce_data.csv` - Main transaction data
- `cohort_detailed_transactions.csv` - Transaction-level cohort data

### Pre-Aggregated Analysis Files:
- `cohort_retention_matrix.csv` - Retention rates by cohort and month
- `cohort_customer_count.csv` - Customer counts by cohort and period
- `cohort_revenue_matrix.csv` - Revenue by cohort and period
- `cohort_ltv_analysis.csv` - Lifetime value by cohort
- `customer_segmentation_analysis.csv` - Full customer segmentation data
- `segment_summary.csv` - Aggregated segment metrics
- `rfm_customer_segmentation.csv` - RFM scores and segments
- `monthly_new_vs_repeat_trend.csv` - Monthly trends

---

## 🚀 Getting Started with Tableau

### Step 1: Connect to Your Data

1. **Open Tableau Desktop**
2. Click on **"Text file"** under Connect
3. Navigate to your project folder
4. Select `cohort_detailed_transactions.csv` as your primary data source
5. Rename the data source to "Cohort Transactions"

### Step 2: Add Additional Data Sources

For each additional file:
1. Click **"Data" → "New Data Source"**
2. Connect to the CSV file
3. Rename appropriately (e.g., "Customer Segmentation", "RFM Analysis")

### Step 3: Create Relationships (if needed)

If using multiple data sources in one view:
1. Use **Customer_ID** as the primary key for joining customer-level data
2. Use **CohortMonth** for cohort-level joins

---

## 📊 Dashboard Layout Strategy

### Recommended Structure:

```
┌─────────────────────────────────────────────────────────┐
│  E-COMMERCE CUSTOMER & COHORT ANALYTICS                 │
│  [Filters: Date Range | Cohort | Country]              │
├──────────────────────┬──────────────────────────────────┤
│  KPI Cards (4 boxes) │  Monthly Revenue Trend           │
├──────────────────────┴──────────────────────────────────┤
│  Cohort Retention Heatmap (Large)                       │
├──────────────────────┬──────────────────────────────────┤
│  Customer Segments   │  RFM Distribution               │
│  (Pie/Donut)        │  (Scatter)                       │
├──────────────────────┴──────────────────────────────────┤
│  One-Time vs Repeat Comparison (Bar Charts)            │
└─────────────────────────────────────────────────────────┘
```

---

## 🎨 Building Key Visualizations

### Visualization 1: KPI Summary Cards

**Purpose:** Show key metrics at a glance

**Data Source:** Use "Cohort Transactions" or "Customer Segmentation"

**Steps:**
1. Create a new worksheet named "KPI - Total Revenue"
2. Drag `TotalAmount` to **Text** on the Marks card
3. Change aggregation to **SUM**
4. Format:
   - Font: Bold, 48pt
   - Number format: Currency, 0 decimals
   - Add label: "Total Revenue" below the number
5. Remove axes and headers (Right-click → Uncheck "Show Header")

**Repeat for these KPIs:**
- **Total Customers:** COUNT(DISTINCT [Customer ID])
- **Avg Customer LTV:** Use data from cohort_ltv_analysis.csv
- **Repeat Purchase Rate:**
  ```
  SUM(IF [CustomerType] = "Repeat Buyer" THEN 1 ELSE 0 END) / COUNT([Customer ID])
  ```

**Pro Tips:**
- Use different colors for each KPI (e.g., Blue, Green, Orange, Purple)
- Add a subtle background color to each card
- Include small trend indicators if you add date filters

---

### Visualization 2: Cohort Retention Heatmap

**Purpose:** Show retention rates across all cohorts and time periods

**Data Source:** `cohort_retention_matrix.csv`

**Steps:**

1. **Data Preparation:**
   - Load `cohort_retention_matrix.csv`
   - In Tableau, pivot the data:
     - Right-click the data source → "Edit Data Source"
     - Select all month columns (Month_0, Month_1, etc.)
     - Right-click → **"Pivot"**
   - Rename pivoted fields:
     - "Pivot Field Names" → "Month Index"
     - "Pivot Field Values" → "Retention Rate"

2. **Create the Heatmap:**
   - Create new worksheet: "Cohort Retention Heatmap"
   - Drag `CohortMonth` to **Rows**
   - Drag `Month Index` to **Columns**
   - Drag `Retention Rate` to **Color**
   - Drag `Retention Rate` to **Label**

3. **Format:**
   - Color palette: **Red-Yellow-Green** (diverging)
   - Center: 50%
   - Label format: 1 decimal place + "%" symbol
   - Square size: Fit width
   - Sort CohortMonth descending (newest at top)

4. **Add Visual Elements:**
   - Border: White, 2px width
   - Tooltip: Add cohort size and retention details
   - Title: "Customer Retention by Cohort and Month"

**Calculated Fields to Add:**

Create these calculated fields for enhanced insights:

```tableau
// Retention Category
IF [Retention Rate] >= 30 THEN "Excellent"
ELSEIF [Retention Rate] >= 20 THEN "Good"
ELSEIF [Retention Rate] >= 10 THEN "Fair"
ELSE "Poor"
END
```

**Pro Tips:**
- Add a reference line at 20% retention (industry benchmark)
- Highlight Month 0 (acquisition month) with a different border
- Use tooltips to show the actual number of retained customers

---

### Visualization 3: Customer Segmentation Pie/Donut Chart

**Purpose:** Show the distribution of customer types

**Data Source:** `segment_summary.csv`

**Steps:**

1. Create new worksheet: "Customer Segments"
2. Drag `Segment` to **Color** in Marks
3. Drag `CustomerCount` to **Angle**
4. Change mark type to **Pie**
5. Drag `Customer_%` to **Label**

6. **Format:**
   - Add segment names to labels
   - Use distinct colors (avoid red/green only for accessibility)
   - Format labels: **"Segment Name: XX%"**

7. **Create Donut Effect (Optional):**
   - Duplicate the sheet
   - Add a white circle in the center using a dual-axis trick:
     - Create a calculated field: `MIN(0)`
     - Drag to Rows, make dual axis
     - Change second mark to Circle
     - Increase size and make white

**Pro Tips:**
- Sort segments by size for easier reading
- Use the Tableau Blind-friendly color palette
- Add a filter to exclude segments with <1%

---

### Visualization 4: Repeat vs One-Time Buyers Comparison

**Purpose:** Clearly show the difference between customer types

**Data Source:** `customer_segmentation_analysis.csv`

**Steps:**

1. **Create Side-by-Side Bar Charts:**

   **Chart A - Customer Count:**
   - Worksheet: "Repeat vs One-Time - Count"
   - Drag `CustomerType` to **Columns**
   - Drag `COUNT([Customer_ID])` to **Rows**
   - Drag `CustomerType` to **Color**
   - Change to horizontal bars
   - Add labels with percentages

   **Chart B - Revenue:**
   - Worksheet: "Repeat vs One-Time - Revenue"
   - Same structure but use `SUM([TotalRevenue])`

2. **Create Comparison Dashboard:**
   - Create worksheet: "Buyer Comparison"
   - Use **dual-axis** or create a dashboard combining both

3. **Add Calculated Field for Insight:**
   ```tableau
   // Revenue per Customer
   SUM([TotalRevenue]) / COUNT([Customer_ID])
   ```

**Pro Tips:**
- Use contrasting colors (e.g., Blue for One-Time, Green for Repeat)
- Add a calculated text box showing "Repeat buyers spend Xx more"
- Include a breakdown by cohort using color

---

### Visualization 5: Revenue Trend Over Time

**Purpose:** Show monthly revenue patterns and growth

**Data Source:** `cohort_detailed_transactions.csv`

**Steps:**

1. Create worksheet: "Revenue Trend"
2. Drag `Date` to **Columns**
   - Change to continuous Month
3. Drag `SUM([TotalAmount])` to **Rows**
4. Change to **Area chart** or **Line chart**

5. **Add Segmentation:**
   - Drag `CustomerType` to **Color**
   - This creates a stacked area showing new vs repeat revenue

6. **Format:**
   - Smooth lines: Right-click chart → Format → Border → Round
   - Add trend line: Analytics → Trend Line
   - Color: Use a gradient (light to dark blue)

7. **Add Reference Band:**
   - Analytics → Reference Band
   - Show average revenue
   - Label: "Average Monthly Revenue"

**Calculated Field - Month-over-Month Growth:**
```tableau
// MoM Revenue Growth
(SUM([TotalAmount]) - LOOKUP(SUM([TotalAmount]), -1)) / LOOKUP(SUM([TotalAmount]), -1)
```

**Pro Tips:**
- Add forecast for next 3 months (Analytics → Forecast)
- Include annotations for peak months
- Use dual-axis to show both revenue and customer count trends

---

### Visualization 6: RFM Segmentation Scatter Plot

**Purpose:** Visualize customer value segments

**Data Source:** `rfm_customer_segmentation.csv`

**Steps:**

1. Create worksheet: "RFM Analysis"
2. Drag `F_Score` (Frequency) to **Columns**
3. Drag `M_Score` (Monetary) to **Rows**
4. Drag `R_Score` (Recency) to **Color**
5. Drag `TotalRevenue` to **Size**
6. Change mark type to **Circle**

7. **Format:**
   - Color: Diverging palette (Red-Yellow-Green)
   - Size range: Small to Large
   - Opacity: 70% (to see overlapping points)

8. **Add Quadrant Lines:**
   - Analytics → Reference Line
   - Add vertical line at median F_Score
   - Add horizontal line at median M_Score
   - Format as dashed gray lines

**Calculated Field - RFM Segment Label:**
```tableau
// RFM Quadrant
IF [F_Score] >= 3 AND [M_Score] >= 3 THEN "Champions"
ELSEIF [F_Score] >= 3 AND [M_Score] < 3 THEN "Loyal but Low Spend"
ELSEIF [F_Score] < 3 AND [M_Score] >= 3 THEN "High Value, Low Frequency"
ELSE "Needs Attention"
END
```

**Pro Tips:**
- Add RFM_Segment labels to color instead of R_Score for clearer segments
- Use tooltips to show customer details
- Filter out extreme outliers for better visualization

---

### Visualization 7: Cohort LTV Comparison

**Purpose:** Compare customer lifetime value across acquisition cohorts

**Data Source:** `cohort_ltv_analysis.csv`

**Steps:**

1. Create worksheet: "Cohort LTV"
2. Drag `CohortMonth` to **Columns**
3. Drag `AvgLTV` to **Rows**
4. Change to **Bar chart**

5. **Add Color Gradient:**
   - Drag `AvgLTV` to **Color**
   - Use sequential color palette (light to dark)

6. **Add Cohort Size Context:**
   - Drag `CohortSize` to **Size**
   - This makes bars thicker for larger cohorts

7. **Format:**
   - Sort by AvgLTV descending
   - Add data labels
   - Currency format for Y-axis

**Calculated Field - LTV vs Average:**
```tableau
// LTV Difference from Avg
[AvgLTV] - WINDOW_AVG([AvgLTV])
```

**Pro Tips:**
- Add a reference line for overall average LTV
- Use color to highlight top 3 cohorts
- Add a parameter to switch between AvgLTV and TotalRevenue

---

## 🎯 Dashboard Assembly & Best Practices

### Step 1: Create the Main Dashboard

1. Click **"Dashboard"** → **"New Dashboard"**
2. Name it: "E-Commerce Customer Analytics"
3. Set size: **Automatic** or **Desktop (1366 x 768)**

### Step 2: Layout Structure

**Header Section:**
1. Add a **Text object** for the title
   - Format: 24pt Bold, Dark Blue
   - Text: "E-Commerce Customer & Cohort Analytics"
   - Add subtitle with date range

2. Add **KPI Cards** in a horizontal container
   - Use floating containers for better positioning
   - Add subtle shadows (Border → Shadow)

**Main Content Area:**
1. Add **Cohort Retention Heatmap** (largest visualization)
   - Takes up ~40% of dashboard space

2. Add **Revenue Trend** (full width, below heatmap)

3. Two-column layout for:
   - Left: Customer Segmentation Pie Chart
   - Right: RFM Scatter Plot

4. Bottom section: Repeat vs One-Time comparison bars

### Step 3: Add Interactivity

**Global Filters:**
Create these filters and add to dashboard:

1. **Date Range Filter:**
   - Drag `Date` to Filters shelf
   - Select "Range of Dates"
   - Show filter → Range slider
   - Apply to all worksheets

2. **Cohort Filter:**
   - Drag `CohortMonth` to Filters
   - Show filter → Multiple values dropdown
   - Apply to cohort-specific sheets

3. **Country Filter:**
   - Drag `Country` to Filters
   - Show filter → Single value dropdown
   - Apply to all worksheets

**Dashboard Actions:**

1. **Highlight Action:**
   - Dashboard → Actions → Add Action → Highlight
   - Source: Any sheet
   - Target: All sheets
   - Hover: Show highlight

2. **Filter Action (Drill-down):**
   - Dashboard → Actions → Add Action → Filter
   - Source: "Customer Segments" pie chart
   - Target: All other sheets
   - Click on segment to filter entire dashboard

3. **URL Action (Optional):**
   - Link to customer details in external system
   - Dashboard → Actions → Add Action → URL
   - Use `<Customer_ID>` in URL string

### Step 4: Formatting for Stakeholder Presentation

**Color Consistency:**
- Use a consistent color palette across all visualizations
- Recommended: Blue for standard metrics, Green for positive/revenue, Orange for alerts

**Typography:**
- Titles: 14-16pt Bold
- Labels: 10-12pt Regular
- Tooltips: 9-10pt

**White Space:**
- Don't overcrowd! Leave breathing room
- Use containers with padding (5-10px)

**Accessibility:**
- Use colorblind-safe palettes
- Add patterns/shapes in addition to colors where possible
- Ensure text contrast ratio is at least 4.5:1

---

## 💡 Strategic Insights to Highlight

### Key Metrics to Emphasize:

1. **Cohort Performance:**
   - Highlight the best performing cohort
   - Show retention drop-off points
   - Identify at-risk cohorts

2. **Customer Value:**
   - Show repeat buyer revenue contribution (should be 90%+)
   - Display average order value by segment
   - Highlight Champions and Loyal Customers

3. **Growth Opportunities:**
   - Identify months with highest acquisition
   - Show which cohorts have best retention
   - Highlight segments with improvement potential

### Adding Insight Callouts:

Create **text boxes** with key insights:

```
💎 KEY INSIGHT:
Repeat buyers represent 72% of customers
but generate 97% of total revenue.

🎯 ACTION: Focus retention strategies
on first 3 months (largest drop-off period).
```

Position these strategically near relevant visualizations.

---

## 📊 Advanced Features

### Dynamic Parameters

**Create a Parameter for Metric Selection:**

1. **Create Parameter:**
   - Name: "Select Metric"
   - Data Type: String
   - Allowable Values: List
   - Values: "Revenue", "Customer Count", "Avg Order Value"

2. **Create Calculated Field:**
   ```tableau
   // Dynamic Metric
   CASE [Select Metric]
       WHEN "Revenue" THEN SUM([TotalAmount])
       WHEN "Customer Count" THEN COUNT(DISTINCT [Customer_ID])
       WHEN "Avg Order Value" THEN SUM([TotalAmount]) / COUNT([Invoice])
   END
   ```

3. **Use in Visualization:**
   - Replace fixed metrics with this calculated field
   - Show parameter control on dashboard

### Set Actions

**Create a Cohort Comparison Set:**

1. Create a Set from CohortMonth
2. Use Set Actions to select multiple cohorts
3. Create visualizations comparing selected cohorts

### Custom Calculated Fields Library

```tableau
// Customer Lifetime (Days)
{FIXED [Customer_ID]: DATEDIFF('day', MIN([InvoiceDate]), MAX([InvoiceDate]))}

// Days Since Last Purchase
DATEDIFF('day', {FIXED [Customer_ID]: MAX([InvoiceDate])}, TODAY())

// Customer Segment (Dynamic)
IF {FIXED [Customer_ID]: COUNT([Invoice])} = 1 THEN "One-Time"
ELSEIF {FIXED [Customer_ID]: COUNT([Invoice])} <= 3 THEN "Occasional"
ELSEIF {FIXED [Customer_ID]: COUNT([Invoice])} <= 10 THEN "Regular"
ELSE "Loyal"
END

// Revenue per Customer
{FIXED [Customer_ID]: SUM([TotalAmount])}

// Cohort Age (Months)
DATEDIFF('month', [CohortMonth], [InvoiceDate])

// Retention Rate
COUNT(DISTINCT IF [CohortIndex] = {FIXED: MAX([CohortIndex])}
              THEN [Customer_ID] END) /
COUNT(DISTINCT IF [CohortIndex] = 0
              THEN [Customer_ID] END)
```

---

## 🎨 Design Tips for Maximum Impact

### 1. Tell a Story
Structure your dashboard to guide viewers through insights:
- **Top:** "What" - Key metrics and current state
- **Middle:** "Why" - Deeper analysis and patterns
- **Bottom:** "How" - Specific segments and actionable insights

### 2. Use Visual Hierarchy
- Largest viz = Most important insight
- Use size, color intensity, and position to direct attention
- Group related visualizations with containers

### 3. Keep It Clean
- Remove unnecessary gridlines
- Hide field labels where obvious
- Use subtle backgrounds (not white, not dark - light gray works well)

### 4. Mobile Optimization (if needed)
- Create a mobile-specific dashboard layout
- Stack visualizations vertically
- Simplify to 3-4 key charts
- Larger touch targets for filters

### 5. Performance Optimization
- Extract data instead of Live connection for large datasets
- Use aggregated tables (the pre-computed CSVs)
- Limit number of marks (filter out small segments)
- Use Context Filters for faster interactivity

---

## ✅ Pre-Launch Checklist

Before presenting to stakeholders:

- [ ] All visualizations load in <3 seconds
- [ ] Filters affect all relevant sheets
- [ ] Tooltips are informative and formatted
- [ ] All numbers are properly formatted (currency, percentages)
- [ ] Color palette is consistent and accessible
- [ ] Dashboard title and metadata are present
- [ ] Date range is clearly displayed
- [ ] No misspellings in titles or labels
- [ ] Tested on target display resolution
- [ ] Exported/published with appropriate permissions
- [ ] Key insights are highlighted with annotations
- [ ] Dashboard actions work as expected

---

## 🚀 Presenting to Stakeholders

### Recommended Presentation Flow:

1. **Start with Overview (30 sec)**
   - Show KPI cards
   - State the time period covered
   - Mention data quality and completeness

2. **Deep Dive: Cohorts (2 min)**
   - Walk through the retention heatmap
   - Highlight best and worst performing cohorts
   - Explain the retention cliff (typically Month 1-3)

3. **Customer Segmentation (2 min)**
   - Show repeat vs one-time split
   - Emphasize the revenue concentration
   - Discuss implications for marketing spend

4. **Actionable Insights (1 min)**
   - RFM segments to target
   - Cohorts needing intervention
   - Opportunities for growth

5. **Q&A and Exploration**
   - Use filters to answer specific questions
   - Drill into interesting patterns
   - Discuss next steps

### Stakeholder-Specific Views:

**For C-Suite:**
- Focus on KPIs and high-level trends
- Revenue impact and ROI
- Strategic recommendations

**For Marketing:**
- Cohort performance by acquisition channel
- Retention rates and drop-off points
- Customer lifetime value by segment

**For Product:**
- Purchase frequency patterns
- Product affinity by segment
- Customer journey touchpoints

---

## 📚 Additional Resources

### Tableau Tips:
- Use Ctrl+Click to multi-select data points
- Double-click to automatically create views
- Use Table Calculations for quick ratio comparisons

### Data Refresh:
- Rerun Python scripts monthly/weekly
- Use Tableau's scheduled extract refresh (Server/Cloud)
- Version control your data sources

### Further Enhancements:
- Add predictive analytics (churn probability)
- Include seasonal decomposition
- Integrate with CRM data for full customer view
- Add cohort comparison what-if scenarios

---

## 🎯 Success Metrics for Your Dashboard

A great dashboard should:

1. ✅ Answer 3-5 key business questions immediately
2. ✅ Load in under 3 seconds
3. ✅ Be understandable without explanation
4. ✅ Enable users to explore and find their own insights
5. ✅ Drive specific, measurable actions

---

## 🆘 Troubleshooting Common Issues

**Issue: Retention rates show >100%**
- **Cause:** Customers from earlier cohorts counted in later cohorts
- **Fix:** Ensure CohortMonth is calculated from FIRST purchase date only

**Issue: Heatmap is too sparse**
- **Cause:** Not enough data in recent cohorts
- **Fix:** Filter to show only cohorts with >100 customers

**Issue: Dashboard is slow**
- **Cause:** Too many marks, live connection, or complex calculations
- **Fix:** Use extracts, pre-aggregate data, limit date range

**Issue: Colors are confusing**
- **Cause:** Inconsistent or too many colors
- **Fix:** Create a color style guide, limit to 5-7 colors max

---

## 📊 Final Dashboard Snapshot

Your completed dashboard should look clean, professional, and insight-driven. Here's what success looks like:

**Top Section:**
```
[Total Revenue: $17.4M]  [Total Customers: 5,878]  [Avg LTV: $1,869]  [Retention: 72%]
```

**Main Visualizations:**
- Large cohort heatmap showing clear retention patterns
- Revenue trend with clear upward or seasonal patterns
- Customer segment pie/donut with clear labels
- RFM scatter showing distinct customer clusters

**Bottom Section:**
- Clear comparison showing repeat buyers drive 97% of revenue
- Actionable insights highlighted in text boxes

---

## 🎉 Conclusion

This dashboard will help stakeholders:
- **Understand** customer behavior patterns
- **Identify** high-value customer segments
- **Optimize** marketing and retention strategies
- **Track** cohort performance over time
- **Make** data-driven decisions

Remember: A dashboard is only as good as the actions it drives. Always tie your visualizations back to business outcomes and strategic decisions.

**Good luck building your dashboard!** 🚀

---

*Need help? Check the Tableau Community or reach out to the Analytics Team.*
