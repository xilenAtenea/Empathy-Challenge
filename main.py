import pandas as pd
from src.data_preprocessing import DataPreprocessor
from src.feature_engineer import FeatureEngineer

df_raw = pd.read_csv("data/raw/synthetic_health_data.csv")

processor = DataPreprocessor(df_raw)
df_clean = processor.run_all()

feature = FeatureEngineer(df_clean)
df_final = feature.run_all()

df_final.to_csv("data/processed/health_clean_data.csv", index=False)
print("Archivo guardado en data/processed/health_clean_data.csv")
