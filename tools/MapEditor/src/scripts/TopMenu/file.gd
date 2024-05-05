extends PopupMenu

var Main = null

# Called when the node enters the scene tree for the first time.
func _ready():
	Main = get_tree().root.get_child(0)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

func _on_open_assets_pressed():
	$AssetDialog.popup()

func _open_save_file_menu():
	$SaveFile.popup()

func _open_open_file_dialog():
	$OpenFile.popup()

func _on_id_pressed(id):
	match id:
		0:
			_on_open_assets_pressed()
		1:
			_open_save_file_menu()
		2:
			_open_open_file_dialog()

func _on_file_dialog_dir_selected(path):
	Main.set_asset_path(path)
	
	$OpenFile.set_current_dir(Main.g_AssetPath+"/"+"maps")


func _on_open_file_file_selected(path):
	var mapFile: String = FileAccess.get_file_as_string(path)
	var mapObject: Dictionary = JSON.parse_string(mapFile)
	
	print(mapObject)
	var size = str_to_var("Vector2" + mapObject["size"])
	Main.change_map_size(size)
	
	for str_coords in mapObject["layers"]["tiles_1"].keys():
		var coords = str_to_var("Vector2" + str_coords)
		var material = mapObject["layers"]["tiles_1"][str_coords]
		var index = (size.x * coords.y) + coords.x
		var node = %Layers.get_node( str(index) )
		if( material != "" ):
			node.m_Material = material
			node.texture = Main.g_Materials[material]
