from flask import Flask
from flask import render_template
from flask import request
import os
import urllib3
import json
import time

app = Flask(__name__)

def get_weather(city):
    api_key = '7efef948c90f4679814125302232410'
    url = 'http://api.weatherapi.com/v1/forecast.json'
    params = {
        'key' : api_key,
        'q' : city,
        'days' :'5'
    }
    http = urllib3.PoolManager()
    response = http.request('GET', url,fields=params)
    return response



@app.route("/")
def index():
    searchcity = request.args.get('searchcity')
    if not searchcity:
        searchcity = 'Chennai'
    return format_weather_data(searchcity)
    #return get_weather()

def format_weather_data(searchcity):
   
    data = json.loads(get_weather(searchcity).data.decode('utf-8'))
    try:
        location = data.get('location').get('name')
        forcastDate = data.get('forecast').get('forecastday')
    except AttributeError:
        return render_template('invalidcity.html', searchcity = searchcity)
    
  
   
    
    forecastw = []
    for day in forcastDate:
        days = []
        days.append(day.get('date'))
       
        days.append(day.get('day').get('maxtemp_c'))
        days.append( day.get('day').get('mintemp_c') )
        days.append( day.get('day').get('condition').get('text') )
        forecastw.append(days)
        print(forecastw)
   

    # page = '<html> <head><title> Weather Forcast </title></head> <body> '
    # page+= '<h1> Weather Forcast for {}</h1>  <p>{} </p>'.format(location, forcastDate)
    # page+= '</body></html>'
    # return page
    return render_template('index.html', location=location,forecast = forecastw )

@app.route("/hello/<name>")
def hello(name):
    return "Hello, {}".format(name)



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000));
    app.run(host='0.0.0.0',port=port, debug=True )
