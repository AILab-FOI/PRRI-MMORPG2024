extends PopupMenu

var TileInstance = preload("res://panels/tile.tscn")


var Main = null

# Called when the node enters the scene tree for the first time.
func _ready():
	Main = get_tree().root.get_child(0)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

func _open_size_menu():
	$SizeMenu.popup()

func _on_id_pressed(id):
	match id:
		0:
			_open_size_menu()


func _on_size_menu_map_size_changed( width: int, height: int ):
	%Layer.set_size( Vector2( Main.g_TileSize * width, Main.g_TileSize * height ) )
	for child in %Layer.get_children():
		%Layer.remove_child(child)
	
	for y in range( 0, height ):
		for x in range( 0, width ):
			var newTile = TileInstance.instantiate()
			newTile.name = str( (y * width) + x )
			%Layer.add_child(newTile)
			newTile.set_size( Vector2( Main.g_TileSize, Main.g_TileSize ) )
			newTile.set_position( Vector2( x * Main.g_TileSize, y * Main.g_TileSize ) )
