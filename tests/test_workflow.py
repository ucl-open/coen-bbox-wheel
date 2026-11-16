"""src\\main.bonsai held to the lab's rules (open_rigs.rigs.workflow_lint, one copy in lib-open-rigs)."""

import re
import xml.etree.ElementTree as ET
from pathlib import Path

from open_rigs.rigs import workflow_lint as lint

ROOT = Path(__file__).parents[1]
WORKFLOW = lint.Workflow(ROOT)
TEXT = (ROOT / "src" / "main.bonsai").read_text(encoding="utf-8-sig")
MAIN = ET.fromstring(TEXT.encode("utf-8"))


def test_the_hardware_is_the_lab_s_pieces():
    # ReadLabRig first, ReadyGate before the pieces, one clock (the board's), the camera on its trigger, Ready waiting for
    # the clock and the camera's first frame.
    assert lint.hardware_problems(WORKFLOW) == []
    assert [name for name, _ in lint.required_devices(WORKFLOW)] == ["BehaviorBoard-Main", "Camera-Overhead"]
    # The behaviour boxes' rig list (16 Nov 2026), which the box's preflight runs too: no piece of its own.
    assert TEXT.count(f'Path="{lint.DEVICES}BehaviorBoxHardware.bonsai"') == 1
    assert {path for path, _ in lint.hardware(WORKFLOW)} - {lint.READ_LAB_RIG, lint.CAMERA_LIVE_CONTROLS} <= set(_rig_list())


def _rig_list() -> list[str]:
    nodes, _ = lint.nodes_and_edges(lint.child(lint.package_include(WORKFLOW, lint.DEVICES + "BehaviorBoxHardware.bonsai"), lint.W + "Workflow"))
    return [n.get("Path") for n in nodes if n.get("Path")]


def test_the_experiment_logs_are_the_lab_s():
    assert lint.experiment_log_problems(WORKFLOW) == []


def test_every_file_the_workflow_writes_is_in_the_manifest_s_expected_files():
    assert lint.expected_files_problems(WORKFLOW) == []


def test_no_trial_graph_closes_a_shared_subject():
    assert lint.subjects_closed_by_a_nested_multicast(WORKFLOW) == []


def test_the_workflow_declares_every_command_it_handles():
    assert lint.undeclared_commands(WORKFLOW) == [] and lint.declared_twice(WORKFLOW) == []


def test_no_spout_step_size_and_no_background_noise():
    # No lick spout stage and no speakers: nothing declares SpoutStepSize or includes BackgroundNoise (16 Nov 2026).
    assert lint.spout_step_size_problems(WORKFLOW) == [] and lint.background_noise_problems(WORKFLOW) == []


def test_the_records_are_experiment_records_and_write_what_the_logging_group_wrote():
    # Pip, 16 Nov 2026: the box as the domes. The hand-built Logging group (LogControlEvents, RecordHarpDevices,
    # ExperimentManifest) is lib's ExperimentRecords, and nothing written changed: the manifest's IngestScript and
    # ExpectedFiles are the group's, no trial columns file (the box has no trial log; the group set none), the same
    # devices, and no reward (the box has no valves). The manifest has no run input now, as the domes': completed comes
    # from TaskLogic's Finished, and run.items is null (the frame count is the camera CSV's rows).
    assert lint.experiment_records_problems(WORKFLOW) == [] and lint.reward_problems(WORKFLOW) == []
    records = next(n for n in lint.ET.fromstring(TEXT.encode("utf-8")).iter(lint.W + "Expression") if n.get("Path") == lint.EXPERIMENT_RECORDS)
    props = {c.tag.split("}")[-1]: (c.text or "") for c in records if c.tag != lint.W + "Description"}
    assert props == {"ConfigRoot": r"C:\Coen-Lab-Local\RigConfigs", "IngestScript": "coen-behaviour-box", "TrialColumns": "",
                     "ExpectedFiles": "auto;harp;Settings/Settings_Rig_;Settings/Settings_Task_;Settings/Settings_Experiment_;BonsaiData/BonsaiData_Async_"}
    assert "<Name>RewardRequests</Name>" not in TEXT and lint.DELIVER_REWARD not in TEXT and lint.TASK_LOGS not in TEXT
    assert TEXT.count("orcl:ReportPhase") == 1 and "<orcl:Phase>Finished</orcl:Phase>" in TEXT


def test_the_layout_is_tracked():
    assert lint.layout_problems(WORKFLOW) == []


def test_the_launch_properties():
    # The launch's IDs, the task file's path, the camera piece's Binning and the lab's ConfigRoot.
    top = lint.child(MAIN, lint.W + "Workflow").find(lint.W + "Nodes")
    exposed = {p.get("Name") for e in top if e.get(lint.XSI) == "ExternalizedMapping" for p in e}
    assert exposed == {"SubjectId", "SessionId", "LaunchId", "TaskPath", "Binning", "ConfigRoot"}


def test_the_launch_id_reaches_the_controller():
    assert lint.launch_id_problems(WORKFLOW) == []


def test_every_device_is_opened_by_the_lab_s_pieces_and_the_live_view_is_last():
    assert lint.hand_opened_devices(WORKFLOW) == [] and lint.live_view_problems(WORKFLOW) == []


def test_every_config_root_is_the_lab_s():
    # check-workflow holds every node that reads rig.yml to one root (ReadLabRig, ExperimentRecords, LiveView); this holds
    # that root to the lab's.
    assert set(re.findall(r"<(?:\w+:)?ConfigRoot>([^<]*)</", TEXT)) == {r"C:\Coen-Lab-Local\RigConfigs"}


def test_the_readme_lists_every_open_rigs_block():
    assert lint.readme_missing_blocks(WORKFLOW) == []


def test_the_run_length_s_frames_are_at_the_camera_s_own_trigger_frequency():
    # A camera on DO1 runs at trigger1Frequency: the frequency is the one OpenRigs.Devices CameraTrigger finds for
    # Camera-Overhead from the board's wiring, as the camera piece does, never the board's trigger0Frequency.
    group = next(e for e in MAIN.iter(lint.W + "Expression") if e.findtext(lint.W + "Name") == "RunLengthToFrames")
    nodes, edges = lint.nodes_and_edges(group.find(lint.W + "Workflow"))
    (trigger,) = [i for i, n in enumerate(nodes) if lint.kind(n) == "dev:CameraTrigger"]
    (zip_,) = [a for a, b, _ in edges if b == trigger]
    fed = {label: nodes[a].findtext(lint.W + "Name") for a, b, label in edges if b == zip_}
    assert fed == {"Source1": "Camera-Overhead", "Source2": "BehaviorBoard-Main"}
    assert "* 60.0 * Item2.Frequency)" in ET.tostring(group, encoding="unicode")

def _xml(element) -> str:
    return re.sub(r"ns\d+:", "", ET.tostring(element, encoding="unicode"))


def test_the_launch_settings_are_lib_s_with_the_box_s_task_file():
    # Pip, 16 Nov 2026: the run length is the task file's, read through lib's LaunchSettings (TaskPath), as the domes'.
    assert lint.launch_settings_problems(WORKFLOW) == []
    node = next(n for n in MAIN.iter(lint.W + "Expression") if n.get("Path") == lint.LAUNCH_SETTINGS)
    assert node.findtext(lint.W + "TaskPath") == "..\\config\\task-box.yml"


def test_the_run_length_is_the_task_file_s_and_no_controller_parameter():
    assert "RunLengthMinutes" not in re.sub(r"<Description>.*?</Description>", "", TEXT, flags=re.S).replace("TaskParameters.RunLengthMinutes", "")
    assert "orcl:ParameterValue" not in TEXT and not re.search(r"<Parameter>\s*<Name>RunLength", TEXT)
    assert "<Name>RunSettings</Name>" not in TEXT  # LaunchSettings publishes it
    group = next(e for e in MAIN.iter(lint.W + "Expression") if e.findtext(lint.W + "Name") == "RunLengthToFrames")
    text = _xml(group)
    assert "<Name>TaskConfig</Name>" in text and "Item1.TaskParameters.RunLengthMinutes * 60.0" in text


def test_the_task_file_is_read_at_go_into_task_config():
    # ExperimentGo zipped with TaskFilePath (the path is known from Start, the read waits for Go), deserialized as the generated model.
    group = next(e for e in MAIN.iter(lint.W + "Expression") if e.findtext(lint.W + "Name") == "TaskFile")
    text = _xml(group)
    for part in ("<Name>ExperimentGo</Name>", "<Name>TaskFilePath</Name>", "core:ReadTextFile", "UclOpenCoenBehaviourBoxTaskLogic", "<Name>TaskConfig</Name>"):
        assert part in text
    assert TEXT.count("<Name>TaskConfig</Name>") == 3  # published once, read by the run length and by Settings_Task


def test_settings_task_is_the_task_file_as_json_after_the_experiment_folder_exists():
    logs = [e for e in MAIN.iter(lint.W + "Expression") if e.get("Path") == "OpenRigs.Logging:LogDataSchema.bonsai" and e.findtext(lint.W + "Name") == "Settings_Task"]
    assert len(logs) == 1
    assert "task:SerializeToJson" in TEXT and "Settings/Settings_Task_" in TEXT
    assert lint.output_ends_logs_problems(WORKFLOW.root) == []
