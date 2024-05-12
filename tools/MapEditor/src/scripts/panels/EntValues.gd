extends PopupPanel

var args = {}

var Main = null

var varControls = {}

var edit_entity = null

# Called when the node enters the scene tree for the first time.
func _ready():
	Main = get_tree().root.get_child(0)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

func _on_about_to_popup():
	size.y = 0

func _on_popup_hide():
	edit_entity = null
	args.clear()
	varControls.clear()

func load_entity(entity):
	edit_entity = entity
	
	var args = Main.g_Entities[entity.entity_type]
	
	Main.g_EntValues.load_type(entity.entity_type, args)
	
	for attrName in entity.attr.keys():
		if( !varControls.has(attrName) ):
			continue
		var attrVal = entity.attr[attrName]
		var attrType = Main.GetTypeStringBasedOnVar(attrVal)
		
		var setControlFunc = Main.g_ControlSet[attrType]
		setControlFunc.call(varControls[attrName], entity.attr[attrName])

func load_type( entType: String, newArgs: Dictionary ):
	args.clear()
	varControls.clear()
	
	for child in %VariableContainer.get_children():
		%VariableContainer.remove_child(child)
		child.queue_free()
	
	%Name.text = entType
	
	for argName in newArgs.keys():
		var argType = newArgs[argName]
		
		if( !Main.g_TypeMapping.has(argType) ):
			continue
		
		args[argName] = Main.g_TypeMapping[argType]
		var input = Main.g_ControlMapping[argType].call(argType)
		
		varControls[argName] = input
		
		var label = Label.new()
		label.text = argName
		
		var control = HBoxContainer.new()
		control.add_child(label)
		control.add_child(input)
		
		%VariableContainer.add_child(control)

func _on_ok_pressed():	
	for attrName in args.keys():
		if( !varControls.has(attrName) ):
			continue
		
		var attrVal = args[attrName]
		var attrType = Main.GetTypeStringBasedOnVar(attrVal)
		
		var getControlFunc = Main.g_ControlGet[attrType]
		var newVal = getControlFunc.call( varControls[attrName] )
		
		edit_entity.set_attr( attrName, newVal )
	
	self.hide()

func _on_cancel_pressed():
	self.hide()
