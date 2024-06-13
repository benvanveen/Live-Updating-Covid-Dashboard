from flask import request, render_template, Flask
from datetime import datetime
import time
import sched
import json
import pytest
import logging
from covid_data_handler import parse_csv_data, minutes_to_seconds, process_covid_csv_data, update_covid
from covid_data_handler import covid_API_request, schedule_covid_updates, hours_to_minutes, hhmm_to_seconds
from covid_news_handling import news_API_request, update_news
from covid_current_data_handler import cases_7_days, deaths_tot_and_hosp

with open("config.json", "r", encoding="utf8") as config_file:
    config = json.load(config_file)
    
# variables:
    
apps=Flask(__name__)

news = news_API_request(api_base_url=config["api_base_url"],
                        api_country=config["api_country"],
                        covid_terms=config["terms"],
                        api_key_input=config["api_key"])

s=sched.scheduler(time.time,time.sleep)

updates=[]

# logging data in sys.log

logging.basicConfig(filename='sys.log',  level=logging.DEBUG)

# function for adding updates

def add_updates(a='label',b='date'):
    
        updates.append({
            'title':a,
            'content':b
        })
        return updates
    
# current covid data
    
cases_7_days_eng = cases_7_days(loc=config["nation_location"],loc_type=config["nation_location_type"])
deaths_and_hosp = deaths_tot_and_hosp(config["nation_location"],config["nation_location_type"])
cases_7_days_loc = cases_7_days(config["local_location"],config["local_location_type"])

# OLD COVID DATA IS IN THE FOLLOWING ORDER: CASES7DAYSENG, CASES7DAYSLOC, DEATHS, HOSPITAL CASES
old_covid_data=[]
old_covid_data.append(cases_7_days_eng)
old_covid_data.append(cases_7_days_loc)
for i in deaths_and_hosp:
    old_covid_data.append(i)
    
# functions for deleting news articles and updates

def del_update(update_name:str):
    for update in updates:
        if update["title"] == update_news:
            del update

def del_news(headline:str):
    for article in news:
        if article['title']==headline:
            del article

@apps.route('/index')
def base():
    
    news = news_API_request(api_base_url=config["api_base_url"],
                            api_country=config["api_country"],
                            covid_terms=config["terms"],
                            api_key_input=config["api_key"])
    
    s.run(blocking=False)
    
    # Obtaining arguements entered in the server by the user
    label = str(request.args.get('two'))
    date = request.args.get('update')
    cov_button = request.args.get("covid-data")
    repeat_button = request.args.get("repeat")
    news_button = request.args.get("news")
    delete_update = request.args.get("update_item")
    delete_news = request.args.get("notif")
    
    # states the functions to run depending on the buttons selected on the website
    if date:
        add_updates(a=label,b=date)
        
    if delete_update:
        del_update(delete_update)
        
    if delete_news:
        news = del_news(delete_news)
        
    if news_button:
        schedule_covid_updates(update_interval=date,update_name=update_news)
        
    
    if cov_button:
        update_covid(update_interval,update_name)
    
    # what appears when you go to the website
    return render_template('index.html',
                           title='Covid updates UK',
                           location=config["local_location"],
                           local_7day_infections=str(old_covid_data[1]),
                           nation_location=config["nation_location"],
                           national_7day_infections=str(old_covid_data[0]),
                           hospital_cases='Current hospital cases: '+str(old_covid_data[3]),
                           deaths_total='Total deaths: '+str(old_covid_data[2]),
                           updates=updates,
                           news_articles=news,
                           image = config['image']
                          )

if __name__=='__main__':
    apps.run(debug=False)