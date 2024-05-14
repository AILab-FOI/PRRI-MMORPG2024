extends Button

var entity_type = "" :
	set(value):
		entity_type = value
		
		var startIndex = max( 0, value.rfind(".") + 1 )
		%EntityType.text = value.substr(startIndex)

var entity_name = ""
var attr = {}

var Main = null

# Called when the node enters the scene tree for the first time.
func _ready():
	Main = get_tree().root.get_child(0)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

func set_entity_type(name: String):
	entity_type = name

func set_attr(attrName: String, newVal):
	attr[attrName] = newVal
	
	match( attrName ):
		"pos":
			var displayPos = newVal * Main.g_TileSize
			displayPos -= Vector2(Main.g_TileSize,Main.g_TileSize) / 2
			set_position( displayPos )
		"name":
			%Name.text = newVal
