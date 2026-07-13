import json
from collections import Counter

with open('weather.json', encoding='utf-8') as f:
    data = json.load(f)

# Current
cc = data['current_condition'][0]
print('=== Current ===')
print(f"Temp: {cc['temp_C']}°C, Feels: {cc['FeelsLikeC']}°C")
print(f"Weather: {cc['weatherDesc'][0]['value']}")
print(f"Humidity: {cc['humidity']}%")
print(f"Wind: {cc['windspeedKmph']} km/h {cc['winddir16Point']}")

# Daily forecasts
for day in data['weather']:
    print(f"\n=== {day['date']} ===")
    print(f"Max: {day['maxtempC']}°C, Min: {day['mintempC']}°C")
    
    rain_chances = []
    wind_speeds = []
    descs = []
    for h in day['hourly']:
        rain_chances.append(int(h['chanceofrain']))
        wind_speeds.append(int(h['windspeedKmph']))
        descs.append(h['weatherDesc'][0]['value'].strip())
    
    avg_rain = sum(rain_chances) // len(rain_chances)
    max_rain = max(rain_chances)
    avg_wind = sum(wind_speeds) // len(wind_speeds)
    max_wind = max(wind_speeds)
    
    common_desc = Counter(descs).most_common(1)[0][0]
    
    print(f"Weather: {common_desc}")
    print(f"Rain chance: avg {avg_rain}%, max {max_rain}%")
    print(f"Wind: avg {avg_wind} km/h, max {max_wind} km/h")
