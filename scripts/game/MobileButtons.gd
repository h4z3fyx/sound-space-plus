extends Control

func _on_Pause_pressed():
	Input.action_press("pause")
	
func _on_Pause_released():
	Input.action_release("pause")
	
func _on_GiveUp_pressed():
	Input.action_press("give_up")
	
func _on_GiveUp_released():
	Input.action_release("give_up")

func _ready():
	var tween:Tween = Tween.new()
	add_child(tween)
	
	$Pause/Button.visible = OS.has_feature("mobile")
	$GiveUp/Button.visible = OS.has_feature("mobile")
	
	get_viewport().connect("size_changed", self, "position_buttons")
	position_buttons()
	
	tween.interpolate_property($Pause, "modulate", Color(1,1,1,0.5), Color(1,1,1,0), 1, Tween.TRANS_QUAD, Tween.EASE_IN_OUT, 1)
	tween.start()
	tween.interpolate_property($GiveUp, "modulate", Color(1,1,1,0.5), Color(1,1,1,0), 1, Tween.TRANS_QUAD, Tween.EASE_IN_OUT, 1)
	tween.start()

func position_buttons():
	if not OS.has_feature("mobile"):
		return
	# Safe area is in screen pixels; buttons use the stretched viewport coordinates.
	var inverse = get_viewport_transform().affine_inverse()
	var safe = OS.get_window_safe_area()
	var top_left = inverse.xform(safe.position)
	var bottom_right = inverse.xform(safe.end)
	var button_x = top_left.x
	if Rhythia.mirror_buttons:
		button_x = bottom_right.x - 150
	$Pause/Button.position = Vector2(button_x, top_left.y)
	$GiveUp/Button.position = Vector2(button_x, bottom_right.y - 226)
