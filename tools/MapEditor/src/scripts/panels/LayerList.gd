extends ItemList

var Main = null

# Called when the node enters the scene tree for the first time.
func _ready():
	Main = get_tree().root.get_child(0)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


func _on_item_selected(index):
	var layerName: String = get_item_text(index)
	%Layers.hide_untill_layer(layerName)

func _on_new_pressed():
	$NewLayerMenu.popup()

func move_layer( direction: int ):
	if( !is_anything_selected() ):
		return
	
	var index = get_selected_items()[0]
	var layerName: String = get_item_text(index)
	%Layers.move_layer(layerName, direction)

func _on_up_pressed():
	move_layer( 1 )


func _on_down_pressed():
	move_layer( -1 )
