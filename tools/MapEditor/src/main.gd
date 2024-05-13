extends Control

var EntityDisplay = preload("res://panels/entity_display.tscn")

var g_AssetPath = "ASSET PATH NOT SELECTED"
var g_Materials: Dictionary = {}
var g_Entities: Dictionary = {}

var g_TypeMapping = {
	"int" = int(),
	"float" = float(),
	"bool" = bool(),
	"str" = String(),
	"vec2" = Vector2(),
}

# Types that need to use .duplicate()
var g_Duplicate = [

]
#region CreateControl Funcs

func CreateNumberEdit(type: String) -> SpinBox:
	var ret: SpinBox = SpinBox.new()
	
	ret.allow_greater = true
	ret.allow_lesser = true
	ret.rounded = type == "int"
	
	if( ret.rounded == false ):
		ret.step = 0.00001
	
	return ret

func CreateBoolButton(type: String) -> CheckButton:
	var ret: CheckButton = CheckButton.new()
	
	return ret

func CreateLineEdit(type: String) -> LineEdit:
	var ret: LineEdit = LineEdit.new()
	
	return ret

func CreateVectorEdit(type: String) -> HBoxContainer:
	var ret = HBoxContainer.new()
	
	var xEdit = CreateNumberEdit("float")
	xEdit.name = "x"
	var yEdit = CreateNumberEdit("float")
	yEdit.name = "y"
	
	var xText = Label.new()
	xText.text = "x"
	var yText = Label.new()
	yText.text = "y"
	
	ret.add_child(xText)
	ret.add_child(xEdit)
	
	ret.add_child(yText)
	ret.add_child(yEdit)
	
	return ret
#endregion

#region Set Funcs

func SetNumberEdit(control: SpinBox, value):
	control.value = value

func SetBoolButton(control: CheckButton, value):
	control.button_pressed = value

func SetLineEdit(control: LineEdit, value):
	control.text = value

func SetVectorEdit(control: HBoxContainer, value):
	var x = control.get_node("x")
	var y = control.get_node("y")
	
	x.value = value.x
	y.value = value.y
#endregion

#region Get Funcs

func GetNumberEdit(control: SpinBox):
	return control.value

func GetBoolButton(control: CheckButton):
	return control.button_pressed

func GetLineEdit(control: LineEdit):
	return control.text

func GetVectorEdit(control: HBoxContainer):
	var x = control.get_node("x")
	var y = control.get_node("y")
	
	return Vector2(x.value, y.value)
#endregion


var g_ControlMapping = {
	"int" = Callable(self, "CreateNumberEdit"),
	"float" = Callable(self, "CreateNumberEdit"),
	"bool" = Callable(self, "CreateBoolButton"),
	"str" = Callable(self, "CreateLineEdit"),
	"vec2" = Callable(self, "CreateVectorEdit")
}

var g_ControlSet = {
	"int" = Callable(self, "SetNumberEdit"),
	"float" = Callable(self, "SetNumberEdit"),
	"bool" = Callable(self, "SetBoolButton"),
	"str" = Callable(self, "SetLineEdit"),
	"vec2" = Callable(self, "SetVectorEdit")
}

var g_ControlGet = {
	"int" = Callable(self, "GetNumberEdit"),
	"float" = Callable(self, "GetNumberEdit"),
	"bool" = Callable(self, "GetBoolButton"),
	"str" = Callable(self, "GetLineEdit"),
	"vec2" = Callable(self, "GetVectorEdit")
}

func ConstructTypeBasedOnString(str: String) -> Variant:
	if( g_Duplicate.has(str) ):
		return g_TypeMapping[str].duplicate()
	else:
		var newVar = g_TypeMapping[str]
		return newVar

func GetTypeStringBasedOnVar( variable: Variant ) -> String:
	for typeName in g_TypeMapping.keys():
		var type = g_TypeMapping[typeName]
		if( typeof(type) == typeof(variable) ):
			return typeName
	
	return "TYPE_NOT_FOUND"

# How big the tiles are IN EDITOR, not in game
var g_TileSize = 32

var g_SelectedTexture = null
var g_SelectedTextureName = ""

var g_SelectedEntity: Button = null :
	get:
		return %EntityList.selected_item

var g_EditorVersion = "1"

var g_MapSize: Vector2 = Vector2( 0, 0 )

var g_Layers = null
var g_EntValues = null

var g_MousePos: Vector2 = Vector2(0,0)

# Called when the node enters the scene tree for the first time.
func _ready():
	g_Layers = %Layers
	g_EntValues = %EntValues

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
	
	g_Layers.layers.clear()
	
	var layerList: ItemList = %LayerList
	layerList.clear()
	
	g_Layers.add_layer("1", "tiles")
# Unneeded as of now
#	for layer: Node in g_Layers.get_children():
#		g_Layers.move_child(layer, -1 - layer.order )

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

func _load_entity( entityList, name ) -> Variant:
	if( g_Entities.has(name) ):
		return g_Entities[name]
	
	if( !entityList.has(name) ):
		return null
	
	var newEnt = {}
	
	var base: Variant = null
	if( entityList[name].has("base") ):
		base = _load_entity(entityList, entityList[name]["base"])
	
	if( base ):
		for key in base.keys():
			newEnt[key] = base[key]
	
	if( entityList[name].has("attr") ):
		for key in entityList[name]["attr"]:
			newEnt[key] = entityList[name]["attr"][key]
	
	g_Entities[name] = newEnt
	
	return newEnt

func _load_entity_list(dir: DirAccess):
	if( !dir.file_exists("entitylist.json") ):
		return

	var rawFile = FileAccess.open(dir.get_current_dir() + "/entitylist.json", FileAccess.READ)
	var json = JSON.parse_string(rawFile.get_as_text())
	if( not json ):
		return
	
	for entName in json.keys():
		_load_entity(json, entName)
	
	rawFile.close()

func set_asset_path( path: String ):
	g_AssetPath = path
	var test: Texture2D = null

	g_Materials.clear()
	g_SelectedTexture = null
	
	var dir:DirAccess = DirAccess.open(g_AssetPath+"/"+"materials")
	if dir:
		_scan_folder_for_materials(dir)
	
	dir = DirAccess.open(g_AssetPath+"/"+"entities")
	if( dir ):
		_load_entity_list(dir)
	
	_on_file_assets_loaded()

func _on_file_assets_loaded():
	var materialList: ItemList = %MaterialList
	materialList.clear()
	
	for name in g_Materials.keys():
		materialList.add_item( name, g_Materials[name] )
		print( name )

	var entityList: Node = %EntityList
	for child in entityList.get_children():
		entityList.remove_child(child)
		child.queue_free()

	for name in g_Entities.keys():
		var newEntity = EntityDisplay.instantiate()
		newEntity.set_entity(name)
		entityList.add_item(newEntity)
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
		for layer in g_Layers.get_children():
			map["layers"][layer.name] = {}
			map["layers"][layer.name]["data"] = {}
			map["layers"][layer.name]["order"] = get_child_count() - 1 - layer.get_index()
			if( layer.type == "tiles" ):
				for tile in layer.get_children():
					if( tile.texture == null ):
						continue
					
					if( tile.m_Material == null ):
						continue
					
					var coord = Vector2(tile.position.x / g_TileSize,
					tile.position.y / g_TileSize)
					
					print(coord)
					
					map["layers"][layer.name]["data"][coord] = tile.m_Material
			elif( layer.type == "entities" ):
				var index = 0
				for entity in layer.get_children():
					var entKey = str(index) + "_" + entity.entity_type
					map["layers"][layer.name]["data"][entKey] = entity.attr.duplicate()
					# HACK HACK
					for attrName in map["layers"][layer.name]["data"][entKey].keys():
						var attrib = map["layers"][layer.name]["data"][entKey][attrName]
						if typeof(attrib) == TYPE_VECTOR2:
							map["layers"][layer.name]["data"][entKey][attrName] = "vec2" + str(attrib)
					
					index += 1

	var file = FileAccess.open(filePath, FileAccess.WRITE)
	file.store_line( JSON.stringify(map) )
	file.close()
