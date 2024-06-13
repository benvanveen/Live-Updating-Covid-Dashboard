# Bens Updating Covid Dashboard

https://github.com/BvanVeen01/Bens-Covid-Dashboard

## Introduction:

- The purpose of this project is to create a covid dashboard that displays current covid data and news articles, which the user can also schedule updates for.


## Prerequisites:

- this code was written in Python 3


## Installation:

- flask: ```pip install Flask```
- UK covid API: ```pip install uk-covid19```
- pytest: ```pip install pytest```


## Getting Started:

- **To run the code to create the dashboard**: make sure all the files in the file are downloaded onto your computer and then run the code in **main.py**

- **navigating to the dashboard**: Open a browser and go to http://127.0.0.1:5000/index

- **using the dashboard**: Type in a title for your update and schedule a time for it to happen, select update covid data or update news   updates to schedule updates for these parts of the dashboard.


## Testing:

- the functions in **test_covid_data_handler** and **test_news_data_handling** can be used test their equivalent functions.


## Developer Documentation:

- **covid_news_handling.py**: this python file contains the functions which access and update covid related news articles from the news API.

- **covid_data_handler.py**: this python file contains the functions related to accessing and processing the covid data from the UK-covid API.

- **main.py**: this is the python file which all of the functions are imported into to be applied to the web server and then run it, this is also where the inputs from the dashboard are defined.

- **templates**: this folder contains the template for which the dashboard fits into, if you would wish to edit or add to the display make the changes to **index.html** in the folder.

- **static**: this folder contains static files such as images, if you would like to add or change any images on the dashboard this is where to save those images to.

- **tests**: this folder contains the python files for testing the code.

- **config.json**: all aspects of the code to personalise the dashboard is found in this cofiguration file.

- **sys.txt**: this is a document which contains all the logged information from the dashboard, such as general inputs and errors.

for more information on the induvidual python files, open the file and read the doc strings in the code.


## Details:

- **Authors**: Benjamin van Veen

- **Acknowledgements**: This dashboard is dependant on the UK-Covid API from https://pypi.org/project/uk-covid19/ and also news articles from https://newsapi.org/v2/top-headlines?