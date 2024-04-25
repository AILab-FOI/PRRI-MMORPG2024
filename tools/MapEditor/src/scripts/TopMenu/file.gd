extends PopupMenu

signal assets_loaded

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

func _scan_folder_for_materials(dir: DirAccess):
	var files = dir.get_files()
	var dirs = dir.get_directories()
	for file in files:
		var fullPath = dir.get_current_dir()+"/"+file
		var relativePath = fullPath.replace(Main.g_AssetPath, "")
		
		if( not file.ends_with(".material") ):
			continue
		
		var rawFile = FileAccess.open(fullPath, FileAccess.READ)
		if not rawFile:
			print("Dang")
			continue
		
		print(rawFile.get_as_text())
		
		var json = JSON.parse_string(rawFile.get_as_text())
		if( not json ):
			continue
		
		print(json["type"])
		
		if( json["type"] != "sprite" ):
			continue
		
		var imagePath = Main.g_AssetPath + "/" + json["path"]
		
		var rawImage = Image.load_from_file(imagePath)
		if rawImage:
			var imageTexture = ImageTexture.create_from_image(rawImage)
			Main.g_Materials[relativePath] = imageTexture
	
	for subpath in dirs:
		var subdir := DirAccess.open(dir.get_current_dir()+"/"+subpath)
		if subdir:
			_scan_folder_for_materials(subdir)

func _on_file_dialog_dir_selected(path):
	Main.g_AssetPath = path
	var test: Texture2D = null

	Main.g_Materials.clear()
	Main.g_SelectedTexture = null
	
	var dir:DirAccess = DirAccess.open(Main.g_AssetPath+"/"+"materials")
	if dir:
		_scan_folder_for_materials(dir)
	
	$OpenFile.set_current_dir(Main.g_AssetPath+"/"+"maps")
	
	assets_loaded.emit()


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
		var node = %Layer.get_node( str(index) )
		if( material != "" ):
			node.m_Material = material
			node.texture = Main.g_Materials[material]
