# FARI - General welcome screen
⚠️⚠️⚠️ Legacy version : only used for the visual question answering demo from AIlab. Indeed, the website that hosts the demo (on ailab infrastructure) does not accept being embeded as an iframe (as the new version of the welcome screen requires)

The new version [here](https://github.com/FARI-brussels/Welcome-Screen) should be used for all other demos.
## Install
```
pip install -r requirements.txt
```
## Run
- First run the specific demo in local (Here it's Flet application)

- Next, make sure that the Strapi API is running somewhere (https://github.com/jbaudru/FARi-Strapi_contentmanager).

- Then, run the Welcome page where *x* is the ID of the desired Welcome page (see below). 
```
python3 main.py --id x
```
