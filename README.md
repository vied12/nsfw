# Neuköllner Stickoxid- und Feinstaub-Warnsystem (NSFW)
*Berlin, July 2016*

We are collecting the daily reports from [Umweltbundesamt](https://www.umweltbundesamt.de/en/data/current-concentrations-of-air-pollutants-in-germany) stations measuring air quality in Germany and give you the possibility to follow some of them by receiving alerts.

http://nsfw.fahrradfreundliches-neukoelln.de

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
with an illustration from <a href="https://www.flickr.com/photos/davdenic/20265152826/" target="_blank">David Denicolò</a>
and Carmen’s helpful design advices. Data provided by the <a href="https://www.umweltbundesamt.de/en/data/current-concentrations-of-air-pollutants-in-germany" target="_blank"><abbr title="Umweltbundesamt">UBA</abbr></a>.
Give us feedback on <a href="https://github.com/vied12/nsfw/issues" target="_blank">github</a> or <a href="mailto:nsfw@fahrradfreundliches-neukoelln.de">write us through email<a/> or <a href="http://twitter.com/radneukoelln">Twitter</a>.
