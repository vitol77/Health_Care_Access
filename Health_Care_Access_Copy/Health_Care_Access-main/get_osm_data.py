import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import overpy
# *** MUST DO "pip install overpy" FOR THIS FILE TO WORK ***


# CITATIONS USED TO LEARN OVERPASS TURBO:

# Used as an intro to Openstreet map
# https://www.youtube.com/watch?v=q9QI4AfwHoM&ab_channel=OpenStreetMapUS

# Used to learn how to use overpass API to get data and save to CSV file
# Adapted some code from this tutorial to extract relevant data
# https://www.youtube.com/watch?v=DnKJ5HrS_NI&t=58s&ab_channel=NikhilNagar


# Used to get build and learn how to build queries in overpass turbo
# https://overpass-turbo.eu/

# Used to learn how to extract info by city
# https://dev.overpass-api.de/overpass-doc/en/full_data/area.html
# https://stackoverflow.com/questions/71433686/limit-overpy-query-to-specific-area-e-g-country

# Overpass turbo tutorial (used to learn how to only extract data a certain distance from one amenity to another)
# Adapted some code from this tutorial in get_amenity_data_around function
# https://www.youtube.com/watch?v=q9QI4AfwHoM&t=1005s&ab_channel=OpenStreetMapUS

#Overpass Docs
#https://dev.overpass-api.de/overpass-doc/en/full_data/area.html


api = overpy.Overpass()


def hospital_data_cleaner(df_node, df_ways):
    df_node = df_node.drop(columns=['healthcare'])

    df_ways = df_ways.drop(columns=['healthcare', 'operator:type', 'phone', 'website', 'wikidata',
                          'alt_name', 'landuse', 'full_name', 'healthcare:speciality', 'gnis:feature_id',
                          'operator:wikidata', 'operator:wikipedia', 'short_name', 'addr:province', 'ref'])

    return df_node, df_ways


def hospital_data_cleaner(df_node, df_ways):
    df_node = df_node.drop(columns=['healthcare'])

    df_ways = df_ways.drop(columns=['healthcare', 'operator:type', 'phone', 'website', 'wikidata',
                          'alt_name', 'landuse', 'full_name', 'healthcare:speciality', 'gnis:feature_id',
                          'operator:wikidata', 'operator:wikipedia', 'short_name', 'addr:province', 'ref'])

    return df_node, df_ways


# Only extracts main amenities if the secondary_amenity is within the specified distance
# To output a csv file input "yes" for output arg
def filter_amenity_by_nearby_amenity(city, main_amenity, secondary_amenity, distance, output):
    if secondary_amenity == "station":
        result = api.query(f"""
            area["name"="{city}"]->.small;
            area["name"="Canada"]->.big;
            (
             node["public_transport"= """ + secondary_amenity + """](area.small)(area.big);
             way["public_transport"= """ + secondary_amenity + """](area.small)(area.big);
            );
            node["amenity"= """ + main_amenity + """](around:""" + distance + """); 
            out body;
            """)
    else:
        result = api.query(f"""
            area["name"="{city}"]->.small;
            area["name"="Canada"]->.big;
            (
             node["amenity"= """ + secondary_amenity + """](area.small)(area.big);
             way["amenity"= """ + secondary_amenity + """](area.small)(area.big);
            );
            node["amenity"= """ + main_amenity + """](around:""" + distance + """); 
            out body;
            """)

    out_list_nodes = []
    for node in result.nodes:
        node.tags['lat'] = node.lat
        node.tags['lon'] = node.lon
        out_list_nodes.append(node.tags)
    df_nodes = pd.DataFrame(out_list_nodes)

    if output == "yes":
        df_nodes.to_csv('filtered_' + city + '_' + main_amenity + '_nodes.csv')

    return df_nodes


# Extracts secondary amenities nearby main amenities within a specified distance
# To output a csv file input "yes" for output arg
def get_nearby_amenity_data(city, main_amenity, secondary_amenity, distance, output):
    result = api.query(f"""
        area["name"="{city}"]; 
        (
         node["amenity"= """ + main_amenity + """](area);
         way["amenity"= """ + main_amenity + """](area);
        );
        node["amenity"= """ + secondary_amenity + """](around:""" + distance + """); 
        out body;
        """)

    out_list_nodes = []
    for node in result.nodes:
        node.tags['lat'] = node.lat
        node.tags['lon'] = node.lon
        out_list_nodes.append(node.tags)
    df_nodes = pd.DataFrame(out_list_nodes)

    if output == "yes":
        df_nodes.to_csv(city + '_' + secondary_amenity + '_nodes.csv')

    return df_nodes


# Function to extract data about a particular amenity in a city
# To output a csv file input "yes" for output arg
# Note: To get the correct city confirm on: https://overpass-turbo.eu/
# List of amenities: https://wiki.openstreetmap.org/wiki/Key:amenity
def get_amenity_data(city, amenity, output):

    result = api.query(f"""
        area["name"="{city}"]->.small;
        area["name"="Canada"]->.big;
        (
        way["amenity"=""" + amenity + """](area.small)(area.big);
        node["amenity"=""" + amenity + """](area.small)(area.big);
  
  
        );
        out body;
        """)

    out_list_ways = []
    for way in result.ways:
        out_list_ways.append(way.tags)
    df_ways = pd.DataFrame(out_list_ways)

    out_list_nodes = []
    for node in result.nodes:
        node.tags['lat'] = node.lat
        node.tags['lon'] = node.lon
        out_list_nodes.append(node.tags)
    df_nodes = pd.DataFrame(out_list_nodes)

    # if amenity == "hospital":
    #     df_nodes, df_ways = hospital_data_cleaner(df_nodes, df_ways)
    if output == "yes":
        df_ways.to_csv(city + '_' + amenity + '_ways.csv')
        df_nodes.to_csv(city + '_' + amenity + '_nodes.csv')
    # print(df_ways)
    return df_ways, df_nodes


# Probably will not need this
# Can use to find distance between a bus stop and a hospital for example
# Function taken from E4
# Which referenced: #https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula/21623206
def coordinates_to_distance(df_a, df_b):
    lat1 = df_a['lat']
    lat2 = df_b['lat']
    lon1 = df_a['lon']
    lon2 = df_b['lon']

    p = np.pi / 180
    r = 6371000

    d_lat = (lat2 - lat1) * p
    d_lon = (lon2 - lon1) * p

    a = np.square(np.sin(d_lat / 2))
    b = np.cos(lat1 * p) * np.cos(lat2 * p) * np.square(np.sin(d_lon / 2))

    d = 2 * r * np.arcsin(np.sqrt(a + b))

    return d

def get_amenity_counts():
    city_list = ["Vancouver", "Kelowna", "Abbotsford", "Victoria", "Kamloops", "Nanaimo", "Chilliwack",
                 "Vernon", "Campbell River", "Penticton"]

    amenity_list = ["hospital", "social_facility", "clinic", "pharmacy", "doctors"]

    # Can extract mass data like this into csv
    count_df = pd.DataFrame(columns=['Hospitals', 'Social Facilities', 'Clinics', 'Pharmacies', "Doctors"],
                            index=["Vancouver", "Kelowna", "Abbotsford", "Victoria", "Kamloops", "Nanaimo", "Chilliwack",
                 "Vernon", "Campbell River", "Penticton"])
    # print(count_df)
    counts = []
    for city in city_list:
        counts = []
        for amenity in amenity_list:
            df_ways, df_nodes, = get_amenity_data(city, amenity, "no")
            if df_ways.shape[0] > df_nodes.shape[0]:
                counts.append(df_ways.shape[0])
            else:
                counts.append(df_nodes.shape[0])
        count_df.loc[city] = counts

    count_df.to_csv("amenity_counts.csv")


def get_healthcare_near_count():
    city_list = ["Vancouver", "Kelowna", "Abbotsford", "Victoria", "Kamloops", "Nanaimo", "Chilliwack",
                 "Vernon", "Campbell River", "Penticton"]

    amenity_list = ["hospital", "social_facility", "clinic", "pharmacy", "doctors"]

    secondary_amenity = ["taxi", "station", "parking"]

    # Can extract mass data like this into csv
    count_df = pd.DataFrame(columns=['Hospitals', 'Social Facilities', 'Clinics', 'Pharmacies', 'Doctors'],
                            index=["Vancouver", "Kelowna", "Abbotsford", "Victoria", "Kamloops", "Nanaimo",
                                   "Chilliwack", "Vernon", "Campbell River", "Penticton"])
    # print(count_df)
    counts = []
    for amen in secondary_amenity:
        for city in city_list:
            counts = []
            for amenity in amenity_list:
                df_nodes = filter_amenity_by_nearby_amenity(city, amenity, amen, "400", "no")
                counts.append(df_nodes.shape[0])
            count_df.loc[city] = counts
        count_df.to_csv("nearby_" + amen + "_counts.csv")


# **All function inputs must be string**
def main():

    # Add/remove cities her
    # get_amenity_data("Kelowna", "pharmacy", "yes")
    get_amenity_counts()
    get_healthcare_near_count()
    # print(counts)

    # get_nearby_amenity_data("Vancouver", "hospital", "station", "250", "yes")

    # x = filter_amenity_by_nearby_amenity("Kamloops", "pharmacy", "parking", "400", "yes")
    # print(x)


if __name__ == '__main__':
    main()
