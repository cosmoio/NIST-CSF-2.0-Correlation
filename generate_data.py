import pandas as pd
import numpy as np

def generate_synthetic_nist_data(filename='data/synthetic_nist_ratings.csv'):
    # NIST CSF 2.0 Structure (Functions and their Category Codes)
    structure = {
        'GOVERN': ['GV.OC', 'GV.RM', 'GV.RR', 'GV.PO', 'GV.OV', 'GV.SC'],
        'IDENTIFY': ['ID.AM', 'ID.RA', 'ID.IM'],
        'PROTECT': ['PR.AA', 'PR.AT', 'PR.DS', 'PR.PS', 'PR.IR'],
        'DETECT': ['DE.CM', 'DE.AE'],
        'RESPOND': ['RS.MA', 'RS.AN', 'RS.CO', 'RS.MI'],
        'RECOVER': ['RC.RP', 'RC.CO']
    }

    data = []
    
    # Generate subcategories for each Category
    # (Simulating roughly 3-5 subcategories per category)
    np.random.seed(42) # Fixed seed for reproducibility
    
    for function, categories in structure.items():
        for cat in categories:
            # Randomly decide how many subcategories this category has (3 to 6)
            num_subcats = np.random.randint(3, 7)
            
            for i in range(1, num_subcats + 1):
                subcategory_code = f"{cat}-{i:02d}" # e.g., GV.OC-01
                
                row = {
                    'Function': function,
                    'Category': cat,
                    'Subcategory': subcategory_code,
                }
                
                # Generate random ratings (1-6) for 6 Managers
                # We add some "bias" to make the correlation interesting (not purely random noise)
                # e.g., Managers roughly agree on the "true" maturity but vary by +/- 1
                base_maturity = np.random.randint(2, 6) 
                
                for m in range(1, 7):
                    # Manager rating is base_maturity +/- noise
                    noise = np.random.randint(-1, 2)
                    rating = np.clip(base_maturity + noise, 1, 6)
                    row[f'Manager_{m}'] = rating
                
                data.append(row)

    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    df.to_csv(filename, index=False)
    print(f"Successfully generated {len(df)} rows of synthetic data at: {filename}")
    print(df.head())

if __name__ == "__main__":
    # Ensure directory exists if needed, or just save to root
    import os
    if not os.path.exists('data'):
        os.makedirs('data')
        
    generate_synthetic_nist_data()