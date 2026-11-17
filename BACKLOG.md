# Backlog

What is still to do, then what has been decided and why. Closed work, audit rounds and lib-open-rigs' own changes are in `git log` (and lib-open-rigs').

## Open

- Check on the rig (BBOX-1):
  - Quick Sync and `LogVideoFfmpeg` (`h264_qsv`): checked offline only. Run 30 minutes: 90,000 frames == 90,000 CSV rows, CPU, no dropped-frame warning.
  - Manifest outcomes seen: `completed`, `stopped`, `ended-early`. Still to see: `error` (a pulled trigger cable) and the overnight copy of a real experiment.
  - Wheel distance: 10 turns during a recording change the `Encoder` value by 10 x `countsPerRev`, unwrapped.
  - The board clock after a power-cycle.
  - Lost board messages shift every later `harpTime` (seen once): frames pair with trigger events in order.
  - A controller `stop` leaves a modal Runtime Error in the editor (headless exits): decide whether `stop` should end the run some quieter way.
  - Whether the heartbeat advertises the live view in ready mode, before Go.
- Raise upstream (open-rigs/open-rigs), each with `*Comment/research by Claude, read/edited by Pip.*` and a short fix diff: CameraTriggerController counts the register-dump reply as a trigger (comment on #4); RunningWheel takes a Difference in Displacement mode; the template's generated files look changed under `core.autocrlf`; the template's `deploy.ps1` ignores failures; its `pyproject.toml` declares a console script with no module; its `Extensions.csproj` compiles C# Bonsai cannot (no `LangVersion` 5). Posted: #5, #6, #7, #8.
- Later: released OpenRigs packages once open-rigs ships the camera fixes and config operators (lib-open-rigs `patches/README.md`); `copier update` from `gh:open-rigs/open-rigs` once roadmap#38 lands.

## Decided

- The hardware is lib's rig list `BBoxHardware`; no device opened by hand.
- The records are lib's `ExperimentRecords`, as the dome tasks', with the same files, columns and `ExpectedFiles` as the hand-built `Logging` group (writers compared with lib's includes expanded, and a test). The manifest has no run input, as the domes': `completed` comes from `TaskLogic`'s Finished and `run.items` is null.
- The run length is a task file, `config\task-bbox.yml`, as the domes keep their task settings: `taskParameters.runLengthMinutes`, read through lib's `LaunchSettings` (`TaskPath`) at Go and logged as `Settings_Task`. It is no longer a controller parameter or a `Settings_Experiment` entry; the workflow has no `ExperimentIds` of its own.
- The run is the `TaskLogic` group, as the dome tasks name theirs.
- Licensed BSD 3-Clause, as lib-open-rigs.
- The camera records Mono8 through `LogVideoFfmpeg`.
- The rig's local `rig.yml` is the master; app-rig-setup copies it one way up to the share.

## Not doing

- Box run length not moved back to a controller parameter: the task file is the one place.
- Box task-file layout not made to mirror the domes: lib `TaskLogs` needs `TrialRow` and the box has no trials; `ReadTextFile` and `ReadAllText` differ on purpose.
