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


def test_the_records_and_launch_settings_are_the_box_s_own():
    # Not ExperimentRecords: the box's manifest takes the run (the frames recorded) as its input, for its outcome and
    # run.items, which ExperimentRecords' manifest does not, and the box gives no rewards. Not LaunchSettings: the box has
    # no task file, and its RunSettings carries the run length (16 Nov 2026).
    assert lint.EXPERIMENT_RECORDS not in TEXT and lint.LAUNCH_SETTINGS not in TEXT
    assert "<Name>RunSettings</Name>" in TEXT


def test_the_layout_is_tracked():
    assert lint.layout_problems(WORKFLOW) == []


def test_the_box_keeps_no_rig_model_of_its_own():
    # The lab's LabRig (ReadLabRig) reads rig.yml, and lib's one template starts a new rig's (15 Nov 2026).
    assert not (ROOT / "src" / "DataSchemas").exists() and not (ROOT / "config" / "rig-template.yml").exists()
    assert "ext:" not in TEXT
