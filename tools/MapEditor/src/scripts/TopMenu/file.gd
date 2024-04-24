extends PopupMenu

signal assets_loaded

var Main = null

# Called when the node enters the scene tree for the first time.
func _ready():
	Main = get_tree().root.get_child(0)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

func _on_open_pressed():
	$FileDialog.popup()

func _on_id_pressed(id):
	match id:
		0:
			_on_open_pressed()

func _scan_folder_for_materials(dir: DirAccess):
	var files = dir.get_files()
	var dirs = dir.get_directories()
	for file in files:
		var fullPath = dir.get_current_dir()+"/"+file
		var relativePath = fullPath.replace(Main.g_AssetPath, "")
		
		if( not file.ends_with(".material") ):
			continue
		
		var rawFile = FileAccess.open(fullPath, FileAccess.READ)
		if not rawFile:
			print("Dang")
			continue
		
		print(rawFile.get_as_text())
		
		var json = JSON.parse_string(rawFile.get_as_text())
		if( not json ):
			continue
		
		print(json["type"])
		
		if( json["type"] != "sprite" ):
			continue
		
		var imagePath = Main.g_AssetPath + "/" + json["path"]
		
		var rawImage = Image.load_from_file(imagePath)
		if rawImage:
			var imageTexture = ImageTexture.create_from_image(rawImage)
			Main.g_Materials[relativePath] = imageTexture
	
	for subpath in dirs:
		var subdir := DirAccess.open(dir.get_current_dir()+"/"+subpath)
		if subdir:
			_scan_folder_for_materials(subdir)

func _on_file_dialog_dir_selected(path):
	Main.g_AssetPath = path
	var test: Texture2D = null

	Main.g_Materials.clear()
	Main.g_SelectedTexture = null
	
	var dir := DirAccess.open(Main.g_AssetPath+"/"+"materials")
	if dir:
		_scan_folder_for_materials(dir)
	
	assets_loaded.emit()
