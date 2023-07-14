import httpx
from prefect import flow,task,get_run_logger


@task(retries = 2)
def weather_fetch(lat,lon):
    logger=get_run_logger()
    param=dict(latitude=lat, longitude = lon,hourly="temperature_2m")
    base_url = "https://api.open-meteo.com/v1/forecast"
    res = httpx.get(base_url,params=param)
    most_recent_temp= float(res.json()['hourly']['temperature_2m'][0])
    logger.info("temp is", str(most_recent_temp))
    return most_recent_temp
    
@task(retries = 2)
def save_csv(temp):
    with open("temp.csv","w+") as s:
        s.write(str(temp))
    return "successfully saved in csv"

@flow(retries = 3)
def pipeline(la,lo):
    logger=get_run_logger()
    logger.info("executing pipeline")
    temp_val=weather_fetch(la,lo)
    save_csv_val=save_csv(temp_val)
    logger.info("completed pipeline")



if __name__ == "__main__":
    pipeline(la,lo)

