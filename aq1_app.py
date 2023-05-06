from flask import Flask, render_template
# import pandas as pd
# import matplotlib.pyplot as plt
# import openaq
# import datetime
# import pytz
from branca.colormap import StepColormap
import folium
from folium.features import DivIcon
from get_data import get_pm25

app = Flask(__name__)


##############################################

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/pm25")
def pm25():
    
    map_center = [13.743136, 100.55529]
    m = folium.Map(location=map_center, zoom_start=11)

    df_nrt = get_pm25()
    
    for index, row in df_nrt.iterrows():
        latlon = (row['lat'], row['lon'])
        info = f"PM2.5={row['val']}, {row['local_t_str']}"
        color = row['color']

        folium.Circle(latlon, 500, color=color,
                      fill_opacity=0.7,
                      fill=True).add_child(folium.Popup(info)).add_to(m)

    colormap = StepColormap(
        colors=['green', 'yellow', 'orange', 'red', 'purple', 'brown'],
        vmin=0, vmax=500,
        index=[0, 50, 100, 150, 200, 300, 500],
        caption='Value Range'
    )

    colormap.caption = 'PM2.5 Index'
    colormap.add_to(m)

    return render_template("pm25.html", map=m._repr_html_())



if __name__ == "__main__":
    app.run(debug=True)

