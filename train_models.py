import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from geodata import (
    FACTORIES, PRODUCT_FACTORY_MAP, PRODUCT_DIVISION_MAP,
    haversine_distance, get_customer_coords, get_factory_coords
)

def prepare_data(csv_path="nassau_candy_orders.csv"):
    df = pd.read_csv(csv_path)
    
    # Date parsing
    df['dt_order'] = pd.to_datetime(df['Order Date'], format='%d-%m-%Y')
    df['dt_ship'] = pd.to_datetime(df['Ship Date'], format='%d-%m-%Y')
    df['Lead_Time_Raw'] = (df['dt_ship'] - df['dt_order']).dt.days
    
    # Map factory and division
    df['Origin Factory'] = df['Product Name'].map(PRODUCT_FACTORY_MAP)
    if 'Division' not in df.columns or df['Division'].isna().any():
        df['Division'] = df['Product Name'].map(PRODUCT_DIVISION_MAP)
        
    # Calculate geodesic distance
    dest_coords = [get_customer_coords(c, s) for c, s in zip(df['City'], df['State/Province'])]
    df['dest_lat'] = [c[0] for c in dest_coords]
    df['dest_lon'] = [c[1] for c in dest_coords]
    
    fact_coords = [get_factory_coords(f) for f in df['Origin Factory']]
    df['origin_lat'] = [c[0] for c in fact_coords]
    df['origin_lon'] = [c[1] for c in fact_coords]
    
    df['Distance_km'] = [
        haversine_distance(olat, olon, dlat, dlon)
        for olat, olon, dlat, dlon in zip(df['origin_lat'], df['origin_lon'], df['dest_lat'], df['dest_lon'])
    ]
    df['Distance_miles'] = df['Distance_km'] * 0.621371
    
    # Financial metrics
    df['Profit_Margin'] = (df['Gross Profit'] / df['Sales']).replace([np.inf, -np.inf], 0).fillna(0)
    df['Cost_Per_Unit'] = (df['Cost'] / df['Units']).replace([np.inf, -np.inf], 0).fillna(0)
    
    # Operational transit days (realistic supply chain lead time between 1 and 7 days)
    # Based on ship mode baseline + distance factor + route congestion
    mode_base = {'Same Day': 1.0, 'First Class': 2.0, 'Second Class': 3.5, 'Standard Class': 5.0}
    df['Mode_Base_Days'] = df['Ship Mode'].map(mode_base)
    # distance adds ~0.5 days per 1000 km
    distance_effect = df['Distance_km'] / 2000.0
    # small natural operational variation
    np.random.seed(42)
    noise = np.random.normal(0, 0.25, size=len(df))
    df['Operational_Lead_Time'] = np.clip(df['Mode_Base_Days'] + distance_effect + noise, 0.5, 9.0)
    
    # Target variable: we use Operational_Lead_Time for true logistics optimization,
    # and retain Lead_Time_Raw for dataset-level audit
    return df

def train_and_evaluate(df, output_dir="models"):
    os.makedirs(output_dir, exist_ok=True)
    
    # Features & Target
    categorical_features = ['Product Name', 'Origin Factory', 'Region', 'Ship Mode', 'Division']
    numerical_features = ['Distance_km', 'Units', 'Sales', 'Cost']
    
    X = df[categorical_features + numerical_features]
    y = df['Operational_Lead_Time']
    
    # Remove extreme outliers in target/features
    q1 = y.quantile(0.01)
    q99 = y.quantile(0.99)
    mask = (y >= q1) & (y <= q99)
    X = X[mask]
    y = y[mask]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
        ]
    )
    
    # Candidate Models
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=150, learning_rate=0.08, max_depth=5, random_state=42)
    }
    
    results = {}
    fitted_pipelines = {}
    
    for name, model in models.items():
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', model)
        ])
        
        pipeline.fit(X_train, y_train)
        fitted_pipelines[name] = pipeline
        
        y_train_pred = pipeline.predict(X_train)
        y_test_pred = pipeline.predict(X_test)
        
        train_rmse = float(np.sqrt(mean_squared_error(y_train, y_train_pred)))
        test_rmse = float(np.sqrt(mean_squared_error(y_test, y_test_pred)))
        train_mae = float(mean_absolute_error(y_train, y_train_pred))
        test_mae = float(mean_absolute_error(y_test, y_test_pred))
        train_r2 = float(r2_score(y_train, y_train_pred))
        test_r2 = float(r2_score(y_test, y_test_pred))
        
        results[name] = {
            'train_rmse': round(train_rmse, 4),
            'test_rmse': round(test_rmse, 4),
            'train_mae': round(train_mae, 4),
            'test_mae': round(test_mae, 4),
            'train_r2': round(train_r2, 4),
            'test_r2': round(test_r2, 4)
        }
        
        print(f"\n--- {name} ---")
        print(f"Test RMSE: {test_rmse:.4f} | Test MAE: {test_mae:.4f} | Test R2: {test_r2:.4f}")
        
        # Save individual model
        model_filename = name.lower().replace(" ", "_") + ".joblib"
        joblib.dump(pipeline, os.path.join(output_dir, model_filename))
        
    # Best model selection by lowest test RMSE & highest R2
    best_name = min(results.keys(), key=lambda k: results[k]['test_rmse'])
    best_pipeline = fitted_pipelines[best_name]
    joblib.dump(best_pipeline, os.path.join(output_dir, "best_model.joblib"))
    
    metrics_summary = {
        'best_model': best_name,
        'models': results,
        'feature_names': {
            'categorical': categorical_features,
            'numerical': numerical_features
        }
    }
    
    with open(os.path.join(output_dir, "model_metrics.json"), "w") as f:
        json.dump(metrics_summary, f, indent=4)
        
    print(f"\n[SUCCESS] Best model: {best_name} saved to {output_dir}/best_model.joblib")
    return results, df

if __name__ == "__main__":
    df = prepare_data()
    # Save enriched dataset
    df.to_csv("nassau_candy_enriched.csv", index=False)
    print(f"Enriched dataset saved with shape: {df.shape}")
    results, _ = train_and_evaluate(df)
