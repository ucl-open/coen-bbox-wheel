"""The task file, its pydantic model, the committed JSON schema and the generated C# agree."""

import json
import re
from pathlib import Path

import jsonschema
import pydantic
import pytest
import yaml
from pydantic import ValidationError

from ucl_open_coen_behaviour_box.task import UclOpenCoenBehaviourBoxTaskLogic

ROOT = Path(__file__).parent.parent
TASK = ROOT / "config" / "task-box.yml"
SCHEMA = ROOT / "src" / "DataSchemas" / "ucl_open_coen_behaviour_box_task.json"
GENERATED = ROOT / "src" / "Extensions" / "UclOpenCoenBehaviourBoxTask.Generated.cs"


def task() -> dict:
    return yaml.safe_load(TASK.read_text(encoding="utf-8"))


def _closed(node):
    # rig-control checks a task file against the schema with every object closed.
    if isinstance(node, dict):
        out = {k: _closed(v) for k, v in node.items()}
        if "properties" in out:
            out["additionalProperties"] = False
        return out
    return [_closed(v) for v in node] if isinstance(node, list) else node


def test_the_task_file_validates_and_keeps_the_boxes_30_minutes():
    model = UclOpenCoenBehaviourBoxTaskLogic.model_validate(task())
    assert model.task_parameters.run_length_minutes == 30
    assert task() == {"taskParameters": {"runLengthMinutes": 30}}


@pytest.mark.parametrize("minutes", [0, -1, 10000, 1.5, "30 min", None])
def test_a_run_length_that_is_not_a_whole_number_from_1_to_9999_is_refused(minutes):
    with pytest.raises(ValidationError):
        UclOpenCoenBehaviourBoxTaskLogic.model_validate({"taskParameters": {"runLengthMinutes": minutes}})
    errors = list(jsonschema.Draft202012Validator(json.loads(SCHEMA.read_text(encoding="utf-8"))).iter_errors({"taskParameters": {"runLengthMinutes": minutes}}))
    assert errors


@pytest.mark.parametrize("key", ["runLengthMins", "rngSeed", "RunLengthMinutes"])
def test_the_schema_refuses_a_key_the_task_does_not_have(key):
    errors = list(jsonschema.Draft202012Validator(_closed(json.loads(SCHEMA.read_text(encoding="utf-8")))).iter_errors({"taskParameters": {key: 30}}))
    assert errors


def test_the_committed_task_schema_is_the_model_s():
    model = pydantic.RootModel[UclOpenCoenBehaviourBoxTaskLogic].model_json_schema(
        by_alias=True, mode="serialization", union_format="primitive_type_array"
    )
    assert json.loads(SCHEMA.read_text(encoding="utf-8")) == json.loads(json.dumps(model))


def _property_names(node) -> set[str]:
    if isinstance(node, dict):
        return set(node.get("properties", {})) | {n for v in node.values() for n in _property_names(v)}
    return {n for v in node for n in _property_names(v)} if isinstance(node, list) else set()


def test_the_generated_csharp_has_every_schema_field():
    # A field added to the model and schema but not regenerated into C# stops the workflow at Go: run regenerate-schemas.
    names = set(re.findall(r'JsonPropertyAttribute\("([^"]+)"', GENERATED.read_text(encoding="utf-8")))
    assert names == _property_names(json.loads(SCHEMA.read_text(encoding="utf-8")))
    assert "runLengthMinutes" in names
