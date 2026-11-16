"""src\\main.bonsai held to the lab's rules (open_rigs.rigs.workflow_lint, one copy in lib-open-rigs)."""

from pathlib import Path

from open_rigs.rigs import workflow_lint as lint

ROOT = Path(__file__).parents[1]
WORKFLOW = lint.Workflow(ROOT)
TEXT = (ROOT / "src" / "main.bonsai").read_text(encoding="utf-8-sig")


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
    assert "SpoutStepSize" not in TEXT and lint.BACKGROUND_NOISE not in TEXT


def test_the_records_are_experiment_records_and_write_what_the_logging_group_wrote():
    # Pip, 16 Nov 2026: the box as the domes. The hand-built Logging group (LogControlEvents, RecordHarpDevices,
    # ExperimentManifest) is lib's ExperimentRecords, and nothing written changed: the manifest's IngestScript and
    # ExpectedFiles are the group's, no trial columns file (the box has no trial log; the group set none), the same
    # devices, and no reward (the box has no valves). The manifest has no run input now, as the domes': completed comes
    # from Run's Finished, and run.items is null (the frame count is the camera CSV's rows).
    assert lint.experiment_records_problems(WORKFLOW) == [] and lint.reward_delivery_problems(WORKFLOW) == []
    records = next(n for n in lint.ET.fromstring(TEXT.encode("utf-8")).iter(lint.W + "Expression") if n.get("Path") == lint.EXPERIMENT_RECORDS)
    props = {c.tag.split("}")[-1]: (c.text or "") for c in records}
    assert props == {"ConfigRoot": "C:\Coen-Lab-Local\RigConfigs", "IngestScript": "coen-behaviour-box", "TrialColumns": "",
                     "ExpectedFiles": "auto;harp;Settings/Settings_Rig_;Settings/Settings_Experiment_;BonsaiData/BonsaiData_Async_"}
    assert "<Name>RewardRequests</Name>" not in TEXT and lint.DELIVER_REWARD not in TEXT and lint.TASK_LOGS not in TEXT
    assert TEXT.count("orcl:ReportPhase") == 1 and "<orcl:Phase>Finished</orcl:Phase>" in TEXT


def test_launch_settings_wait_for_a_task_file():
    # LaunchSettings needs the task file's TaskPath, and the box's one task setting, RunLengthMinutes, is a controller
    # parameter that Settings_Experiment records: a task file would move it (a new Settings_Task file), so the box keeps
    # its own RunSettings, with the run length, until Pip decides (16 Nov 2026).
    assert lint.LAUNCH_SETTINGS not in TEXT and "<Name>RunSettings</Name>" in TEXT


def test_the_layout_is_tracked():
    assert lint.layout_problems(WORKFLOW) == []


def test_the_box_keeps_no_rig_model_of_its_own():
    # The lab's LabRig (ReadLabRig) reads rig.yml, and lib's one template starts a new rig's (15 Nov 2026).
    assert not (ROOT / "src" / "DataSchemas").exists() and not (ROOT / "config" / "rig-template.yml").exists()
    assert "ext:" not in TEXT


def test_the_camera_s_parameters_are_the_piece_s_own():
    # CameraLiveControls declares CameraExposureUs and CameraGainDb (lib-open-rigs, 16 Nov 2026): the task names neither.
    assert "<Name>CameraExposureUs</Name>" not in TEXT and "<Name>CameraGainDb</Name>" not in TEXT and "ExposureParameter" not in TEXT
