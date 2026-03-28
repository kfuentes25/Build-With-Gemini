extends Node3D

@onready var start_menu = get_tree().current_scene.find_child("Menu", true, false)
@onready var start_button = get_tree().current_scene.find_child("Start Button", true, false)
@onready var next_button = get_tree().current_scene.find_child("Button", true, false)
@onready var theme_input = get_tree().current_scene.find_child("LineEdit", true, false)
@onready var player = get_tree().current_scene.find_child("Player", true, false)
@onready var music_player = get_tree().current_scene.find_child("LevelMusicPlayer", true, false)

var spacing = 8.0 
var json_path = "res://layout.json"
var prompt_path = "res://next_prompt.txt"
var check_timer = 0.0
var is_generating = false

func _ready():
	set_process(false)
	
	# Force UI visibility
	if start_menu: start_menu.show()
	if theme_input: theme_input.show()
	if next_button: next_button.show()
	
	# Force Sky Blue Background
	var world_env = get_tree().current_scene.find_child("WorldEnvironment", true, false)
	if world_env:
		world_env.environment.background_mode = Environment.BG_COLOR
		world_env.environment.background_color = Color("#87ceeb")
	
	if player and start_menu:
		player.set_physics_process(false)
		Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
		build_world()
		play_music()

	if start_button: start_button.pressed.connect(_on_start_pressed)
	if next_button: next_button.pressed.connect(_on_next_pressed)

func play_music():
	if music_player and FileAccess.file_exists("res://level_music.mp3"):
		var file = FileAccess.open("res://level_music.mp3", FileAccess.READ)
		var stream = AudioStreamMP3.new()
		stream.data = file.get_buffer(file.get_length())
		music_player.stream = stream
		music_player.play()

func _on_start_pressed():
	if start_menu: start_menu.hide()
	if player: player.set_physics_process(true)
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)

func _on_next_pressed():
	if not theme_input or theme_input.text == "": return
	var f = FileAccess.open(prompt_path, FileAccess.WRITE)
	f.store_string(theme_input.text)
	f.close()
	if next_button: next_button.text = "Painting..."
	is_generating = true
	set_process(true)

func _process(delta):
	check_timer += delta
	if check_timer >= 1.0:
		check_timer = 0.0
		if not FileAccess.file_exists(prompt_path):
			get_tree().reload_current_scene()

func build_world():
	if not FileAccess.file_exists(json_path): return
	var file = FileAccess.open(json_path, FileAccess.READ)
	var data = JSON.parse_string(file.get_as_text())
	var grid = data.grid
	var offset_x = (grid[0].size() * spacing) / 2.0
	var offset_z = (grid.size() * spacing) / 2.0
	var max_h = 0.0

	for z in range(grid.size()):
		for x in range(grid[0].size()):
			var cell = grid[z][x]
			var height = cell[0] * 4.5
			if height > max_h: max_h = height
			spawn_tile(cell[0], cell[1], Vector3(x*spacing-offset_x, 0, z*spacing-offset_z))
	
	if player:
		player.global_position = Vector3(0, max_h + 15.0, 0)

func spawn_tile(h, col, pos):
	var height = h * 4.5
	var pillar = MeshInstance3D.new()
	pillar.mesh = BoxMesh.new()
	pillar.mesh.size = Vector3(spacing * 0.98, height, spacing * 0.98)
	var mat = StandardMaterial3D.new()
	mat.albedo_color = Color(col)
	pillar.material_override = mat
	pillar.position = Vector3(pos.x, height / 2.0, pos.z)
	add_child(pillar)
	pillar.create_trimesh_collision()
