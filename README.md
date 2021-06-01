# PlanetTerp API

This is [PlanetTerp's API](https://api.planetterp.com). [PlanetTerp](https://planetterp.com) is a website designed to help students at the University of Maryland — College Park make informed decisions.

To run locally, you will need a local copy of PlanetTerp's database. This will be available publicly soon; for now, please email us for the database.

Once you have the repository, install [web.py](https://webpy.org/), navigate to the repository's directory, and run `python app.py`. You may need to do a couple other steps. Once everything is set up, visit `http://0.0.0.0:8080` (or whatever URL was listed in your console) to access the API.

If you find any issues, please open a ticket here, or email us at [admin@planetterp.com](mailto:admin@planetterp.com)

## Building docs

We build the docs with [widdershins](https://github.com/Mermade/widdershins) and [slate](https://github.com/slatedocs/slate).

First, install widdershins and clone the slate repo, as instructed in their respective setup guides.

Then run the following, replacing paths as appropriate:

```bash
widdershins '/Users/tybug/Desktop/coding/PlanetTerp-API/documentation.yaml' -o '/Users/tybug/Desktop/coding/slate/source/index.html.md' --shallowSchemas true
# manually add new "usage" section
sed -i '' 's/<h1 id="planetterp-api-courses">Courses<\/h1>/\
# Usage\
\
The API does not require any authentication. There are no hard rate limits, but please take a pause between each request.\
\
The API has a [Python wrapper](https:\/\/github.com\/planetterp\/PlanetTerp-API-Python-Wrapper) on GitHub.\
\
If you'\''re new to interacting with APIs, [we'\''ve written an example program in python using the api](https:\/\/gist.github.com\/tybug\/3fcebc8a2b63d471270bda86f0756cdf) for you to follow along with.\
\
<h1 id="planetterp-api-courses">Courses<\/h1>\
/g' '/Users/tybug/Desktop/coding/slate/source/index.html.md'
# cd into slate
cd /Users/tybug/Desktop/coding/slate/
# build the html
bundle exec middleman build
# run the server locally (if you want a preview)
bundle exec middleman server
# move the built html files to planetterp-api
mv build/* /Users/tybug/Desktop/coding/PlanetTerp-API/static
# delete garbage temp files
rm /Users/tybug/Desktop/coding/PlanetTerp-API/static/index.html.md.bak
rm /Users/tybug/Desktop/coding/PlanetTerp-API/static/index.html.md.old
# double escape dollar signs for webpy
sed -i '' 's/\$/$$/g' '/Users/tybug/Desktop/coding/PlanetTerp-API/static/index.html'
# make relative includes play nice with webpy
sed -i '' 's/stylesheets\//static\/stylesheets\//g' '/Users/tybug/Desktop/coding/PlanetTerp-API/static/index.html'
sed -i '' 's/images\//static\/images\//g' '/Users/tybug/Desktop/coding/PlanetTerp-API/static/index.html'
sed -i '' 's/fonts\//static\/fonts\//g' '/Users/tybug/Desktop/coding/PlanetTerp-API/static/index.html'
sed -i '' 's/javascripts\//static\/javascripts\//g' '/Users/tybug/Desktop/coding/PlanetTerp-API/static/index.html'
```
