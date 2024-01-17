import numpy as np
import pandas as pd


def sum_cols(df):
    df["total"] = df["Hospitals"] + df["Social Facilities"] + df["Clinics"] + df["Pharmacies"] + df["Doctors"]
    return df


def main():

    df_1 = pd.read_csv('Counts/nearby_station_counts.csv')
    df_2 = pd.read_csv('Counts/nearby_parking_counts.csv')
    df_3 = pd.read_csv('Counts/nearby_taxi_counts.csv')
    df_4 = pd.read_csv('Counts/amenity_counts.csv')

    df_1 = sum_cols(df_1)
    df_2 = sum_cols(df_2)
    df_3 = sum_cols(df_3)
    df_4 = sum_cols(df_4)

    df_1.to_csv('Sum/summed_stations.csv')
    df_2.to_csv('Sum/summed_parking.csv')
    df_3.to_csv('Sum/summed_taxi.csv')
    df_4.to_csv('Sum/summed_counts.csv')


if __name__ == "__main__":
    main()
