# CDP-DB-SITE




## Description
This is a lightweight web application which is meant to be accessible from various older game consoles (Wii U, PS3, Xbox One, etc).

It displays a database of the current contents of my CD player, including:
* Disc name
* Disc position
* Disc group (CD, DVD, Xbox 360 game, etc)
* Image of disc

And can send requests to my Home Assistant instance, which in turn sends infrared output to the CD player to quickly locate and retrieve particular disks.

## What's next?

- Implement versatile configuration options
  - More than one CD player, different disc limits for each
- An animation-heavy frontend for pizzazz and lols
- Expand to a general game library management app
  - Integrate with Xbox/Steam/others
  - Show where ALL my games are, not just discs but also physical on various consoles
- Create or find a good database for disc label images


## Tech details

| Thing 	    | Other 	                                       |
|------------|-----------------------------------------------|
| Backend  	 | **Django**                                    |
| Frontend   | **HTML/CSS with jinja2 templates. NO JS**   	 |
| Database   | **SQLlite**                                   |


## Instructions
* Install the requirements with `pip install -r requirements.txt`
* Set the `settings.py`:
    * `CDP_SIZE` to the size of your CD player (mine is 300 discs)
      * *Create an issue if you want support for multi-player setups! Sony MegaStorage players can link together and share control*
    * `CDP_CDP_CONTROL_REDIR_URL` to the base URL that you wish to use to control the CD player. I have this linked to a webhook on my Home Assistant instance to send IR commands to my CD player
    * Add any desired host IPs into `ALLOWED_HOSTS` -- Like your server's IP locally or on the internet.
* Make database migrations with `python manage.py makemigrations cdp_db_site_app`  and `python manage.py migrate`
* Start the server with `python manage.py runserver 0.0.0.0:8000 ` (or any desired port number)

## Disclaimers
* This project is meant for personal use and is not intended to be secure or store secret information. Do not use this project to store private information!
  * By extension, don't host this on the open internet!