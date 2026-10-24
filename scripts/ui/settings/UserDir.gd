extends Button

func _pressed():
	if !OS.has_feature("mobile"):
		OS.shell_open(ProjectSettings.globalize_path(Globals.p("user://")))

func _ready():
	if OS.has_feature("mobile"):
		disabled = true
		text = "User folder location: " + Globals.p("user://")
