import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import os

# To get every nth row
# https://stackoverflow.com/questions/25055712/pandas-every-nth-row
def main():

    # Count data
    health_counts = pd.read_csv('Counts/amenity_counts.csv')
    nearby_taxi = pd.read_csv('Counts/nearby_taxi_counts.csv')
    nearby_parking = pd.read_csv('Counts/nearby_parking_counts.csv')
    nearby_station = pd.read_csv('Counts/nearby_station_counts.csv')

    # Summed count data
    sum_health_counts = pd.read_csv('Sum/summed_counts.csv')
    sum_nearby_taxi = pd.read_csv('Sum/summed_taxi.csv')
    sum_nearby_parking = pd.read_csv('Sum/summed_parking.csv')
    sum_nearby_station = pd.read_csv('Sum/summed_stations.csv')

    sum_health_counts = sum_health_counts.drop(
        columns=["Hospitals", "Social Facilities", "Clinics", "Pharmacies", "Doctors"])
    sum_nearby_taxi = sum_nearby_taxi.drop(
        columns=["Hospitals", "Social Facilities", "Clinics", "Pharmacies", "Doctors"])
    sum_nearby_parking = sum_nearby_parking.drop(
        columns=["Hospitals", "Social Facilities", "Clinics", "Pharmacies", "Doctors"])
    sum_nearby_station = sum_nearby_station.drop(
        columns=["Hospitals", "Social Facilities", "Clinics", "Pharmacies", "Doctors"])

    sum_health_counts = sum_health_counts.rename(columns={"Unnamed: 0": "City"})
    sum_health_counts = sum_health_counts.drop(columns=["Unnamed: 0.1"])

    sum_nearby_taxi = sum_nearby_taxi.rename(columns={"Unnamed: 0": "City"})
    sum_nearby_taxi = sum_nearby_taxi.drop(columns=["Unnamed: 0.1"])

    sum_nearby_parking = sum_nearby_parking.rename(columns={"Unnamed: 0": "City"})
    sum_nearby_parking = sum_nearby_parking.drop(columns=["Unnamed: 0.1"])

    sum_nearby_station = sum_nearby_station.rename(columns={"Unnamed: 0": "City"})
    sum_nearby_station = sum_nearby_station.drop(columns=["Unnamed: 0.1"])

    # print(sum_nearby_station)

    # Disease Data
    data = pd.read_csv('Counts/city_profiles.csv')

    # Used to learn how to append multiple rows to DF
    # https: // practicaldatascience.co.uk / data - science / how - to - use - append - to - add - rows - to - a - pandas - dataframe  #:~:text=Use%20append()%20and%20Series,rows%20to%20an%20existing%20dataframe.
    # Average number of people with disease per 1000
    grouped_data = data.drop(columns="Indicator")
    grouped_data_100 = pd.DataFrame()
    snd = 10
    fst = 5
    for i in range(10):
        rows = (data.iloc[fst:snd])
        grouped_data_100 = grouped_data_100.append(rows, ignore_index=True)
        fst = fst + 10
        snd = snd + 10

    # print(grouped_data_100)
    grouped_data_100 = grouped_data_100.drop(columns="Unnamed: 0")
    grouped_data_100 = grouped_data_100.groupby(["City"]).sum("Value")
    grouped_data_100['Value'] = grouped_data_100['Value'] / 5
    grouped_data_100 = grouped_data_100.join(sum_health_counts.set_index('City'), on="City")

    # print(grouped_data_100)
    grouped_data_1000 = pd.DataFrame()
    snd = 5
    fst = 0
    for i in range(10):
        rows = (data.iloc[fst:snd])
        grouped_data_1000 = grouped_data_1000.append(rows, ignore_index=True)
        fst = fst + 10
        snd = snd + 10

    # print(grouped_data_100)
    grouped_data_1000 = grouped_data_1000.drop(columns="Unnamed: 0")
    grouped_data_1000 = grouped_data_1000.groupby(["City"]).sum("Value")
    grouped_data_1000['Value'] = grouped_data_1000['Value'] / 5
    # print(grouped_data_1000)

    grouped_data_1000 = grouped_data_1000.join(sum_health_counts.set_index('City'), on="City")

    # DataFrames split up by city
    van = data[data["City"] == "Vancouver"]
    ver = data[data["City"] == "Vernon"]
    vic = data[data["City"] == "Victoria"]
    abb = data[data["City"] == "Abbotsford"]
    camp = data[data["City"] == "Campbell River"]
    chill = data[data["City"] == "Chilliwack"]
    kam = data[data["City"] == "Kamloops"]
    kel = data[data["City"] == "Kelowna"]
    nana = data[data["City"] == "Nanaimo"]
    pen = data[data["City"] == "Penticton"]

    # linear regression with avg total disease prevalence per 100
    fit_100 = stats.linregress(grouped_data_100["total"], grouped_data_100["Value"])
    grouped_data_100['prediction'] = grouped_data_100['total'] * fit_100.slope + fit_100.intercept

    # linear regression with avg total disease incidence per 1000
    fit_1000 = stats.linregress(grouped_data_1000["total"], grouped_data_1000["Value"])
    grouped_data_1000['prediction'] = grouped_data_1000['total'] * fit_1000.slope + fit_1000.intercept

    plt.xlabel("Total Number of Healthcare Facilities")
    plt.ylabel("Diseases in the Population Per 1000")
    plt.scatter(grouped_data_100['total'], grouped_data_100['Value'])
    plt.xticks(rotation="vertical")

    print("Per 100 is the prevalence of disease & Per 1000 is incidence of disease. \n")

    # plt.plot(grouped_data['total'], grouped_data["Value"], 'r-', linewidth=3)
    # plt.show()
    print("P-Value & r-value for total healthcare amenities and average disease prevalence per 100: ", fit_100.pvalue, fit_1000.rvalue)
    print("P-Value  & r-value for total healthcare amenities and average disease incidence per 1000: ", fit_1000.pvalue, fit_1000.rvalue, "\n")

    # Used answer to learn how to write files to a directory
    # https://stackoverflow.com/questions/47143836/pandas-dataframe-to-csv-raising-ioerror-no-such-file-or-directory
    # Extracting each individual disease data
    outdir = './Diseases'
    for i in range(10):
        f_name = str(i)
        df = data.iloc[i::10, :]
        df = df.drop(columns="Unnamed: 0")
        outname = f_name + "counts.csv"
        joined_name = os.path.join(outdir, outname)
        df.to_csv(joined_name)

    disease1 = pd.read_csv('Diseases/0counts.csv')
    disease2 = pd.read_csv('Diseases/1counts.csv')
    disease3 = pd.read_csv('Diseases/2counts.csv')
    disease4 = pd.read_csv('Diseases/3counts.csv')
    disease5 = pd.read_csv('Diseases/4counts.csv')
    disease6 = pd.read_csv('Diseases/5counts.csv')
    disease7 = pd.read_csv('Diseases/6counts.csv')
    disease8 = pd.read_csv('Diseases/7counts.csv')
    disease9 = pd.read_csv('Diseases/8counts.csv')
    disease10 = pd.read_csv('Diseases/9counts.csv')

    disease1 = disease1.join(sum_health_counts.set_index('City'), on="City")
    disease1 = disease1.drop(columns="Unnamed: 0")

    disease2 = disease2.join(sum_health_counts.set_index('City'), on="City")
    disease2 = disease2.drop(columns="Unnamed: 0")

    disease3 = disease3.join(sum_health_counts.set_index('City'), on="City")
    disease3 = disease3.drop(columns="Unnamed: 0")

    disease4 = disease4.join(sum_health_counts.set_index('City'), on="City")
    disease4 = disease4.drop(columns="Unnamed: 0")

    disease5 = disease5.join(sum_health_counts.set_index('City'), on="City")
    disease5 = disease5.drop(columns="Unnamed: 0")

    disease6 = disease6.join(sum_health_counts.set_index('City'), on="City")
    disease6 = disease6.drop(columns="Unnamed: 0")

    disease7 = disease7.join(sum_health_counts.set_index('City'), on="City")
    disease7 = disease7.drop(columns="Unnamed: 0")

    disease8 = disease8.join(sum_health_counts.set_index('City'), on="City")
    disease8 = disease8.drop(columns="Unnamed: 0")

    disease9 = disease9.join(sum_health_counts.set_index('City'), on="City")
    disease9 = disease9.drop(columns="Unnamed: 0")

    disease10 = disease10.join(sum_health_counts.set_index('City'), on="City")
    disease10 = disease10.drop(columns="Unnamed: 0")

    disease_df_list = [disease1, disease2, disease3, disease4, disease5, disease6, disease7, disease8, disease9, disease10]
    disease_list = ["Asthma (5-54) Per 100", "COPD (45+) Per 100", "Diabetes (1+) Per 100",
                    "Heart Failure (1+) Per 100", "Hypertension (20+) Per 100", "Asthma (5-54) Per 1000",
                    "COPD (45+) Per 1000", "Diabetes (1+) Per 1000", "Heart Failure (1+) Per 1000",
                    "Hypertension (20+) Per 1000"]

    print("Comparing individual diseases to the total healthcare amenity counts:")
    k = 0
    for i in disease_df_list:
        fit = stats.linregress(i["total"], i["Value"])
        print(disease_list[k], "P-Value:", fit.pvalue, "r-Value:", fit.rvalue)
        k = k+1

    # TODO: Individual diseases vs amenities near some form of transportation
    disease1_near = pd.read_csv('Diseases/0counts.csv')
    disease2_near = pd.read_csv('Diseases/1counts.csv')
    disease3_near = pd.read_csv('Diseases/2counts.csv')
    disease4_near = pd.read_csv('Diseases/3counts.csv')
    disease5_near = pd.read_csv('Diseases/4counts.csv')
    disease6_near = pd.read_csv('Diseases/5counts.csv')
    disease7_near = pd.read_csv('Diseases/6counts.csv')
    disease8_near = pd.read_csv('Diseases/7counts.csv')
    disease9_near = pd.read_csv('Diseases/8counts.csv')
    disease10_near = pd.read_csv('Diseases/9counts.csv')

    disease1_parking = disease1_near.join(sum_nearby_parking.set_index('City'), on="City")
    disease1_parking = disease1_parking.drop(columns="Unnamed: 0")

    disease2_parking = disease2_near.join(sum_nearby_parking.set_index('City'), on="City")
    disease2_parking = disease2_parking.drop(columns="Unnamed: 0")

    disease3_parking = disease3_near.join(sum_nearby_parking.set_index('City'), on="City")
    disease3_parking = disease3_parking.drop(columns="Unnamed: 0")

    disease4_parking = disease4_near.join(sum_nearby_parking.set_index('City'), on="City")
    disease4_parking = disease4_parking.drop(columns="Unnamed: 0")

    disease5_parking = disease5_near.join(sum_nearby_parking.set_index('City'), on="City")
    disease5_parking = disease5_parking.drop(columns="Unnamed: 0")

    disease6_parking = disease6_near.join(sum_nearby_parking.set_index('City'), on="City")
    disease6_parking = disease6_parking.drop(columns="Unnamed: 0")

    disease7_parking = disease7_near.join(sum_nearby_parking.set_index('City'), on="City")
    disease7_parking = disease7_parking.drop(columns="Unnamed: 0")

    disease8_parking = disease8_near.join(sum_nearby_parking.set_index('City'), on="City")
    disease8_parking = disease8_parking.drop(columns="Unnamed: 0")

    disease9_parking = disease9_near.join(sum_nearby_parking.set_index('City'), on="City")
    disease9_parking = disease9_parking.drop(columns="Unnamed: 0")

    disease10_parking = disease10_near.join(sum_nearby_parking.set_index('City'), on="City")
    disease10_parking = disease10_parking.drop(columns="Unnamed: 0")


    disease_df_list = [disease1_parking, disease2_parking, disease3_parking, disease4_parking, disease5_parking,
                       disease6_parking, disease7_parking, disease8_parking, disease9_parking,
                       disease10_parking]

    print("\n")
    print("Comparing individual diseases to the total healthcare amenity near a parking lot:")
    m = 0
    for j in disease_df_list:
        fit = stats.linregress(j["total"], j["Value"])
        print(disease_list[m], "P-Value:", fit.pvalue, "r-Value:", fit.rvalue)
        m = m + 1

    disease1_taxi = disease1_near.join(sum_nearby_taxi.set_index('City'), on="City")
    disease1_taxi = disease1_taxi.drop(columns="Unnamed: 0")

    disease2_taxi = disease2_near.join(sum_nearby_taxi.set_index('City'), on="City")
    disease2_taxi = disease2_taxi.drop(columns="Unnamed: 0")

    disease3_taxi = disease3_near.join(sum_nearby_taxi.set_index('City'), on="City")
    disease3_taxi = disease3_taxi.drop(columns="Unnamed: 0")

    disease4_taxi = disease4_near.join(sum_nearby_taxi.set_index('City'), on="City")
    disease4_taxi = disease4_taxi.drop(columns="Unnamed: 0")

    disease5_taxi = disease5_near.join(sum_nearby_taxi.set_index('City'), on="City")
    disease5_taxi = disease5_taxi.drop(columns="Unnamed: 0")

    disease6_taxi = disease6_near.join(sum_nearby_taxi.set_index('City'), on="City")
    disease6_taxi = disease6_taxi.drop(columns="Unnamed: 0")

    disease7_taxi = disease7_near.join(sum_nearby_taxi.set_index('City'), on="City")
    disease7_taxi = disease7_taxi.drop(columns="Unnamed: 0")

    disease8_taxi = disease8_near.join(sum_nearby_taxi.set_index('City'), on="City")
    disease8_taxi = disease8_taxi.drop(columns="Unnamed: 0")

    disease9_taxi = disease9_near.join(sum_nearby_taxi.set_index('City'), on="City")
    disease9_taxi = disease9_taxi.drop(columns="Unnamed: 0")

    disease10_taxi = disease10_near.join(sum_nearby_taxi.set_index('City'), on="City")
    disease10_taxi = disease10_taxi.drop(columns="Unnamed: 0")

    disease_df_list = [disease1_taxi, disease2_taxi, disease3_taxi, disease4_taxi, disease5_taxi,
                       disease6_taxi, disease7_taxi, disease8_taxi, disease9_taxi,
                       disease10_taxi]

    print("\n")
    print("Comparing individual diseases to the total healthcare amenity near a taxi stand:")
    n = 0
    for j in disease_df_list:
        fit = stats.linregress(j["total"], j["Value"])
        print(disease_list[n], "P-Value:", fit.pvalue, "r-Value:", fit.rvalue)
        n = n + 1

    disease1_station = disease1_near.join(sum_nearby_station.set_index('City'), on="City")
    disease1_station = disease1_station.drop(columns="Unnamed: 0")

    disease2_station = disease2_near.join(sum_nearby_station.set_index('City'), on="City")
    disease2_station = disease2_station.drop(columns="Unnamed: 0")

    disease3_station = disease3_near.join(sum_nearby_station.set_index('City'), on="City")
    disease3_station = disease3_station.drop(columns="Unnamed: 0")

    disease4_station = disease4_near.join(sum_nearby_station.set_index('City'), on="City")
    disease4_station = disease4_station.drop(columns="Unnamed: 0")

    disease5_station = disease5_near.join(sum_nearby_station.set_index('City'), on="City")
    disease5_station = disease5_station.drop(columns="Unnamed: 0")

    disease6_station = disease6_near.join(sum_nearby_station.set_index('City'), on="City")
    disease6_station = disease6_station.drop(columns="Unnamed: 0")

    disease7_station = disease7_near.join(sum_nearby_station.set_index('City'), on="City")
    disease7_station = disease7_station.drop(columns="Unnamed: 0")

    disease8_station = disease8_near.join(sum_nearby_station.set_index('City'), on="City")
    disease8_station = disease8_station.drop(columns="Unnamed: 0")

    disease9_station = disease9_near.join(sum_nearby_station.set_index('City'), on="City")
    disease9_station = disease9_station.drop(columns="Unnamed: 0")

    disease10_station = disease10_near.join(sum_nearby_station.set_index('City'), on="City")
    disease10_station = disease10_station.drop(columns="Unnamed: 0")

    disease_df_list = [disease1_station, disease2_station, disease3_station, disease4_station, disease5_station,
                       disease6_station, disease7_station, disease8_station, disease9_station,
                       disease10_station]

    print("\n")
    print("Comparing individual diseases to the total healthcare amenity near a major public transit station:")
    p = 0
    for j in disease_df_list:
        fit = stats.linregress(j["total"], j["Value"])
        print(disease_list[p], "P-Value:", fit.pvalue, "r-Value:", fit.rvalue)
        p = p + 1

    # TODO: All diseases avg vs amenities near a form of transportation

    grouped_data_1000 = grouped_data_1000.drop(columns="total")
    grouped_data_1000 = grouped_data_1000.drop(columns="prediction")
    grouped_data_100 = grouped_data_100.drop(columns="total")
    grouped_data_100 = grouped_data_100.drop(columns="prediction")
    # print(grouped_data_1000)

    disease_1000_taxi = grouped_data_1000.join(sum_nearby_taxi.set_index('City'), on="City")

    disease_1000_station = grouped_data_1000.join(sum_nearby_station.set_index('City'), on="City")

    disease_1000_parking = grouped_data_1000.join(sum_nearby_parking.set_index('City'), on="City")

    disease_100_taxi = grouped_data_100.join(sum_nearby_taxi.set_index('City'), on="City")

    disease_100_station = grouped_data_100.join(sum_nearby_station.set_index('City'), on="City")

    disease_100_parking = grouped_data_100.join(sum_nearby_parking.set_index('City'), on="City")

    disease_df_per_list = [disease_1000_taxi, disease_1000_station, disease_1000_parking, disease_100_taxi,
                           disease_100_station, disease_100_parking]
    disease_df_per_name = ["disease_1000_taxi", "disease_1000_station", "disease_1000_parking", "disease_100_taxi",
                           "disease_100_station", "disease_100_parking"]

    print("\n")
    print("Comparing disease prevalence per 100 and incidence per 1000 to the total healthcare amenity near a "
          "form of transportation")
    q = 0
    for j in disease_df_per_list:
        fit = stats.linregress(j["total"], j["Value"])
        print(disease_df_per_name[q], "P-Value:", fit.pvalue, "r-Value:", fit.rvalue)
        q = q + 1

    # TODO: Number of each specific healthcare vs total count of disease incidence/prevalence
    # Take each healthcare amenity and join it with the avg disease prevalence per 100 & incidence 1000
    df_hospitals = health_counts.drop(columns=["Social Facilities", "Clinics", "Pharmacies", "Doctors"])
    df_hospitals = df_hospitals.rename(columns={"Unnamed: 0": "City"})

    df_social_facilities = health_counts.drop(columns=["Hospitals", "Clinics", "Pharmacies", "Doctors"])
    df_social_facilities = df_social_facilities.rename(columns={"Unnamed: 0": "City"})

    df_clinics =  health_counts.drop(columns=["Social Facilities", "Hospitals", "Pharmacies", "Doctors"])
    df_clinics = df_clinics.rename(columns={"Unnamed: 0": "City"})

    df_pharm = health_counts.drop(columns=["Social Facilities", "Clinics", "Hospitals", "Doctors"])
    df_pharm = df_pharm.rename(columns={"Unnamed: 0": "City"})

    df_doctors =  health_counts.drop(columns=["Social Facilities", "Clinics", "Pharmacies", "Hospitals"])
    df_doctors = df_doctors.rename(columns={"Unnamed: 0": "City"})

    # print(df_doctors)

    #Todo: Join with the per 100 and per 1000 data woth each individual amenity

    # print(df_hospitals)

    grouped_data_1000 = grouped_data_1000.reset_index()
    grouped_data_100 = grouped_data_100.reset_index()

    df_hospitals_1000 = df_hospitals.join(grouped_data_1000.set_index('City'), on="City")
    df_hospitals_100 = df_hospitals.join(grouped_data_100.set_index('City'), on="City")

    df_social_facilities_1000 = df_social_facilities.join(grouped_data_1000.set_index('City'), on="City")
    df_social_facilities_100 = df_social_facilities.join(grouped_data_100.set_index('City'), on="City")

    df_clinics_1000 = df_clinics.join(grouped_data_1000.set_index('City'), on="City")
    df_clinics_100 = df_clinics.join(grouped_data_100.set_index('City'), on="City")

    df_pharm_1000 = df_pharm.join(grouped_data_1000.set_index('City'), on="City")
    df_pharm_100 = df_pharm.join(grouped_data_100.set_index('City'), on="City")

    df_doctors_1000 = df_doctors.join(grouped_data_1000.set_index('City'), on="City")
    df_doctors_100 = df_doctors.join(grouped_data_100.set_index('City'), on="City")

    # print(df_social_facilities_1000)

    print("\n")
    print("Comparing individual healthcare facilities against avg disease incidences in each city")
    amenity_df_per_list = [df_hospitals_1000, df_hospitals_100, df_social_facilities_1000, df_social_facilities_100,
                           df_clinics_1000 , df_clinics_100, df_pharm_1000,  df_pharm_100, df_doctors_1000,
                           df_doctors_100]

    amenity_list = ["Hospitals", "Hospitals",  "Social Facilities", "Social Facilities", "Clinics", "Clinics",
                    "Pharmacies", "Pharmacies", "Doctors", "Doctors"]

    g = 0
    for j in amenity_df_per_list:
        curr_amenity = amenity_list[g]
        fit = stats.linregress(j[curr_amenity], j["Value"])
        if(g % 2 == 0):
            print(amenity_list[g], "Per 1000 P-Value:", fit.pvalue, "r-Value:", fit.rvalue)
        else:
            print(amenity_list[g], "Per 100 P-Value:", fit.pvalue, "r-Value:", fit.rvalue)
        g = g + 1



if __name__ == '__main__':
    main()
