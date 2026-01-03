import pandas as pd
import numpy as np

DATA_FILE = r"final_data_with_coords.csv" 

def load_data():
    try:
        df = pd.read_csv(DATA_FILE)
        return df
    except FileNotFoundError:
        print(f"Error: Could not find '{DATA_FILE}' in the current directory.")

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)
    a = np.sin(dphi/2)**2 + np.cos(phi1)*np.cos(phi2)*np.sin(dlambda/2)**2
    return 2 * R * np.arctan2(np.sqrt(a), np.sqrt(1-a))

def recommend_weekend_trip(df, source_city,k=5):
    source_city = source_city.title()
    if source_city not in df['City'].values:
        return "City not found in database."

    source_row = df[df['City'] == source_city].iloc[0]
    s_lat, s_lon = source_row['Latitude'], source_row['Longitude']

    df['Distance_km'] = haversine(s_lat, s_lon, df['Latitude'], df['Longitude'])

    recommendations = df[
        (df['Distance_km'] > 0) & 
        (df['Distance_km'] <= 250)
    ].copy()
    recommendations['Final_Rank'] = recommendations['Google review rating'] * 0.7 + \
                                    (1 / (recommendations['Distance_km'] + 1)) * 0.3

    return recommendations.sort_values('Final_Rank', ascending=False)[['City', 'Name', 'Distance_km', 'Type', 'Google review rating']].head(k)

def main():
    df = load_data()
    
    while True:
        city = input("\nEnter your current city (or 'q' to quit): ")
        
        if city.lower() in ['q', 'quit', 'exit']:
            break
            
        results = recommend_weekend_trip(df, city)
        
        if results is not None:
            print(f"\nTop 10 Weekend Getaways from {city.title()}:\n")
            results['Distance_km'] = results['Distance_km'].round(1)
            print(results.to_string(index=False))

if __name__ == "__main__":
    main()
