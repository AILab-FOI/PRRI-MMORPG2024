extends Button

var entity_name = "" :
	set(value):
		var startIndex = max( 0, value.rfind(".") + 1 )
		entity_name = value.substr(startIndex)
		
		# If there's a module, set it as well
		if( startIndex != 0 ):
			module_name = value.substr(0, startIndex-1)
			$VBoxContainer/ModuleName.text = module_name
		else:
			$VBoxContainer/ModuleName.visible = false
		
		$VBoxContainer/EntityName.text = entity_name
var module_name = ""

var full_name: String :
	get:
		var ret = ""
		if( module_name.length() > 0 ):
			ret += module_name + "."
		ret += entity_name
		return ret
	set(val):
		pass

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

func set_entity(name: String):
	entity_name = name
