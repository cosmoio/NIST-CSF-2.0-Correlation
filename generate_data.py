import pandas as pd
import numpy as np

def generate_synthetic_nist_data(filename='data/synthetic_nist_ratings.csv'):
    # Load structure from nist.csv
    # Assumes nist.csv is in the data folder and has columns: Function, Category, Subcategory
    # We need to parse the Category and Subcategory columns to get the codes (e.g., GV.OC from "Organizational Context (GV.OC)...")
    
    nist_df = pd.read_csv('data/nist.csv')
    
    # Helper to extract code from text (e.g., "GV.OC" from "Organizational Context (GV.OC)...")
    def extract_code(text):
        if pd.isna(text): return ""
        # Look for pattern like (XX.YY) or XX.YY-01
        import re
        # For Category: "Name (CODE): Description" -> extract CODE
        cat_match = re.search(r'\(([A-Z]{2}\.[A-Z]{2})\)', text)
        if cat_match:
            return cat_match.group(1)
            
        # For Subcategory: "CODE-01: Description" -> extract CODE-01
        sub_match = re.search(r'^([A-Z]{2}\.[A-Z]{2}-\d{2})', text)
        if sub_match:
            return sub_match.group(1)
            
        return text

    data = []
    np.random.seed(42) # Fixed seed for reproducibility

    for _, row in nist_df.iterrows():
        func = row['Function']
        cat_text = row['Category']
        sub_text = row['Subcategory']
        
        cat_code = extract_code(cat_text)
        sub_code = extract_code(sub_text)
        
        # If extraction failed, fallback to raw text or skip
        if not sub_code:
            continue
            
        # Use the extracted codes
        data_row = {
            'Function': func,
            'Category': cat_code,
            'Subcategory': sub_code,
        }
        
        # Generate random ratings (0-6) for 6 Managers
        base_maturity = np.random.randint(0,8) 
        
        managers = ["Alice", "Bob", "Craig", "Carol", "Dave", "Frank"]
        for m in range(1, 7):
            # Manager rating is base_maturity +/- noise
            noise = np.random.randint(-1, 1) 
            rating = (base_maturity + noise) % 6
            
            
            # Make Dave an outlier
            if "Dave" in managers[m-1]:
                noise = np.random.randint(-1, 1) 
                rating = np.clip(base_maturity + noise, 5, 7)
            data_row[managers[m-1]] = rating
        
        data.append(data_row)

    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    df.to_csv(filename, index=False)
    print(f"Successfully generated {len(df)} rows of synthetic data at: {filename}")
    print(df.head())

if __name__ == "__main__":
    import signal
    import sys

    def signal_handler(sig, frame):
        print('\nProcess cancelled by user (Ctrl+C). Exiting...')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # Ensure directory exists if needed, or just save to root
    import os
    if not os.path.exists('data'):
        os.makedirs('data')
        
    generate_synthetic_nist_data()
