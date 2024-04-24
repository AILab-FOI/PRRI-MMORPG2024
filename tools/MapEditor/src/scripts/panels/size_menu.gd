extends PopupPanel

class_name SizeMenu

signal map_size_changed


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


func _on_ok_pressed():
	self.hide()
	
	var widthInput: SpinBox = %WidthInput
	var heightInput: SpinBox = %HeightInput
	map_size_changed.emit( widthInput.value, heightInput.value )


func _on_cancel_pressed():
	self.hide()
