extends Control

var dragging = false
var painting = false
var clearing = false

var Main = null

# Called when the node enters the scene tree for the first time.
func _ready():
	Main = get_tree().root.get_child(0)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


func _on_gui_input(event:InputEvent):
	if event is InputEventMouseButton:
		painting = false
		clearing = false
		dragging = false

		match event.button_index:
			1:
				painting = event.pressed
			2:
				clearing = event.pressed
			3:
				dragging = event.pressed

	elif event is InputEventMouseMotion:
		if( not dragging ):
			return
		
		var position: Vector2 = self.get_position()
		
		position += event.relative
		self.set_position(position)
