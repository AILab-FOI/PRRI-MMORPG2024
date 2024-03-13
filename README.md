# PRRI-MMORPG2024

A fantasy MMORPG game based on Stanislav Petrov's [Sprite Stacking project](https://github.com/StanislavPetrovV/SpriteStacking) developed by students in the [Artificial Intelligence Laboratory](https://ai.foi.hr/) at the [University of Zagreb Faculty of Organization and Informatics](https://www.foi.unizg.hr/). The game is developed using the [PyGame](https://www.pygame.org/). More details available at [itch.io](https://ailab-foi.itch.io/prri-mmorpg2024).

# Short intro

To start the game you first need to start the ZEO database server

```
runzeo -C zeo.conf
```

Then you need to start the web socket server:

```
./server.py
```

And in the end one or more clients by supplying username and password:

```
./main.py --username USER --password PASS
```
