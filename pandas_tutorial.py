import pandas as pd
import numpy as np

# setup: Create a dummy dataset for demonstration
data = {
    "Name": ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace"],
    "Age": [25, 30, 35, 28, 40, 22, 50],
    "Department": ["HR", "Engineering", "Engineering", "Sales", "HR", "IT", "Sales"],
    "Salary": [50000, 80000, 90000, 60000, 55000, 70000, 100000],
}

# Save as dummy CSV for this script to read
pd.DataFrame(data).to_csv("sample_data.csv", index=False)

# Read CSV/Excel into DataFrame
print("------- Reading Data Start ------- ")
df = pd.read_csv("sample_data.csv")

# Inspect head/tail/types
print("\n--- Inspecting Data ---")
print("Head:\n", df.head(3))

print("\nTail:\n", df.tail(2))

print("\nData Types:\n", df.dtypes)

print("\nDataFrame Info:")
df.info()

print("------- Reading Data End -------")

# Compute summary stats (mean, median, min, max, count)
print("\n--- Summary Statistics ---")

print(f"Mean:   {df['Salary'].mean()}")
print(f"Median: {df['Salary'].median()}")
print(f"Min:    {df['Salary'].min()}")
print(f"Max:    {df['Salary'].max()}")
print(f"Count:  {df['Salary'].count()}")

# Filter rows, select columns and slice subsets
print("\n--- Filtering and Slicing ---")

print("\nsingle column:\n", df["Name"].head(3))
subset_cols = df[["Name", "Salary"]]
print("\nmultiple columns:\n", subset_cols.head(3))

filtered_rows = df[df["Age"] > 30]
print("\nFilter rows (Age > 30):\n", filtered_rows)

complex_filter = df[(df["Age"] > 25) & (df["Department"] == "Engineering")]
print("\nComplex Filter (Age > 25 & Dept=Engineering):\n", complex_filter)

print("\nSlice rows index 2 to 4 using iloc:\n", df.iloc[2:5])
print(
    "\nSlice specific rows and columns using loc:\n",
    df.loc[2:4, ["Name", "Department"]],
)

print("------- Filtering and Slicing End -------")

# Save filtered results to CSV/Excel
print("\n--- Saving Results ---")

# Save to CSV
filtered_rows.to_csv("filtered_results.csv", index=False)
print("Saved filtered results to 'filtered_results.csv'")

# Save to Excel
filtered_rows.to_excel("filtered_results.xlsx", index=False)
print("Saved filtered results to 'filtered_results.xlsx'")

print("------- Saving Results End -------")
