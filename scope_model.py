
import pandas as pd
from sklearn.linear_model import LinearRegression
import argparse

def load_data(file_path):
    return pd.read_csv(file_path)

def process_data(df):
    # Group the data by item name and calculate total for each relevant feature
    return df.groupby('Item name').agg({
        'Items viewed': 'sum',
        'Items added to cart': 'sum',
        'Items purchased': 'sum'
    }).reset_index()

def run_model(item_stats):
    X = item_stats[['Items viewed', 'Items added to cart']]
    y = item_stats['Items purchased']
    
    model = LinearRegression()
    model.fit(X, y)
    
    item_stats['Predicted purchases'] = model.predict(X)
    item_stats['Potential additional sales'] = item_stats['Predicted purchases'] - item_stats['Items purchased']
    return item_stats

def export_results(item_stats, output_file):
    top_250_items = item_stats[['Item name', 'Items purchased', 'Predicted purchases', 'Potential additional sales']].sort_values(by='Potential additional sales', ascending=False).head(250)
    top_250_items.to_csv(output_file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run SCOPE model for sales predictions')
    parser.add_argument('--input', type=str, required=True, help='Path to input CSV file')
    parser.add_argument('--output', type=str, required=True, help='Path to output CSV file')
    
    args = parser.parse_args()
    
    df = load_data(args.input)
    item_stats = process_data(df)
    item_stats = run_model(item_stats)
    export_results(item_stats, args.output)

    print(f"Results exported to {args.output}")
