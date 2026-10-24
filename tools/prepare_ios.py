#!/usr/bin/env python3
"""Create an isolated Godot 3 iOS source tree without desktop native addons."""
import argparse
import re
import shutil
from pathlib import Path


def prepare(source: Path, destination: Path) -> None:
    source, destination = source.resolve(), destination.resolve()
    if destination == source or source in destination.parents or destination in source.parents:
        raise ValueError("Destination must be outside the source tree")
    if destination.exists():
        raise ValueError("Destination must not already exist")
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns(
        ".git", ".github", ".import", ".godot", "build", "android", "addons", "__pycache__"))

    project_path = destination / "project.godot"
    project = project_path.read_text()
    # NativeScript classes and addon example classes cannot be parsed without their SDKs.
    classes = re.search(r'_global_script_classes=\[ (.*?) \]', project, re.S)
    if not classes:
        raise ValueError("Missing Godot 3 script class registry")
    entries = re.findall(r'\{.*?\}', classes[1], re.S)
    entries = [entry for entry in entries if '"res://addons/' not in entry]
    project = project[:classes.start(1)] + ", ".join(entries) + project[classes.end(1):]
    class_names = {re.search(r'"class": "(.*?)"', entry)[1] for entry in entries}
    project = re.sub(r'^"([^"\n]+)": ""[,]?\n',
                     lambda match: match[0] if match[1] in class_names else "", project, flags=re.M)
    project = re.sub(r'^Discord=".*"$', 'Discord="*res://scripts/platform/DiscordDisabled.gd"', project, flags=re.M)
    project = re.sub(r'^enabled=PoolStringArray\(.*\)$', 'enabled=PoolStringArray(  )', project, flags=re.M)
    project = re.sub(r'^singletons=\[.*\]$', 'singletons=[  ]', project, flags=re.M)
    # Also disable RPC during the Linux import/export, where .mobile overrides do not apply.
    project = project.replace('config/discord_rpc=true', 'config/discord_rpc=false')
    project = project.replace('config/disable_native_file_dialogs=false', 'config/disable_native_file_dialogs=true')
    project = project.replace('quality/driver/fallback_to_gles2=true', 'quality/driver/fallback_to_gles2=false')
    project_path.write_text(project)

    # These placeholder nodes trigger the existing FileSelector2D fallback to Godot dialogs.
    for scene in destination.rglob("*.tscn"):
        text = scene.read_text()
        text = re.sub(r'res://addons/native_dialogs/bin/[^"\n]+\.gdns',
                      'res://scripts/platform/NativeDialogDisabled.gd', text)
        scene.write_text(text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    try:
        prepare(Path(__file__).resolve().parents[1], args.destination)
    except ValueError as error:
        parser.error(str(error))
