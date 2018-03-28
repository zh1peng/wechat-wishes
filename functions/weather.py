from weather import Weather, Unit
weather = Weather(unit=Unit.CELSIUS)

# Lookup WOEID via http://weather.yahoo.com.

lookup = weather.lookup(560743)
condition = lookup.condition()
print(condition.text())

# Lookup via location name.

location = weather.lookup_by_location('dublin')
condition = location.condition()
print(condition.text())

# Get weather forecasts for the upcoming days.

forecasts = location.forecast()
for forecast in forecasts:
    print(forecast.text())
    print(forecast.date())
    print(forecast.high())
    print(forecast.low())
    
    
    
    
from weather import Weather, Unit
weather = Weather(unit=Unit.CELSIUS)
# Lookup via location name.
def weather_in(city_name):
    location = weather.lookup_by_location(city_name)
    condition = location.condition()
    msg=city_name+'\n Today:'+condition.text()+'\n'
# Get weather forecasts for the upcoming days.
    forecasts = location.forecast()
    for forecast in forecasts:
        msg=msg+forecast.date()+':'+forecast.text()+'\n Degree:'+forecast.low()+'~'+forecast.high()+'\n'
    return msg
