# The iOS staging step replaces the desktop Discord autoload with this facade.
# Keep the members referenced by game scripts available to the GDScript parser.
extends Node

enum ActivityType { Playing, Streaming, Listening, Watching }
enum Result { Ok, ServiceUnavailable }

class Assets:
	func set_large_image(_image):
		pass

class Activity:
	func set_type(_type):
		pass
	func set_details(_details):
		pass
	func set_state(_state):
		pass
	func get_assets():
		return Assets.new()

class DisabledResult:
	extends Reference
	signal result
	var result = Result.ServiceUnavailable

class ActivityManager:
	func update_activity(_activity):
		var response = DisabledResult.new()
		response.call_deferred("emit_signal", "result", response)
		return response

var activity_manager = ActivityManager.new()
