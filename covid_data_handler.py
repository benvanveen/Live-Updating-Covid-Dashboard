# Read data from a file:

def parse_csv_data(csv_filename:str)->list: # returns a list of strings for the rows in a csv file
    
    from csv import reader
    
    lines = open(csv_filename , 'r')
    read = reader(lines)
    lists = list(read) 
    
    return lists
    
# Data Processing:

def process_covid_csv_data(covid_csv_data:list)->tuple: # this function returns three variables, as shown below.
    
    # cases in 7 days
    last_days = []
    for i in range(3,10):
        last_7_days = covid_csv_data[i]
        cases = int(last_7_days[6])
        last_days.append(cases)
    cases_in_the_last_7days = sum(last_days)
    
    # hospital cases
    recent = covid_csv_data[1]
    hospital_cases = int(recent[5])
    
    # cumulative deaths
    last_report = covid_csv_data[14]
    cum_deaths = int(last_report[4])
    
    # as this function returns specific columns, it would not be guaranteed to return these values from a 
    # different dataset than nation 2021-10-28.csv
    
    return cases_in_the_last_7days, hospital_cases, cum_deaths # returns the values shown in this order

# Live data access:

def covid_API_request(location='Exeter',location_type='ltla')->dict:
    
    # To view your local covid data on the dashboard, go to the configuration file config.json and change the values in
    # the json file for local_location and local_location_type.
    
    loc = str(location)
    loctype = str(location_type)
    
    from uk_covid19 import Cov19API
    
    # cases_and_deaths defines the information to be obtained from the Cov19API data and how it will be structured.
    
    cases_and_deaths = {
    "date": "date",
    "areaName": "areaName",
    "areaCode": "areaCode",
    "newCasesByPublishDate": "newCasesByPublishDate",
    "cumCasesByPublishDate": "cumCasesByPublishDate",
    "newDeaths28DaysByDeathDate": "newDeaths28DaysByDeathDate",
    "cumDeaths28DaysByDeathDate": "cumDeaths28DaysByDeathDate",
    "hospitalCases":"hospitalCases"}
    
    area = [
    'areaType='+loctype,
    'areaName='+loc]
    
    
    # implements the covid data into the cases_and_deaths structure as seen above, some of the information i have included
    # in the data variable such as cumCasesByPublishDate are not used in the dashboard, but i have implemented them anyway
    # so they can be easily added to the dashboard.
    
    api = Cov19API(filters = area,structure=cases_and_deaths)
    data = api.get_json()
    return data

def update_covid():
    
    from covid_current_data_handler import cases_7_days, deaths_tot_and_hosp
    
    cases_7_days_eng = cases_7_days(loc=config["nation_location"],loc_type=config["nation_location_type"])
    deaths_and_hosp = deaths_tot_and_hosp()
    deaths=deaths_and_hosp[0]
    hosp=deaths_and_hosp[1]
    cases_7_days_loc = cases_7_days()
    
    # updates the old covid data to the new set of updated data
    old_covid_data[0]=cases_7_days_eng
    old_covid_data[1]=cases_7_days_loc
    old_covid_data[2]=deaths
    old_covid_data[3]=hosp
    
# time conversions:

def minutes_to_seconds( minutes: str ) -> int:
    return int(minutes)*60

def hours_to_minutes( hours: str ) -> int:
    return int(hours)*60

# converts time as shown on a digital clock, as a string into seconds (used for calculating the seconds until an update 
# should occur when a time is input into the dashboard)

def hhmm_to_seconds( hhmm: str ) -> int:
    if len(hhmm.split(':')) != 2:
        return None
    return minutes_to_seconds(hours_to_minutes(hhmm.split(':')[0])) + \
          minutes_to_seconds(hhmm.split(':')[1])

# Automated updates:
    
def schedule_covid_updates(update_interval:str,update_name:str):
    update_t = str(update_interval)
    
    from datetime import datetime
    import sched
    import time

    # accesses current time
    now = datetime.now()

    # removes the seconds from the current time
    current_timehms = now.strftime("%H:%M:%S")
    split = current_timehms.split(':')
    split.insert(1,':')
    split = [''.join(split[0 : 3])]
    current_time_hhmm = split[0]
    
    # uses hhmm_to_seconds to convert the digital clock time into seconds for the current and update times.
    current_time_s = hhmm_to_seconds(current_time_hhmm)
    update_time_s = hhmm_to_seconds(update_t)
    
    # calculates the seconds between the current and update time.
    interval = update_time_s - current_time_s
    
    # schedules the update to run after interval seconds
    s=sched.scheduler(time.time,time.sleep)
    e1=s.enter(interval,1,update_name)