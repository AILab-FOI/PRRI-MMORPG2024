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

func _on_set_default_pressed():
	var defaultPaths = [
		"../../Circus/assets",
		"../../../Circus/assets"
	]
	
	var validPath = null
	
	for path in defaultPaths:
		var dir = DirAccess.open(path)
		if !dir:
			continue
		
		validPath = dir.get_current_dir()
		break

	if( validPath != null ):
		Main.set_asset_path(validPath)
		$OpenFile.set_current_dir(Main.g_AssetPath+"/"+"maps")
	else:
		$DefaultFail.show()
	

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
		3:
			_on_set_default_pressed()

func _on_file_dialog_dir_selected(path):
	Main.set_asset_path(path)
	
	$OpenFile.set_current_dir(Main.g_AssetPath+"/"+"maps")


func _on_open_file_file_selected(path):
	var mapFile: String = FileAccess.get_file_as_string(path)
	var mapObject: Dictionary = JSON.parse_string(mapFile)
	
	print(mapObject)
	var size = str_to_var("Vector2" + mapObject["size"])
	Main.change_map_size(size)
	
	var layers: Array = mapObject["layers"].values()
	layers.sort_custom( func(a, b): return a["order"] < b["order"] )
	
	for layer in layers:
		var key = mapObject["layers"].find_key(layer)
		var type: String = key
		var name: String = key
		var order: int = layer["order"]
		
		var typeEnd = type.find("_")
		type = type.substr(0, typeEnd)
		name = name.substr(typeEnd+1)
		
		var layerControl = null
		
		if( key != "tiles_1" ):
			layerControl = Main.g_Layers.add_layer(name, type, order)
		else:
			layerControl = %Layers.get_child(0)
		
		var data = layer["data"]
		
		if( type == "tiles" ):
			for str_coords in data.keys():
				var coords = str_to_var("Vector2" + str_coords)
				var material = data[str_coords]
				var index = (size.x * coords.y) + coords.x
				var node = layerControl.get_node( str(index) )
				if( material != "" ):
					node.m_Material = material
					node.texture = Main.g_Materials[material]
		elif( type == "entities" ):
			for entKey in data.keys():
				var entity = data[entKey]
				var entType = entKey.substr(entKey.find("_")+1)
				
				if( !entity.has("pos") ):
					continue

				var pos = str_to_var(entity["pos"].replace("vec2", "Vector2"))
				
				var newEnt = layerControl.create_entity(entType, pos)
				for attrName in entity.keys():
					var value = entity[attrName]
					if( typeof(value) == TYPE_STRING ):
						value = value.replace("vec2", "Vector2")
						if( str_to_var(value) != null ):
							value = str_to_var(value)

					print(type_string(typeof(value)))
					newEnt.set_attr(attrName, value)
