extends Control

var LayerInstance = preload("res://panels/layer.tscn")
var TileInstance = preload("res://panels/tile.tscn")

var dragging = false
var painting = false
var clearing = false

var Main = null

var layers = {}

# Called when the node enters the scene tree for the first time.
func _ready():
	Main = get_tree().root.get_child(0)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

func _recalc_layer_order():
	var sortedOrder = layers.keys()
	sortedOrder.sort()
	
	print(sortedOrder)
	
	var localOrder = 0
	for order in sortedOrder:
		var layer = layers[order]
		var index = -1
		for i in %LayerList.item_count:
			if( %LayerList.get_item_text(i) == layer.name ):
				index = i
				break
		
		%LayerList.move_item(index, localOrder)
		localOrder += 1

	for order in range( sortedOrder.size()-1, -1, -1):
		var index = sortedOrder[order]
		remove_child(layers[index])
		add_child(layers[index])

func put_layer_in_order( layer, order ):
	var originalOrder = layer.order
	layer.order = order

	if( !layers.keys().is_empty() && layers.has(order) ):
		if( originalOrder == -1 ):
			for i in range( layers.keys().max(), order-1, -1 ):
				layers[i+1] = layers[i]
				layers[i+1].order = i+1
		elif( originalOrder > layer.order ):
			for i in range( originalOrder, layer.order, -1 ):
				layers[i] = layers[i-1]
				layers[i].order = i
		elif( originalOrder < layer.order ):
			for i in range( originalOrder, layer.order, 1 ):
				layers[i] = layers[i+1]
				layers[i].order = i
	
	layers[layer.order] = layer

func add_layer(name: String, type: String, order: int = -1):
	var tile_layer = LayerInstance.instantiate()
	tile_layer.name = type + "_" + name
	tile_layer.type = type
	
	if( order == -1 ):
		order = 0
	
	tile_layer.order = -1
	
	put_layer_in_order(tile_layer, order)
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
	var order = -1
	
	for layer in layers.values():
		if( layer.name == name ):
			order = layer.order
			break
	
	var layer = layers[order]
	
	var newOrder = max(0, min(order + direction, layers.keys().max()))
	
	layers.erase( order )
	put_layer_in_order(layer, newOrder)
	
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
