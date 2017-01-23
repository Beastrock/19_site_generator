# Encyclopedia

This script generates static site converting [Devman encyclopedia](https://devman.org/encyclopedia/) markdown articles and then rendering them and index page by python template engine Jinja2. 
This is [generated site](https://beastrock.github.io/index.html).

## Getting started
`git clone https://github.com/Beastrock/19_site_generator.git`  
`pip install -r requirements.txt` 

## Launching
 `python site_generator.py`  

By default script will generate `*.html` files from `*.md` files from `./articles/` folder using **config.json**.  
If is needed to add new `*.md` files, change **config.json** accordingly.  


## Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
