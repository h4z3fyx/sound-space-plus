import tempfile
import unittest
from pathlib import Path

from prepare_ios import prepare

REPO = Path(__file__).resolve().parents[1]


class PrepareIOSTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.source = Path(self.temp.name) / "source"
        self.source.mkdir()
        (self.source / "project.godot").write_bytes((REPO / "project.godot").read_bytes())
        (self.source / "filesel.tscn").write_bytes((REPO / "prefabs/menu/filesel.tscn").read_bytes())
        (self.source / "addons").mkdir()
        (self.source / "addons/desktop.so").write_bytes(b"desktop-only")
        (self.source / "map.sspm").write_bytes(b"map-content")
        self.destination = Path(self.temp.name) / "ios"

    def test_isolated_source_and_native_free_project(self):
        original = {path.name: path.read_bytes() for path in self.source.iterdir() if path.is_file()}
        prepare(self.source, self.destination)
        self.assertFalse((self.destination / "addons").exists())
        project = (self.destination / "project.godot").read_text()
        self.assertNotIn("NativeScript", project)
        self.assertNotIn("res://addons/", project)
        self.assertIn('Discord="*res://scripts/platform/DiscordDisabled.gd"', project)
        self.assertIn('"class": "Song"', project)
        self.assertIn("config/discord_rpc=false", project)
        self.assertIn("config/disable_native_file_dialogs=true", project)
        self.assertNotIn(".gdns", (self.destination / "filesel.tscn").read_text())
        self.assertEqual((self.destination / "map.sspm").read_bytes(), b"map-content")
        for name, content in original.items():
            self.assertEqual((self.source / name).read_bytes(), content)

    def test_refuses_overwrite(self):
        self.destination.mkdir()
        sentinel = self.destination / "keep"
        sentinel.write_text("keep")
        with self.assertRaises(ValueError):
            prepare(self.source, self.destination)
        self.assertEqual(sentinel.read_text(), "keep")

    def test_refuses_overlapping_trees(self):
        for destination in [self.source, self.source / "nested", self.source.parent]:
            with self.subTest(destination=destination), self.assertRaises(ValueError):
                prepare(self.source, destination)


if __name__ == "__main__":
    unittest.main()
