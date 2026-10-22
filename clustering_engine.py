import os
import joblib
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def perform_route_clustering(df, n_clusters=4, output_dir="models"):
    os.makedirs(output_dir, exist_ok=True)
    
    # Define route by Origin Factory, Region, and Ship Mode
    route_grouped = df.groupby(['Origin Factory', 'Region', 'Ship Mode']).agg(
        order_count=('Row ID', 'count'),
        avg_distance_km=('Distance_km', 'mean'),
        avg_lead_time=('Operational_Lead_Time', 'mean'),
        total_units=('Units', 'sum'),
        avg_units=('Units', 'mean'),
        total_sales=('Sales', 'sum'),
        total_profit=('Gross Profit', 'sum'),
        avg_profit_margin=('Profit_Margin', 'mean')
    ).reset_index()
    
    # Feature matrix for clustering
    cluster_features = ['avg_distance_km', 'avg_lead_time', 'avg_units', 'avg_profit_margin', 'order_count']
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(route_grouped[cluster_features])
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    route_grouped['Cluster'] = kmeans.fit_predict(scaled_data)
    
    # Meaningful cluster labels based on centroids
    cluster_profiles = {}
    for c in range(n_clusters):
        c_df = route_grouped[route_grouped['Cluster'] == c]
        mean_dist = c_df['avg_distance_km'].mean()
        mean_lt = c_df['avg_lead_time'].mean()
        order_vol = c_df['order_count'].sum()
        
        if mean_lt > 5.0 and mean_dist > 2500:
            label = "Severe Cross-Country Friction"
            severity = "High"
            action = "Primary candidate for regional factory reallocation"
        elif mean_lt > 4.5:
            label = "Moderate Lead-Time Bottleneck"
            severity = "Medium"
            action = "Evaluate factory switch or expedited logistics"
        elif order_vol > 2000:
            label = "High-Volume Core Lanes"
            severity = "Low"
            action = "Maintain dedicated batch production"
        else:
            label = "Optimal Low-Friction Routes"
            severity = "Low"
            action = "Sustain current operational parameters"
            
        cluster_profiles[c] = {
            'label': label,
            'severity': severity,
            'action': action,
            'avg_distance_km': round(float(mean_dist), 1),
            'avg_lead_time': round(float(mean_lt), 2),
            'route_count': int(len(c_df)),
            'total_orders': int(order_vol)
        }
    
    route_grouped['Cluster_Label'] = route_grouped['Cluster'].map(lambda c: cluster_profiles[c]['label'])
    route_grouped['Severity'] = route_grouped['Cluster'].map(lambda c: cluster_profiles[c]['severity'])
    route_grouped['Action'] = route_grouped['Cluster'].map(lambda c: cluster_profiles[c]['action'])
    
    # Identify top congested region-product combinations
    product_region_friction = df.groupby(['Product Name', 'Region', 'Origin Factory']).agg(
        orders=('Row ID', 'count'),
        avg_lead_time=('Operational_Lead_Time', 'mean'),
        avg_distance_km=('Distance_km', 'mean'),
        total_profit=('Gross Profit', 'sum')
    ).reset_index()
    
    product_region_friction['Congestion_Score'] = (
        (product_region_friction['avg_lead_time'] / product_region_friction['avg_lead_time'].max()) * 0.6 +
        (product_region_friction['avg_distance_km'] / product_region_friction['avg_distance_km'].max()) * 0.4
    ) * 100
    
    product_region_friction = product_region_friction.sort_values(by='Congestion_Score', ascending=False)
    
    # Save clustering model and results
    joblib.dump(kmeans, os.path.join(output_dir, "route_clusters_kmeans.joblib"))
    joblib.dump(scaler, os.path.join(output_dir, "route_clusters_scaler.joblib"))
    route_grouped.to_csv(os.path.join(output_dir, "route_clusters.csv"), index=False)
    product_region_friction.to_csv(os.path.join(output_dir, "product_region_friction.csv"), index=False)
    
    print("[SUCCESS] Route and product clustering completed.")
    return route_grouped, product_region_friction, cluster_profiles

if __name__ == "__main__":
    df = pd.read_csv("nassau_candy_enriched.csv")
    perform_route_clustering(df)
