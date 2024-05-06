extends Control

var LayerInstance = preload("res://panels/layer.tscn")
var TileInstance = preload("res://panels/tile.tscn")

var dragging = false
var painting = false
var clearing = false

var Main = null

var layers = []

# Called when the node enters the scene tree for the first time.
func _ready():
	Main = get_tree().root.get_child(0)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

func _sort_by_order( a, b ) -> bool:
	return a.order < b.order

func _recalc_layer_order():
	for index in layers.size():
		layers[index].order = index
	
	for layer in layers:
		var index = -1
		for i in %LayerList.item_count:
			if( %LayerList.get_item_text(i) == layer.name ):
				index = i
				break
		%LayerList.move_item(index, %LayerList.item_count-layer.order-1)

	for index in range( layers.size()-1, -1, -1):
		remove_child(layers[index])
		add_child(layers[index])

func add_layer(name: String, type: String, order: int = -1):
	var tile_layer = LayerInstance.instantiate()
	tile_layer.name = type + "_" + name
	tile_layer.type = type
	if( order == -1 ):
		tile_layer.order = layers.size()
	else:
		tile_layer.order = order
	Main.g_Layers.add_child(tile_layer)
	
	if( tile_layer.order < layers.size() ):
		layers.insert(tile_layer.order, tile_layer)
	else:
		layers.push_back(tile_layer)
	
	layers.sort_custom(_sort_by_order)
	%LayerList.add_item( tile_layer.name )
	_recalc_layer_order()
	
	var width = Main.g_MapSize.x
	var height = Main.g_MapSize.y
	
	var tileSize = Main.g_TileSize
	
	for y in range( 0, height ):
		for x in range( 0, width ):
			var newTile = TileInstance.instantiate()
			newTile.name = str( (y * width) + x )
			tile_layer.add_child(newTile)
			newTile.set_size( Vector2( tileSize, tileSize ) )
			newTile.set_position( Vector2( x * tileSize, y * tileSize ) )

func move_layer(name, direction):
	if( direction > 0 ):
		direction += 1
	
	var index = -1
	
	for i in range(layers.size()):
		if( layers[i].name == name ):
			index = i
			break
	
	var layer = layers[index]
	
	var newIndex = max(0, min(index + direction, layers.size()))
	
	layers.insert( newIndex, layer )
	
	if( direction > 0 ):
		layers.remove_at(index)
	else:
		layers.remove_at(index+1)
	
	_recalc_layer_order()

func get_top_visible_layer() -> Node:
	for index in range( get_child_count()-1, -1, -1 ):
		var child: Node = get_child(index)
		if( child.visible ):
			return child

	return null

func hide_untill_layer(name):
	var bHiding: bool = false
	
	for index in range( 0, get_child_count() ):
		var child: Node = get_child(index)
		child.visible = !bHiding
		if( child.name == name ):
			bHiding = !bHiding

func _on_gui_input(event:InputEvent):
	if event is InputEventMouseButton:
		painting = false
		clearing = false
		dragging = false

		match event.button_index:
			1:
				painting = event.pressed
			2:
				clearing = event.pressed
			3:
				dragging = event.pressed

	elif event is InputEventMouseMotion:
		var mouse_pos = get_local_mouse_position()
		mouse_pos /= Main.g_TileSize
		%Info_Label_XPos.text = "X: " + str(mouse_pos.x)
		%Info_Label_YPos.text = "Y: " + str(mouse_pos.y)
		
		if( not dragging ):
			return
		
		var position: Vector2 = self.get_position()
		
		position += event.relative
		self.set_position(position)


func _on_new_layer_menu_new_layer_added(name: String, type: String):
	add_layer(name, type)
