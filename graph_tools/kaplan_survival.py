import pandas as pd
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt

def create_kaplan_survival_plot(): 
    # Read the CSV file
    data = pd.read_csv("sample_data/kaplan_survival_data.csv")

    # Initialize the Kaplan-Meier estimator
    kmf = KaplanMeierFitter()

    # Plot Kaplan-Meier curves for each treatment group
    plt.figure(figsize=(10, 6))
    for treatment in data["TRTP"].unique():
        # Filter data for the specific treatment group
        treatment_data = data[data["TRTP"] == treatment]
        
        # Fit the Kaplan-Meier model
        average_month_days = 365.25/12 
        kmf.fit(treatment_data["AVAL"] / average_month_days, event_observed=1 - treatment_data["CNSR"], label=treatment) 
        
        # Plot the survival function
        kmf.plot_survival_function()

    # Add labels and title
    plt.title("Kaplan-Meier Survival Estimates")
    plt.xlabel("Months from Randomization")
    plt.ylabel("Survival Probability")
    plt.legend(title="Treatment")
    plt.grid(True)
    plt.show()