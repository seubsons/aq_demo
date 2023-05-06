import pandas as pd
import matplotlib.pyplot as plt
import openaq
import datetime
import pytz
#from branca.colormap import StepColormap
# import folium
# from folium.features import DivIcon


def get_pm25():
    
    def get_color(val):
        if val <= 50:
            return 'green'
        elif val <= 100:
            return 'yellow'
        elif val <= 150:
            return 'orange'
        elif val <= 200:
            return 'red'
        elif val <= 300:
            return 'purple'
        else:
            return 'brown'


    api = openaq.OpenAQ()

    country = 'TH'
    city = 'Bangkok'

    stations = api.locations(city=city, country=country, parameter='pm25')

    # Get the current UTC time
    utc_now = datetime.datetime.now(pytz.utc)

    data_list = []
    for loc in stations[1]['results']:

        data = api.latest(city=city,
                          country=country,
                          location=loc['locations'],
                          parameter='pm25')

        if len(data[1]['results']) > 0:
            #print(loc['locations'])

            coord = data[1]['results'][0]['coordinates']
            lat = coord['latitude']
            lon = coord['longitude']
            val = data[1]['results'][0]['measurements'][0]['value']
            t = data[1]['results'][0]['measurements'][0]['lastUpdated']
            dt = datetime.datetime.fromisoformat(t)
            time_diff = utc_now - dt
            delay_hr = round(time_diff.total_seconds()/3600.0, 1)
            #print(lat, lon, val, t, delay_hr)

            data_list.append([lat, lon, val, t, delay_hr])

    df = pd.DataFrame(data_list, columns=['lat', 'lon', 'val', 't', 'delay_hr'])

    ## use only data within 24 hours
    df_nrt = df[df['delay_hr'] <= 24].copy()

    df_nrt['t'] = pd.to_datetime(df_nrt['t'])
    bangkok_tz = pytz.timezone('Asia/Bangkok')
    df_nrt['local_t'] = df_nrt['t'].dt.tz_convert(bangkok_tz)
    df_nrt['local_t_str'] = df_nrt['local_t'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df_nrt['color'] = df_nrt['val'].apply(get_color)

    return df_nrt
