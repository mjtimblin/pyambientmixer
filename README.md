# pyAmbientMixer - a Python player with Pygame to play ambient-mixer.com mixes locally.

This little hacked script is here to allow people to download and play ambient mixes stored on ambient-mixer.com. It's not really "out for all users", but it works enough to be public.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You'll need python3 installed on your system, with the python packages contained in requirements.txt.

If you're on a 'bian system, you can install python3 and pip with

`sudo apt install python3 python3-pip`

I recommend pip to install the required modules. Install them with

`sudo pip3 install -r requirements.txt`

## Downloading a mix

Easy. Get to the mix you'd like to keep. In this example, I went with "**Night in a Medieval Monastery**".

Just run python -m src.main --url` with the url.

In our example :

`python -m src.main --url http://religion.ambient-mixer.com/night-in-a-medieval-monastery`

Once the downloads are complete, the mix will start playing. You will also see a line printed to the console, like this:

`Environment saved as id: ambient-mixer_environment_48152`

Once the mix is initially downloaded, you can play it again without making any web requests to ambient-mixer by running

`python -m src.main --environment ambient-mixer_environment_48152`

The environment details can be found `data/environments.json`.

### Playing the mix

Once you downloaded your mix, and you've converted the files, just play it with ```ambient.py``` as such :
`python3 ambient.py presets/night-in-a-medieval-monastery.xml`

You should see 
```
Loaded Channel 0 : Gregorian Chant 2 (looping), 3677.ogg (volume 21, balance 0).
Loaded Channel 1 : old Castle Background (looping), (volume 100, balance 0)
Loaded Channel 2 : Burning Torches (looping), (volume 71, balance 0)
Loaded Channel 3 : Door open with creak and close (random 1 per 10m), (volume 21, balance 0)
Loaded Channel 4 : Flipping through large book (random 1 per 1m), (volume 71, balance 0)
Loaded Channel 5 : Small Group Whispering (random 5 per 10m), (volume 61, balance 0)
Loaded Channel 6 : echoing steps (looping), (volume 100, balance 0)
Loaded Channel 7 : Writing with a quill (looping), (volume 96, balance 0)
```

Relax and enjoy your mix! :)

### TODOS and possible bugs

So far, everything should work fine, except Crossfade (which is a TODO).
The random playing times can act funny.
There is no GUI, and no possibility of changing files "on the fly". Feel free to fork and continue this project. ^^

## Authors

* **Philooz** - *Initial work* - [Philooz](https://github.com/Philooz)
* **mjtimblin** - *Code refactor* - [mjtimblin](https://github.com/mjtimblin)

## License

This project is licensed under the GPL License - see the [LICENSE](LICENSE.md) file for details

## Acknowledgments

* Thanks to ambient-mixer.com website
* Huge thanks to the makers of the awesome python modules
* You for downloading this!
