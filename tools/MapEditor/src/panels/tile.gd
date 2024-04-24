extends TextureRect

class_name Tile

var Main = null

# Called when the node enters the scene tree for the first time.
func _ready():
	Main = get_tree().root.get_child(0)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


func _on_mouse_entered():
	print(name)
		
	if( get_parent().painting && Main.g_SelectedTexture ):
		texture = Main.g_SelectedTexture
	elif( get_parent().clearing ):
		texture = null
