extends PopupPanel

signal save_file

var Main = null

# Called when the node enters the scene tree for the first time.
func _ready():
	Main = get_tree().root.get_child(0)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


func _on_ok_pressed():
	self.hide()
	
	var fileNameInput: TextEdit = %FileNameInput
	save_file.emit( fileNameInput.text )

func _on_cancel_pressed():
	self.hide()


func _on_about_to_popup():
	$VBoxContainer/Input/Label.text = Main.g_AssetPath + "/maps/"
