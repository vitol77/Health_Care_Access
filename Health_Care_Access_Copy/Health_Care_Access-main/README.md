# Health Care Access


In this project, we looked at how healthcare facilities in a city might affect the spread of diseases. We had three main questions:

1. Does having more healthcare facilities in a city relate to fewer diseases?
2. How does the location of healthcare facilities near places like parking lots or public transit stations impact disease rates?
3. Are there specific diseases that are affected by the presence of healthcare facilities near certain places?

By answering these questions, we hoped to find ways to improve public health and reduce the number of diseases in the city.

## Required Libraries
- Overpy
- Pandas
- Numpy
- Scipy
- Matplotlib



## Commands to run it

### Installation Commands
- Installing jupyter Notebook:
  - ```pip install jupyter ```
- Installing individual libraries:
  -  ```pip install overpy```
  -  ```pip install pandas```
  -  ```pip install numpy```
  -  ```pip install scipy```
  -  ```pip install matplotlib```
- To install __all libraries__:
  - ```pip install pandas numpy scipy matplotlib overpy```

### Order of Execution fo cleaning the data and data analysis 

__*All csv's files produced from these files already exist in the repo.*__

1. get_osm_data.py
   - To run this file, use either of these commands:
     - ``` python get_osm_data.py```
     - ``` python3 get_osm_data.py```
2. filter_city_profiles.py
   - To run this file, use either of these commands:
     - ``` python filter_city_profiles.py```
     - ``` python3 filter_city_profiles.py```
3. sum_nearby_data.py
   - To run this file, use either of these commands:
     - ``` python sum_nearby_data.py```
     - ``` python3 sum_nearby_data.py```
4. stats.py
   - To run this file, use either of these commands:
     - ``` python stats.py```
     - ``` python3 stats.py```
5. stats_to_csv.ipynb
   - Run the code cells individually or run all cells
6. more_stats_test.ipynb
   - Run the code cells individually or run all cells

## Files produced/expected

### Data Files

- __From filter_city_profiles.py__
  - city_profiles.csv
- __From get_osm_data.py__
  - amenity_counts.csv
  - nearby_parking_counts.csv
  - nearby_station_counts.csv
  - nearby_taxi_counts.csv
- __From sum_nearby_data.py__
  - summed_stations.csv
  - summed_parking.csv
  - summed_taxi.csv
  - summed_counts.csv
- __From stats.py__
  - 0counts.csv
  - 1counts.csv
  - 2counts.csv
  - 3counts.csv
  - 4counts.csv
  - 5counts.csv
  - 6counts.csv
  - 7counts.csv
  - 8counts.csv
  - 9counts.csv
- __From stats_to_csv.ipynb__
  - 0counts.csv
  - 1counts.csv
  - 2counts.csv
  - 3counts.csv
  - 4counts.csv
  - 5counts.csv
  - 6counts.csv
  - 7counts.csv
  - 8counts.csv
  - 9counts.csv
  - format_avg_pr.csv
  - format_avg_ir.csv
  - format_prir_van.csv
  - format_prir_ver.csv
  - format_prir_vic.csv
  - format_prir_abb.csv
  - format_prir_camp.csv
  - format_prir_chill.csv
  - format_prir_kam.csv
  - format_prir_kel.csv
  - format_prir_nana.csv
  - format_prir_pen.csv
  - format_sum_health.csv
  - format_sum_taxi.csv
  - format_sum_parking.csv
  - format_sum_station.csv
  - format_indiv_pr.csv
  - format_indiv_ir.csv
