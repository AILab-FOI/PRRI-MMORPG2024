# Table of Contents

* [bullet](#bullet)
* [cache](#cache)
  * [Cache](#cache.Cache)
    * [cache\_entity\_sprite\_data](#cache.Cache.cache_entity_sprite_data)
    * [create\_entity\_mask](#cache.Cache.create_entity_mask)
    * [cache\_stacked\_sprite\_data](#cache.Cache.cache_stacked_sprite_data)
    * [compile\_stacked\_sprite\_angles](#cache.Cache.compile_stacked_sprite_angles)
    * [create\_stack\_layer\_array](#cache.Cache.create_stack_layer_array)
* [client-test](#client-test)
* [client\_app](#client_app)
  * [ClientApp](#client_app.ClientApp)
    * [set\_local\_player](#client_app.ClientApp.set_local_player)
    * [set\_active\_scene](#client_app.ClientApp.set_active_scene)
    * [tick](#client_app.ClientApp.tick)
    * [update](#client_app.ClientApp.update)
    * [draw](#client_app.ClientApp.draw)
    * [check\_events](#client_app.ClientApp.check_events)
    * [get\_time](#client_app.ClientApp.get_time)
    * [connect](#client_app.ClientApp.connect)
    * [on\_message](#client_app.ClientApp.on_message)
    * [on\_error](#client_app.ClientApp.on_error)
    * [on\_open](#client_app.ClientApp.on_open)
* [config](#config)
* [draw\_manager](#draw_manager)
  * [LayerMask](#draw_manager.LayerMask)
  * [DrawManager](#draw_manager.DrawManager)
    * [set\_dirty](#draw_manager.DrawManager.set_dirty)
    * [add\_layer](#draw_manager.DrawManager.add_layer)
    * [add\_drawable](#draw_manager.DrawManager.add_drawable)
    * [remove\_drawable](#draw_manager.DrawManager.remove_drawable)
* [entity](#entity)
  * [WorldObject](#entity.WorldObject)
    * [is\_visible](#entity.WorldObject.is_visible)
    * [is\_in\_pov](#entity.WorldObject.is_in_pov)
    * [update\_visuals](#entity.WorldObject.update_visuals)
  * [BaseSpriteEntity](#entity.BaseSpriteEntity)
  * [Entity](#entity.Entity)
  * [RemotePlayer](#entity.RemotePlayer)
    * [should\_think](#entity.RemotePlayer.should_think)
* [entity\_system](#entity_system)
  * [EntitySystem](#entity_system.EntitySystem)
    * [add\_entity](#entity_system.EntitySystem.add_entity)
    * [remove\_entity](#entity_system.EntitySystem.remove_entity)
    * [think](#entity_system.EntitySystem.think)
    * [delete](#entity_system.EntitySystem.delete)
* [main](#main)
* [message](#message)
* [player](#player)
  * [Player](#player.Player)
* [scene](#scene)
  * [K](#scene.K)
* [server](#server)
  * [Player](#server.Player)
    * [login](#server.Player.login)
  * [handle\_connection](#server.handle_connection)
  * [handle\_connection](#server.handle_connection)
  * [register\_player](#server.register_player)
  * [login\_player](#server.login_player)
  * [logout\_player](#server.logout_player)
  * [update\_player\_position](#server.update_player_position)
  * [broadcast\_positions](#server.broadcast_positions)
* [shared](#shared)
  * [RES](#shared.RES)
  * [TILE\_SIZE](#shared.TILE_SIZE)
  * [BG\_COLOR](#shared.BG_COLOR)
  * [NUM\_ANGLES](#shared.NUM_ANGLES)
  * [ENTITY\_SPRITE\_ATTRS](#shared.ENTITY_SPRITE_ATTRS)
* [stacked\_sprite](#stacked_sprite)
* [tilemap](#tilemap)
  * [MapData](#tilemap.MapData)
  * [Layer](#tilemap.Layer)
    * [draw](#tilemap.Layer.draw)
  * [Material](#tilemap.Material)
  * [Tile](#tilemap.Tile)
    * [update\_screenpos](#tilemap.Tile.update_screenpos)
* [viewpoint](#viewpoint)

<a id="bullet"></a>

# bullet

<a id="cache"></a>

# cache

<a id="cache.Cache"></a>

## Cache Objects

```python
class Cache()
```

Cache base class

<a id="cache.Cache.cache_entity_sprite_data"></a>

#### cache\_entity\_sprite\_data

```python
def cache_entity_sprite_data()
```

Called when a scene loads.
Takes all the sprite data and saves it into the cache.

<a id="cache.Cache.create_entity_mask"></a>

#### create\_entity\_mask

```python
def create_entity_mask(attrs: dict, images: list) -> pg.Mask
```

Creates an entity mask

**Arguments**:

- `attrs` _ dict _ - Dictionary of attributes
- `images` _ list _ - Array of images
  

**Returns**:

- `Mask` - Entity mask

<a id="cache.Cache.cache_stacked_sprite_data"></a>

#### cache\_stacked\_sprite\_data

```python
def cache_stacked_sprite_data()
```

Caches stacked sprite data

**Yields**:

- `status` - whether it was done or not

<a id="cache.Cache.compile_stacked_sprite_angles"></a>

#### compile\_stacked\_sprite\_angles

```python
def compile_stacked_sprite_angles(obj_name: str, layer_array: list,
                                  attrs: dict)
```

Compiles the stacked sprite angles of a given stacked sprite

**Arguments**:

- `obj_name` _str_ - object's name
- `layer_array` _list_ - array of the slices
- `attrs` _dict_ - sprite attributes

<a id="cache.Cache.create_stack_layer_array"></a>

#### create\_stack\_layer\_array

```python
def create_stack_layer_array(attrs: dict) -> list
```

Creates a stack sprite layer array, returns the layer array in reverse order

**Arguments**:

- `attrs` _ dict _ - dictionary of attributes
  

**Returns**:

- `list` - layer array list in reverse

<a id="client-test"></a>

# client-test

<a id="client_app"></a>

# client\_app

<a id="client_app.ClientApp"></a>

## ClientApp Objects

```python
class ClientApp()
```

Client app base class

<a id="client_app.ClientApp.set_local_player"></a>

#### set\_local\_player

```python
def set_local_player(player: Player)
```

Set the local player

**Arguments**:

- `player` _Player_ - player to set local

<a id="client_app.ClientApp.set_active_scene"></a>

#### set\_active\_scene

```python
def set_active_scene(scene)
```

Sets the active scene

**Arguments**:

- `scene` _Scene_ - Scene to set as active

<a id="client_app.ClientApp.tick"></a>

#### tick

```python
def tick()
```

A single game tick

<a id="client_app.ClientApp.update"></a>

#### update

```python
def update()
```

Updates the systems

<a id="client_app.ClientApp.draw"></a>

#### draw

```python
def draw()
```

Draws the scene

<a id="client_app.ClientApp.check_events"></a>

#### check\_events

```python
def check_events()
```

Checks events

<a id="client_app.ClientApp.get_time"></a>

#### get\_time

```python
def get_time()
```

Gets the time

<a id="client_app.ClientApp.connect"></a>

#### connect

```python
def connect()
```

Connects self to websocket

<a id="client_app.ClientApp.on_message"></a>

#### on\_message

```python
def on_message(ws: websocket, message: Message)
```

On message received from websocket, updates the player based on message

**Arguments**:

- `ws` _ Websocket _ - Websocket
- `message` _ Message _ - Message

<a id="client_app.ClientApp.on_error"></a>

#### on\_error

```python
def on_error(ws: websocket, error)
```

On error

**Arguments**:

- `ws` _websocket_ - websocket
- `error` _error_ - error

<a id="client_app.ClientApp.on_open"></a>

#### on\_open

```python
def on_open(ws: websocket)
```

On open

**Arguments**:

- `ws` _websocket_ - websocked to open

<a id="config"></a>

# config

<a id="draw_manager"></a>

# draw\_manager

<a id="draw_manager.LayerMask"></a>

## LayerMask Objects

```python
class LayerMask(pg.sprite.LayeredUpdates)
```

Layermask class

**Arguments**:

- `pg` _pygame_ - pygame macro

<a id="draw_manager.DrawManager"></a>

## DrawManager Objects

```python
class DrawManager()
```

Draw Manager class

<a id="draw_manager.DrawManager.set_dirty"></a>

#### set\_dirty

```python
def set_dirty(repeats=2)
```

force a draw call update

**Arguments**:

- `repeats` _int, optional_ - number of times to redraw. Defaults to 2.

<a id="draw_manager.DrawManager.add_layer"></a>

#### add\_layer

```python
def add_layer(name: str, order: int)
```

adds a draw layer by name defined by the order

**Arguments**:

- `name` _string_ - layer name
- `order` _int_ - number of layer in order

<a id="draw_manager.DrawManager.add_drawable"></a>

#### add\_drawable

```python
def add_drawable(drawable)
```

adds a drawable object

**Arguments**:

- `drawable` _ object _ - the object to add

<a id="draw_manager.DrawManager.remove_drawable"></a>

#### remove\_drawable

```python
def remove_drawable(drawable)
```

removes a drawable object

**Arguments**:

- `drawable` _ object _ - the object to remove

<a id="entity"></a>

# entity

<a id="entity.WorldObject"></a>

## WorldObject Objects

```python
class WorldObject(object)
```

World Object base class for anything that is within the world
Handles displaying the object on the screen based on a given viewpoint

**Arguments**:

- `object` _ object _ - world object

<a id="entity.WorldObject.is_visible"></a>

#### is\_visible

```python
def is_visible() -> bool
```

If you can, at any point, see the object

**Returns**:

- `bool` - Returns the object's visibility

<a id="entity.WorldObject.is_in_pov"></a>

#### is\_in\_pov

```python
def is_in_pov() -> bool
```

Checks if the object is in our line of sight

**Returns**:

- `bool` - Returns true if the object is in the line of sight

<a id="entity.WorldObject.update_visuals"></a>

#### update\_visuals

```python
def update_visuals()
```

Called for every frame when in view

<a id="entity.BaseSpriteEntity"></a>

## BaseSpriteEntity Objects

```python
class BaseSpriteEntity(WorldObject)
```

BaseSpriteEntity class

**Arguments**:

- `WorldObject` _ WorldObject _ - _description_

<a id="entity.Entity"></a>

## Entity Objects

```python
class Entity(BaseSpriteEntity)
```

Base Entity class

**Arguments**:

- `BaseSpriteEntity` _ BaseSpriteEntity _ - _description_

<a id="entity.RemotePlayer"></a>

## RemotePlayer Objects

```python
class RemotePlayer(Entity)
```

<a id="entity.RemotePlayer.should_think"></a>

#### should\_think

```python
def should_think() -> bool
```

Checks whether the entity has behaviour to be called every frame

**Returns**:

- `bool` - Returns true if the entity has defined behaviour in the think function

<a id="entity_system"></a>

# entity\_system

<a id="entity_system.EntitySystem"></a>

## EntitySystem Objects

```python
class EntitySystem(object)
```

This is the Entity System base class.

**Arguments**:

- `object` _object_ - python base class

<a id="entity_system.EntitySystem.add_entity"></a>

#### add\_entity

```python
def add_entity(entity)
```

Adds an entity

**Arguments**:

- `entity` _ entity_type _ - entity to add

<a id="entity_system.EntitySystem.remove_entity"></a>

#### remove\_entity

```python
def remove_entity(index: int)
```

Removes an entity

**Arguments**:

- `index` _int_ - index/id of the entity in the dictionary to remove

<a id="entity_system.EntitySystem.think"></a>

#### think

```python
def think()
```

Entity function that executes every frame
If no behaviour, skips it

<a id="entity_system.EntitySystem.delete"></a>

#### delete

```python
def delete(entity)
```

Deletes an entity

**Arguments**:

- `entity` _entity_type_ - Entity to delete

<a id="main"></a>

# main

<a id="message"></a>

# message

<a id="player"></a>

# player

<a id="player.Player"></a>

## Player Objects

```python
class Player(BaseSpriteEntity)
```

Player base class

**Arguments**:

- `BaseSpriteEntity` _ BaseSpriteEntity _ - Sprite entity to create the player from

<a id="scene"></a>

# scene

<a id="scene.K"></a>

#### K

entity

<a id="server"></a>

# server

<a id="server.Player"></a>

## Player Objects

```python
class Player(persistent.Persistent)
```

Player's position model on the server

**Arguments**:

- `persistent` _ persistent _ - _description_

<a id="server.Player.login"></a>

#### login

```python
def login(password: str) -> bool
```

Logins the player

**Arguments**:

- `password` _ str _ - player's password
  

**Returns**:

- `bool` - whether login was successful

<a id="server.handle_connection"></a>

#### handle\_connection

```python
async def handle_connection(websocket, path: str)
```

Websocket server handling

**Arguments**:

- `websocket` _ websocket _ - _description_
- `path` _ string _ - _description_

<a id="server.handle_connection"></a>

#### handle\_connection

```python
async def handle_connection(websocket, path: str)
```

Handles websocket connection

**Arguments**:

- `websocket` _ websocket _ - _description_
- `path` _string _ - _description_

<a id="server.register_player"></a>

#### register\_player

```python
def register_player(player_id: str, password: str) -> bool
```

Registers the player

Note: last 4 lines will never be executed, connection to db won't be closed and transaction won't be committed.

**Arguments**:

- `player_id` _ str _ - player username
- `password` _ str _ - password string
  

**Returns**:

- `bool` - whether registration was successful

<a id="server.login_player"></a>

#### login\_player

```python
def login_player(player_id: str, password: str) -> bool
```

Logins the player

**Arguments**:

- `player_id` _ str_ - player's username
- `password` _ str _ - player's password
  

**Returns**:

- `bool` - login success

<a id="server.logout_player"></a>

#### logout\_player

```python
def logout_player(player_id: str, password: str)
```

Logs out the player

**Arguments**:

- `player_id` _ str _ - player's username
- `password` _ str _ - player's password

<a id="server.update_player_position"></a>

#### update\_player\_position

```python
def update_player_position(player_id: str, x: float, y: float)
```

_summary_

**Arguments**:

- `player_id` _str_ - player's username
- `x` _float_ - x coordinate
- `y` _float_ - y coordinate

<a id="server.broadcast_positions"></a>

#### broadcast\_positions

```python
async def broadcast_positions()
```

broadcasts the positions to all clients

<a id="shared"></a>

# shared

<a id="shared.RES"></a>

#### RES

vec2( 1600, 900 )

<a id="shared.TILE_SIZE"></a>

#### TILE\_SIZE



<a id="shared.BG_COLOR"></a>

#### BG\_COLOR

'white'  # olivedrab

<a id="shared.NUM_ANGLES"></a>

#### NUM\_ANGLES

multiple of 360 -> 24, 30, 36, 40, 45, 60, 72, 90, 120, 180

<a id="shared.ENTITY_SPRITE_ATTRS"></a>

#### ENTITY\_SPRITE\_ATTRS

mask_layer - index of the layer from which we get the mask for collisions
and is also cached for all angles of the object, set manually or by default 
equal to num_layer // 2

<a id="stacked_sprite"></a>

# stacked\_sprite

<a id="tilemap"></a>

# tilemap

<a id="tilemap.MapData"></a>

## MapData Objects

```python
class MapData(object)
```

MapData base class

<a id="tilemap.Layer"></a>

## Layer Objects

```python
class Layer(object)
```

Layer base class

<a id="tilemap.Layer.draw"></a>

#### draw

```python
def draw(screen)
```

Draws the layer on given screen

**Arguments**:

- `screen` _ reference _ - reference to the screen to draw on

<a id="tilemap.Material"></a>

## Material Objects

```python
class Material()
```

Base Material class

<a id="tilemap.Tile"></a>

## Tile Objects

```python
class Tile(WorldObject)
```

Tile base class with an image, x and y coordinates

**Arguments**:

- `WorldObject` _ WorldObject _ - Which class the tile inherits from

<a id="tilemap.Tile.update_screenpos"></a>

#### update\_screenpos

```python
def update_screenpos()
```

Updates the screen position of the tile

<a id="viewpoint"></a>

# viewpoint

