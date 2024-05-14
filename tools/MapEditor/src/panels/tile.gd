extends TextureRect

class_name Tile

var Main = null
var m_Material = ""

# Called when the node enters the scene tree for the first time.
func _ready():
	Main = get_tree().root.get_child(0)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


func _on_mouse_entered():
	if( get_parent() != Main.g_Layers.get_top_visible_layer() ):
		return
	
	if( Main.g_Layers.painting && Main.g_SelectedTexture ):
		texture = Main.g_SelectedTexture
		m_Material = Main.g_SelectedTextureName
	elif( Main.g_Layers.clearing ):
		texture = null
