import pandas as pd

def analyze_csv(file_path):
    df=pd.read_csv(file_path)

    summary={
        "total_count":len(df),
        "avg_flowrate":df["Flowrate"].mean(),
        "avg_pressure":df["Pressure"].mean(),
        "avg_temperature":df["Temperature"].mean(),
        "type_distribution":df["Type"].value_counts().to_dict()
    }
    return summary