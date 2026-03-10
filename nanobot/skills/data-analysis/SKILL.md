---
name: data-analysis
description: "Analyze CSV, JSON, Excel files with Python pandas. Generate insights, charts, and reports."
metadata: {"nanobot":{"emoji":"📊","requires":{"bins":["python3"]},"python_packages":["pandas","numpy","matplotlib"]}}
---

# Data Analysis Skill

Analyze data files using Python pandas and generate insights.

## Quick Analysis

### Load and Preview Data
```python
import pandas as pd

# Load CSV
df = pd.read_csv('data.csv')

# Load Excel
df = pd.read_excel('data.xlsx')

# Load JSON
df = pd.read_json('data.json')

# First rows
print(df.head())

# Summary
print(df.info())
print(df.describe())
```

### Basic Statistics
```python
# Column statistics
print(df['column'].mean())
print(df['column'].median())
print(df['column'].std())
print(df['column'].min(), df['column'].max())

# Value counts
print(df['category'].value_counts())

# Correlation
print(df.corr())
```

## Data Exploration

### Check Data Quality
```python
# Missing values
print(df.isnull().sum())

# Duplicate rows
print(f"Duplicates: {df.duplicated().sum()}")

# Unique values
print(df.nunique())

# Data types
print(df.dtypes)
```

### Filter and Query
```python
# Filter rows
filtered = df[df['sales'] > 1000]

# Multiple conditions
filtered = df[(df['sales'] > 1000) & (df['region'] == 'North')]

# Query syntax
filtered = df.query('sales > 1000 and region == "North"')

# Select columns
subset = df[['name', 'sales', 'date']]
```

## Data Transformation

### GroupBy Analysis
```python
# Group and aggregate
grouped = df.groupby('category')['sales'].sum()

# Multiple aggregations
grouped = df.groupby('region').agg({
    'sales': ['sum', 'mean', 'count'],
    'profit': 'mean'
})

# Group by multiple columns
grouped = df.groupby(['region', 'category'])['sales'].sum()
```

### Add/Modify Columns
```python
# New column
df['profit_margin'] = df['profit'] / df['sales']

# Apply function
df['name_upper'] = df['name'].apply(str.upper)

# Conditional column
df['status'] = df['sales'].apply(lambda x: 'High' if x > 1000 else 'Low')

# Date extraction
df['year'] = pd.to_datetime(df['date']).dt.year
df['month'] = pd.to_datetime(df['date']).dt.month
```

### Merge and Join
```python
# Merge DataFrames
merged = pd.merge(df1, df2, on='id', how='inner')

# Concatenate
combined = pd.concat([df1, df2], axis=0)

# Join on index
joined = df1.join(df2, lsuffix='_left', rsuffix='_right')
```

## Visualization

### Basic Plots
```python
import matplotlib.pyplot as plt

# Line chart
df.plot(x='date', y='sales', kind='line', title='Sales Over Time')
plt.savefig('sales_trend.png')

# Bar chart
df['category'].value_counts().plot(kind='bar')
plt.savefig('categories.png')

# Histogram
df['sales'].plot(kind='hist', bins=20)
plt.savefig('sales_dist.png')

# Scatter plot
df.plot(x='advertising', y='sales', kind='scatter')
plt.savefig('scatter.png')

# Box plot
df.boxplot(column='sales', by='region')
plt.savefig('boxplot.png')
```

### Advanced Charts
```python
# Heatmap (correlation)
import seaborn as sns
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.savefig('correlation.png')

# Pie chart
df['category'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.savefig('pie.png')

# Area chart
df.plot(x='date', y=['product_a', 'product_b'], kind='area', stacked=True)
plt.savefig('area.png')
```

## Export Results

### Save to File
```python
# To CSV
df.to_csv('output.csv', index=False)

# To Excel
df.to_excel('output.xlsx', index=False, sheet_name='Results')

# To JSON
df.to_json('output.json', orient='records', indent=2)

# To Markdown table
print(df.head().to_markdown(index=False))
```

## Complete Analysis Script

```python
import pandas as pd
import matplotlib.pyplot as plt

def analyze_sales_data(filepath):
    """Complete sales data analysis."""
    # Load
    df = pd.read_csv(filepath)
    
    # Summary report
    report = []
    report.append(f"Records: {len(df)}")
    report.append(f"Columns: {len(df.columns)}")
    report.append(f"\nMissing values:\n{df.isnull().sum()}")
    report.append(f"\nSales Summary:\n{df['sales'].describe()}")
    
    # Group by region
    region_sales = df.groupby('region')['sales'].agg(['sum', 'mean', 'count'])
    report.append(f"\nSales by Region:\n{region_sales}")
    
    # Top products
    top_products = df.groupby('product')['sales'].sum().nlargest(10)
    report.append(f"\nTop 10 Products:\n{top_products}")
    
    # Save report
    with open('analysis_report.txt', 'w') as f:
        f.write('\n'.join(report))
    
    # Create charts
    df.plot(x='date', y='sales', kind='line')
    plt.savefig('sales_trend.png')
    
    return "Analysis complete! See analysis_report.txt and charts."

# Run
analyze_sales_data('sales_data.csv')
```

## CLI One-Liners

```bash
# CSV stats with Python
python -c "import pandas as pd; df=pd.read_csv('data.csv'); print(df.describe())"

# Count rows
python -c "import pandas as pd; print(len(pd.read_csv('data.csv')))"

# Column names
python -c "import pandas as pd; print(', '.join(pd.read_csv('data.csv').columns))"

# Filter and save
python -c "import pandas as pd; df=pd.read_csv('data.csv'); df[df['sales']>1000].to_csv('filtered.csv', index=False)"
```

## Tips

- Use `df.sample(5)` to see random rows
- `df.memory_usage(deep=True)` to check memory
- Use chunks for large files: `pd.read_csv('large.csv', chunksize=10000)`
- Cache results with `df.to_parquet()` for faster loading
- Use `df.style` for nice HTML tables in Jupyter
