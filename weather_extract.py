import httpx
from prefect import flow


@flow
def weather_fetch(lat,lon):
    param=dict(latitude=lat, longitude = lon,hourly="temperature_2m")
    base_url = "https://api.open-meteo.com/v1/forecast"
    res = httpx.get(base_url,params=param)
    most_recent_temp= float(res.json()['hourly']['temperature_2m'][0])
    print("temp is", str(most_recent_temp))
    return most_recent_temp
    


if __name__ == "__main__":
    weather_fetch(52.52,13.41)
