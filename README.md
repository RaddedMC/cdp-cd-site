# CDP-DB-SITE




## Description
This (in development) is a lightweight web application which is meant to be accessible from various older game consoles (Wii U, PS3, Xbox One, etc).

It displays a database of the current contents of my CD player, including:
* Disc name
* Disc position
* Disc group (CD, DVD, Xbox 360 game, etc)
* [Tentative] image of disc

And can send requests to my Home Assistant instance, which in turn sends infrared output to the CD player to quickly locate and retrieve particular disks.

## Goals

- Implement a lightweight (minimal javascript) frontend
- Create a backend which is fast and responsive even on low end hardware (1-2 CPU cores, ~1 GB RAM)
- Implement versatile configuration options
- Future goal: An animation-heavy frontend for pizzazz and lols


## Tech details

| Thing 	    | Other 	     |
|------------|-------------|
| Backend  	 | **Django**  |
| Frontend   | **TBD**   	 |
| Database   | **SQLlite** |


## Instructions
* Install the requirements with `pip install -r requirements.txt`
* Set the `settings.py`:
    * `CDP_SIZE` to the size of your CD player (mine is 300 discs)
      * *Create an issue if you want support for multi-player setups! Sony MegaStorage players can link together and share control*
    * `CDP_CDP_CONTROL_REDIR_URL` to the base URL that you wish to use to control the CD player. I have this linked to a webhook on my Home Assistant instance to send IR commands to my CD player
* Make database migrations with `python manage.py makemigrations cdp_db_site_app`  and `python manage.py migrate`

## Disclaimers
* This project is meant for personal use and is not intended to be secure or store secret information. Do not use this project to store private information!