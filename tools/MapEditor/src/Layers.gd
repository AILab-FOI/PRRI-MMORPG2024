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

func add_layer(name):
	var tile_layer = LayerInstance.instantiate()
	tile_layer.name = "tiles_" + name
	tile_layer.order = layers.size()
	Main.g_Layers.add_child(tile_layer)
	
	layers.push_back(tile_layer)
	%LayerList.add_item( tile_layer.name )
	
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
