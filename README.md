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