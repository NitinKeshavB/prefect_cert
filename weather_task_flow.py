import httpx
from prefect import flow,task


@task
def weather_fetch(lat,lon):
    param=dict(latitude=lat, longitude = lon,hourly="temperature_2m")
    base_url = "https://api.open-meteo.com/v1/forecast"
    res = httpx.get(base_url,params=param)
    most_recent_temp= float(res.json()['hourly']['temperature_2m'][0])
    print("temp is", str(most_recent_temp))
    return most_recent_temp
    
@task
def save_csv(temp):
    with open("temp.csv","w+") as s:
        s.write(str(temp))
    return "successfully saved in csv"

@flow
def pipeline():
    print("executing pipeline")
    temp_val=weather_fetch(52.52,13.41)
    save_csv_val=save_csv(temp_val)
    print("completed pipeline")



if __name__ == "__main__":
    pipeline()

