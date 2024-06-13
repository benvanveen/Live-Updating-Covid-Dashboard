def cases_7_days(loc:str,loc_type:str)->int:
    
    from covid_data_handler import covid_API_request
    
    # accesses current covid data
    data = covid_API_request(loc,loc_type)
    dates = data['data']
    cases_per_day=[]
    
    # creates a list of cases per day by publish date.
    for date in dates:
        new_cases = date['newCasesByPublishDate']
        cases_per_day.append(new_cases)
    
    # returns the cumulative cases of the last seven days, not including the first value as this one may not have been fully 
    # updated for that day
    return sum(cases_per_day[1:8])

def deaths_tot_and_hosp(loc:str,loc_type:str)->list:
    
    # to calculate cumulative deaths
    from covid_data_handler import covid_API_request
    data = covid_API_request(loc,loc_type)
    dates = data['data']
    deaths=[]
    for date in dates:
        deaths.append(date['cumDeaths28DaysByDeathDate'])
        
    # to calculate current hospital cases
    data = covid_API_request(loc,loc_type)
    dates = data['data']
    hosp=[]
    for date in dates:
        hosp.append(date['hospitalCases'])
    
    deaths_and_hosp=[]
    deaths_and_hosp.append(deaths[1])
    deaths_and_hosp.append(hosp[1])
    
    # returns a list with two values, with cumulative deaths being the first value and current hospital caes being the second.
    return deaths_and_hosp