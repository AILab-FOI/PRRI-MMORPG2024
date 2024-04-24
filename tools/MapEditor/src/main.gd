extends Control

var g_AssetPath = ""
var g_Materials: Dictionary = {}

var g_TileSize = 32

var g_SelectedTexture = null

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


func _on_file_assets_loaded():
	var itemList: ItemList = $VBoxContainer/GridContainer/ScrollContainer/MaterialList
	itemList.clear()
	
	for name in g_Materials.keys():
		itemList.add_item( name, g_Materials[name] )
		print( name )


func _on_item_list_item_selected(index):
	var materialList = $VBoxContainer/GridContainer/ScrollContainer/MaterialList
	if( materialList.get_selected_items().is_empty() ):
		return
		return
	var matName = materialList.get_item_text(index)
	g_SelectedTexture = g_Materials[matName]
