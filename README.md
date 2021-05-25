# PlanetTerp API
This is <a href="https://api.planetterp.com">PlanetTerp's API</a>. <a href="https://planetterp.com">PlanetTerp</a> is a website designed to help students at the University of Maryland — College Park make informed decisions.

To run locally, you will need a local copy of PlanetTerp's database. This will be available publicly soon; for now, please email us for the database.

Once you have the repository, install <a href="https://webpy.org/">web.py</a>, navigate to the repository's directory, and run `python app.py`. You may need to do a couple other steps. Once everything is set up, visit `http://0.0.0.0:8080` (or whatever URL was listed in your console) to access the API.

If you find any issues, please open a ticket here, or email us at <a href="mailto:admin@planetterp.com">admin@planetterp.com</a>.


## Building docs

We build the docs with [widdershins](https://github.com/Mermade/widdershins) and [slate](https://github.com/slatedocs/slate).

First, install widdershins and clone the slate repo, as instructed in the respective setup guides.

Then run the following, replacing paths as appropriate:

```bash
widdershins '/Users/tybug/Desktop/coding/PlanetTerp-API/documentation/documentation.yaml' -o '/Users/tybug/Desktop/coding/slate/source/index.html.md' --shallowSchemas true
# build the html
bundle exec middleman build
# run the server locally
bundle exec middleman server
```
