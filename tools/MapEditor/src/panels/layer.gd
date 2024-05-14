extends Control

var Entity = preload("res://panels/entity_in_world.tscn")

var type = ""
var order = 0

var Main = null

# Called when the node enters the scene tree for the first time.
func _ready():
	Main = get_tree().root.get_child(0)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

func open_ent_edit(entity):
	Main.g_EntValues.load_entity(entity)
	Main.g_EntValues.popup()

func create_entity( type: String, pos: Vector2 ):
	var newEnt = Entity.instantiate()
	add_child(newEnt)
	
	newEnt.set_entity_type( type )
	
	newEnt.set_attr( "pos", pos )
	newEnt.pressed.connect( open_ent_edit.bind(newEnt) )
	
	return newEnt

func create_entity_at_cursor():
	return create_entity(Main.g_SelectedEntity.full_name, Main.g_MousePos - Vector2(0.5,0.5))

func _on_gui_input(event:InputEvent):
	if( type != "entities" ):
		return
	
	if event is InputEventMouseButton:
		match event.button_index:
			1:
				if( event.pressed ):
					create_entity_at_cursor()
