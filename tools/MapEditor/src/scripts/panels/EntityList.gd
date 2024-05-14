extends HFlowContainer

var selected_item: Button = null :
	get:
		return selected_item
	set(new):
		if( selected_item ):
			selected_item.button_pressed = false
		selected_item = new

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

func on_entity_pressed(entityDisplay):
	selected_item = entityDisplay

func add_item( entityDisplay ):
	entityDisplay.pressed.connect(on_entity_pressed.bind(entityDisplay))
	add_child(entityDisplay)
