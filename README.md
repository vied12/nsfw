# Neukölln Service for Feinstaub Warning (NSFW)
*Berlin, July 2016*

We are collecting the daily reports from [Umweltbundesamt](https://www.umweltbundesamt.de/en/data/current-concentrations-of-air-pollutants-in-germany) air quality stations network in Germany and give you a chance to track them by receiving alerts via email or rss.

http://nsfw.herokuapp.com/

# Install and run

```bash
pip install -r requirements.txt
npm install
bower install
# collect yesterday reports
./manage.py yesterday
# launch the web application
./manage.py runserver
```

# Contributions

Developed by <a href="https://twitter.com/vied12" target="_blank">Edouard</a>,
from a brillant idea of <a href="https://twitter.com/jmi" target="_blank">Jan</a>,
an illustration from <a href="https://www.flickr.com/photos/davdenic/20265152826/" target="_blank">David Denicolò</a>
with the helpful Carmen's advices
and the <a href="https://www.umweltbundesamt.de/en/data/current-concentrations-of-air-pollutants-in-germany" target="_blank">UBA's data</a>.
