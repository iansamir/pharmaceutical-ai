import pandas as pd 

df = pd.read_csv("adsl_sample.csv")
df.rename(columns={"TRTPN": "Treatment"}, inplace=True)
df.rename(columns={"USUBJID": "Subject ID"}, inplace=True)
grouped_data = df.groupby("Treatment")

for group_name, group_df in grouped_data: 
    print("\n", group_name, "\n")
    print(group_df) 

print("\n\n")