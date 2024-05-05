extends Control

var g_AssetPath = "ASSET PATH NOT SELECTED"
var g_Materials: Dictionary = {}

# How big the tiles are IN EDITOR, not in game
var g_TileSize = 32

var g_SelectedTexture = null
var g_SelectedTextureName = ""

var g_EditorVersion = "1"

var g_MapSize: Vector2 = Vector2( 0, 0 )

var g_Layers = null

# Called when the node enters the scene tree for the first time.
func _ready():
	g_Layers = %Layers
	print(%Layers)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

func change_map_size(size: Vector2):
	g_MapSize = size
	var width = size.x
	var height = size.y
	
	g_Layers.set_size( Vector2( g_TileSize * width, g_TileSize * height ) )
	for child in g_Layers.get_children():
		g_Layers.remove_child(child)
	
	var layerList: ItemList = %LayerList
	layerList.clear()
	
	g_Layers.add_layer("1")
	
	for layer: Node in g_Layers.get_children():
		g_Layers.move_child(layer, -1 - layer.order )

func _scan_folder_for_materials(dir: DirAccess):
	var files = dir.get_files()
	var dirs = dir.get_directories()
	for file in files:
		var fullPath = dir.get_current_dir()+"/"+file
		var relativePath = fullPath.replace(g_AssetPath + "/", "")
		
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
		
		if( json["type"] != "sprite" and json["type"] != "tile" ):
			continue
		
		var imagePath = g_AssetPath + "/" + json["path"]
		
		var rawImage = Image.load_from_file(imagePath)
		if rawImage:
			var imageTexture = ImageTexture.create_from_image(rawImage)
			g_Materials[relativePath] = imageTexture
	
	for subpath in dirs:
		var subdir := DirAccess.open(dir.get_current_dir()+"/"+subpath)
		if subdir:
			_scan_folder_for_materials(subdir)

func set_asset_path( path: String ):
	g_AssetPath = path
	var test: Texture2D = null

	g_Materials.clear()
	g_SelectedTexture = null
	
	var dir:DirAccess = DirAccess.open(g_AssetPath+"/"+"materials")
	if dir:
		_scan_folder_for_materials(dir)
	
	_on_file_assets_loaded()

func _on_file_assets_loaded():
	var itemList: ItemList = %MaterialList
	itemList.clear()
	
	for name in g_Materials.keys():
		itemList.add_item( name, g_Materials[name] )
		print( name )
	
	_enable_asset_locked_options()
	
func _enable_asset_locked_options():
	for child: PopupMenu in %TopMenu.get_children():
		for item in child.item_count:
			child.set_item_disabled(item, false)

func _on_item_list_item_selected(index):
	var materialList = %MaterialList
	if( materialList.get_selected_items().is_empty() ):
		return
		return
	var matName = materialList.get_item_text(index)
	g_SelectedTexture = g_Materials[matName]
	g_SelectedTextureName = matName

func _on_save_file_save_file(filename: String):
	var savePath = g_AssetPath + "/maps"
	var filePath = savePath + "/" + filename + ".map"
	
	var dir := DirAccess.open(savePath)
	if( not dir ):
		DirAccess.make_dir_recursive_absolute(savePath)
		dir = DirAccess.open(savePath)
		if( not dir ):
			return

	var map: Dictionary = {}
	map["editor_version"] = g_EditorVersion
	map["size"] = g_MapSize
	map["layers"] = {}
	
	if( g_MapSize != Vector2( 0, 0 ) ):
		map["layers"]["tiles_1"] = {}
		
		for tile in g_Layers.get_node("tiles_1").get_children():
			if( tile.texture == null ):
				continue
			
			if( tile.m_Material == null ):
				continue
			
			var coord = Vector2(tile.position.x / g_TileSize, tile.position.y / g_TileSize)
			print(coord)
			map["layers"]["tiles_1"][coord] = tile.m_Material

	var file = FileAccess.open(filePath, FileAccess.WRITE)
	file.store_line( JSON.stringify(map) )
	file.close()
