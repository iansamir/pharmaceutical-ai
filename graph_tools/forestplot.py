# forestplot.py 
# Need to fix axis labels, ensure generality. 

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

def create_forest_plot(csv_file="sample_data/forest_sample.csv"):
    # Read the CSV data
    data = pd.read_csv(csv_file)
    
    # Convert categorical variables to proper format for regression
    data['TRTPN'] = data['TRTPN'].astype('category')
    data['SEX'] = data['SEX'].astype('category')
    data['RACE'] = data['RACE'].astype('category')
    
    # Check if AVAL has enough variation (not just 0 or 1)
    if data['AVAL'].nunique() <= 1:
        print("AVAL has insufficient variation (only one class). Logistic regression may not work.")
        return

    # Define the columns for analysis, treating BASEPAIN separately
    categorical_categories = ["TRTPN", "SEX", "RACE"]
    continuous_categories = ["BASEPAIN"]
    results = []

    # Create mappings for categorical variable labels
    category_labels = {
        'SEX': {0: 'Female', 1: 'Male'},  # Ensure these match exactly what your data contains
        'RACE': {1: 'White', 2: 'Black', 3: 'Other'},  # Adjust as per your actual data
        'TRTPN': {0: 'Placebo', 1: 'Active Therapy'}  # Same for TRTPN
    }

    # Logistic regression to calculate odds ratios for categorical variables
    for category in categorical_categories:
        formula = f"AVAL ~ C({category})"
        
        try:
            # Fit the logistic regression model with regularization
            model = smf.logit(formula, data=data).fit(method='lbfgs', disp=0)
            
            odds_ratios = np.exp(model.params)  # Calculate odds ratios for all params
            conf = model.conf_int()  # Get confidence intervals

            # Only extract odds ratios for the categorical variables (ignore intercept)
            for param in model.params.index:
                if param.startswith('C('):  # Skip intercept and only consider categorical variables
                    odds_ratio = odds_ratios[param]
                    conf_odds = np.exp(conf.loc[param])  # Convert to odds ratio scale

                    # Get the label for the categorical variable
                    category_name = param.split('[')[0][2:]  # Extract the variable name from the parameter (e.g., "C(TRTPN)")
                    labels = category_labels.get(category_name, {})

                    # Case where we have multiple levels like [T.1] for 'Active Therapy'
                    if '[' in param:  
                        level = param.split('[')[1].split(']')[0]  # Extract level (e.g., "T.1")
                        level_num = int(level.split('.')[1])  # Get numeric level (e.g., "1" or "2")
                        
                        # Ensure correct label retrieval
                        level_label = labels.get(level_num, "Unknown")
                        results.append({
                            "Category": f"{category_name}: {level_label}",
                            "Odds Ratio": odds_ratio,
                            "Lower CI": conf_odds[0],
                            "Upper CI": conf_odds[1]
                        })

        except Exception as e:
            print(f"Error with {category}: {e}")
    
    # Logistic regression to calculate odds ratio for continuous variables
    for category in continuous_categories:
        formula = f"AVAL ~ {category}"
        
        try:
            # Fit the logistic regression model for continuous variable
            model = smf.logit(formula, data=data).fit(method='lbfgs', disp=0)
            
            odds_ratios = np.exp(model.params)  # Calculate odds ratios for all params
            conf = model.conf_int()  # Get confidence intervals

            # Extract odds ratio and confidence interval for continuous variable
            odds_ratio = odds_ratios[category]
            conf_odds = np.exp(conf.loc[category])  # Convert to odds ratio scale

            # Add result to the list for continuous variable (BASEPAIN)
            results.append({
                "Category": f"{category} (Continuous)",
                "Odds Ratio": odds_ratio,
                "Lower CI": conf_odds[0],
                "Upper CI": conf_odds[1]
            })

        except Exception as e:
            print(f"Error with {category}: {e}")

    # Check if results were collected
    if not results:
        print("No valid results to plot.")
        return

    # Convert results to a DataFrame
    results_df = pd.DataFrame(results)

    # Create the forest plot
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot the odds ratios and confidence intervals
    y_positions = range(len(results_df))
    ax.errorbar(
        results_df["Odds Ratio"],
        y_positions,
        xerr=[
            results_df["Odds Ratio"] - results_df["Lower CI"],
            results_df["Upper CI"] - results_df["Odds Ratio"]
        ],
        fmt="o",
        color="black",
        capsize=5,
        label="95% CI"
    )

    # Add vertical line at odds ratio = 1
    ax.axvline(1, color="red", linestyle="--", label="Odds Ratio = 1")

    # Set y-axis labels and ticks
    ax.set_yticks(y_positions)
    ax.set_yticklabels(results_df["Category"])
    ax.set_xlabel("Odds Ratio")
    ax.set_title("Forest Plot: Odds Ratios with 95% CI")
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)
    ax.legend()

    # Show plot
    plt.tight_layout()
    plt.show()

# Run the function
create_forest_plot()