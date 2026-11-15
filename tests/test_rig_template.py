import importlib.util
import subprocess
from pathlib import Path

import pytest
from open_rigs.core import yaml

import ucl_open_coen_behaviour_box.regenerate as regenerate
from ucl_open_coen_behaviour_box.rig import BehaviourBoxRig

REPO = Path(__file__).parent.parent
TEMPLATE = REPO / "config" / "rig-template.yml"


def _examples_rig():
    spec = importlib.util.spec_from_file_location("examples_rig", REPO / "examples" / "rig.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_template_is_what_examples_rig_writes(tmp_path):
    # e118138: lib-open-rigs added trigger0Enabled and trigger1Enabled, examples/rig.py was not rerun,
    # and the committed template lagged the model until the Schemas CI was noticed failing.
    written = tmp_path / "rig-template.yml"
    _examples_rig().main(written)
    assert written.read_text(encoding="utf-8") == TEMPLATE.read_text(encoding="utf-8")


def test_template_loads_with_the_devices_the_workflow_asks_for():
    rig = yaml.load(BehaviourBoxRig, TEMPLATE)
    assert set(rig.behavior_board) == {"main"}
    assert set(rig.camera) == {"overhead"}


def test_regenerate_fails_when_sgen_fails(tmp_path, monkeypatch):
    # 054f823 let regenerate-schemas carry on after a failed bonsai.sgen, so a new schema could be
    # committed beside a stale Generated.cs; c5d6607 made it exit with sgen's code.
    monkeypatch.setattr(regenerate, "SCHEMA_ROOT", tmp_path)
    monkeypatch.setattr(regenerate, "SCHEMA_FILE", tmp_path / "schema.json")
    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: subprocess.CompletedProcess(args, 3))
    with pytest.raises(SystemExit) as stopped:
        regenerate.main()
    assert stopped.value.code == 3
