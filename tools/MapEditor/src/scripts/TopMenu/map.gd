extends PopupMenu

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
	Main.change_map_size(Vector2(width, height))
