extends PopupPanel

signal new_layer_added

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

func _on_ok_pressed():
	self.hide()
	
	var nameInput: TextEdit = %NameInput
	var typeInput: OptionButton = %TypeInput

	new_layer_added.emit( nameInput.text, typeInput.get_item_text(typeInput.selected) )

func _on_cancel_pressed():
	self.hide()
