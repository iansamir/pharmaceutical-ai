import pandas as pd
import numpy as np

def create_random_data(num_rows=1000):
    # Seed for reproducibility
    np.random.seed(42)
    
    # Generate random values for the columns
    aval = np.random.randint(0, 2, size=num_rows)  # Random binary outcomes (0 or 1)
    
    # Generate random treatment groups (TRTPN)
    trtpn = np.random.choice([0, 1, 2], size=num_rows)  # Random treatment groups (0, 1, 2)
    
    # Generate random sex values (SEX)
    sex = np.random.choice([1, 2], size=num_rows)  # Random sex values (1, 2)
    
    # Generate random race values (RACE)
    race = np.random.choice([0, 1], size=num_rows)  # Random race values (0, 1)
    
    # Generate random baseline pain values (BASEPAIN)
    basepain = np.random.randint(20, 80, size=num_rows)  # Random baseline pain (between 20 and 80)
    
    # Create DataFrame
    data = pd.DataFrame({
        'AVAL': aval,
        'TRTPN': trtpn,
        'SEX': sex,
        'SEX_N': np.random.randint(18, 60, size=num_rows),  # Age or another numerical value for SEX_N
        'RACE': race,
        'RACE_N': np.random.randint(1, 5, size=num_rows),  # Random value for RACE_N
        'BASEPAIN': basepain
    })
    
    # Save to CSV
    data.to_csv('sample_data/forest_sample.csv', index=False)
    print("Random data generated and saved to 'random_data.csv'.")

# Call the function to generate the data
create_random_data(num_rows=5000)  # Change num_rows to generate more or less data