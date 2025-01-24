import pandas as pd
from scipy.stats import ttest_ind, chi2_contingency

# Example dataset
data = pd.read_csv("adsl_sample.csv")
# Create a DataFrame
df = pd.DataFrame(data)
print("\nData \n")
print(df) 

# Compute summary for Age (Numerical)
def age_summary(df):
    groups = df.groupby("TRTPN")["AGE"]
    summary = {
        "N": groups.size(),
        "Mean": groups.mean(),
        "Std Dev": groups.std(),
    }
    overall = {
        "N": df["AGE"].count(),
        "Mean": df["AGE"].mean(),
        "Std Dev": df["AGE"].std(),
    }
    p_value = ttest_ind(
        df[df["TRTPN"] == "Active"]["AGE"],
        df[df["TRTPN"] == "Placebo"]["AGE"]
    )[1]
    summary_df = pd.DataFrame(summary).T
    summary_df["Overall"] = overall.values()
    summary_df["P-value"] = [p_value] * 1 + [None] * (len(summary_df) - 1)  # Only first row gets p-value
    return summary_df

# Compute summary for categorical variables
def categorical_summary(df, column):
    counts = pd.crosstab(df[column], df["TRTPN"], normalize="columns") * 100
    counts["Overall"] = df[column].value_counts(normalize=True) * 100
    chi2, p_value, _, _ = chi2_contingency(pd.crosstab(df[column], df["TRTPN"]))
    counts["P-value"] = [p_value] + [None] * (len(counts) - 1)  # Only first row gets p-value
    return counts

# Generate summaries
age_summary_table = age_summary(df)
sex_summary_table = categorical_summary(df, "SEX")
race_summary_table = categorical_summary(df, "RACE")

# Combine results into a single summary table
summary_table = pd.concat(
    [age_summary_table, sex_summary_table, race_summary_table],
    keys=["Age (Years)", "Sex", "Race"]
)

# Display the summary table
print("\nSummary Table \n")
print(summary_table)
print("\n")