# This is a sample Python script.
import python_weather, asyncio, schedule, time, json
from tinydb import TinyDB, Query
import pandas as pd
from io import StringIO

# exec(open('main.py').read())
print('''
 __          ________       _______ _    _ ______ _____                       
 \ \        / /  ____|   /\|__   __| |  | |  ____|  __ \                      
  \ \  /\  / /| |__     /  \  | |  | |__| | |__  | |__) |                     
   \ \/  \/ / |  __|   / /\ \ | |  |  __  |  __| |  _  /                      
    \  /\  /  | |____ / ____ \| |  | |  | | |____| | \ \                      
  ___\/__\/   |______/_/   _\_\_|__|_|  |_|______|_|  \_\_______ ____  _____  
 |__   __| |  | |_   _| \ | |/ ____|   /\   | \ | |   /\|__   __/ __ \|  __ \ 
    | |  | |__| | | | |  \| | |  __   /  \  |  \| |  /  \  | | | |  | | |__) |
    | |  |  __  | | | | . ` | | |_ | / /\ \ | . ` | / /\ \ | | | |  | |  _  / 
    | |  | |  | |_| |_| |\  | |__| |/ ____ \| |\  |/ ____ \| | | |__| | | \ \ 
    |_|  |_|  |_|_____|_| \_|\_____/_/    \_\_| \_/_/    \_\_|  \____/|_|  \_\                                                                                                   
''')
print("Running script....")


async def getweather():
    db = TinyDB('db.json')
    client = python_weather.Client(format=python_weather.METRIC)

    weather = await client.find("Montreal Quebec")

    #  print(weather.current.temperature,"In montreal right now",sep=" // ")

    for forecast in weather.forecasts:
        Duplicata = Query()
        if not db.search(Duplicata.date == str(forecast.date)):
            print(forecast.date, "date not added. addings to database", sep=" ")
            db.insert(
                {'date': str(forecast.date), 'temperature': forecast.temperature, 'condiiton': str(forecast.sky_text)})
            print(str(forecast.date), forecast.sky_text, forecast.temperature)
        else:
            print("data already added")


    # TODO: review this whold ordeal down here
    r = open('db.json')
    data = json.load(r)
    dataob = StringIO(json.dumps(data['_default']))
    print(json.dumps(data['_default']))
    print(type(data))
    pandareader = pd.read_json(dataob, typ='frame', orient='index')
    pandareader.to_csv('out.csv')
    r.close()
    await client.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getweather())


def job():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getweather())

# schedule.every(10).minutes.do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
