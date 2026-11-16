# Backlog

History, the audit cycles and every closed item, is in `git log`.

## Open

- A task file and the shared includes (`LaunchSettings`, `ExperimentRecords`) as the dome tasks have, in place of the hand-built `RunSettings` and `Logging` group, recording the same files and columns (Pip, 16 Nov 2026).
- Check on the rig (GEEK-BBOX1):
  - Quick Sync and `LogVideoFfmpeg` (`h264_qsv`): checked offline only. Run 30 minutes: 90,000 frames == 90,000 CSV rows, CPU, no dropped-frame warning.
  - Manifest outcomes seen: `completed`, `stopped`, `ended-early`. Still to see: `error` (a pulled trigger cable) and the overnight copy of a real experiment.
  - Wheel distance: 10 turns during a recording change the `Encoder` value by 10 x `countsPerRev`, unwrapped.
  - The board clock after a power-cycle.
  - Lost board messages shift every later `harpTime` (seen once, 30 Oct 2026): frames pair with trigger events in order.
  - A controller `stop` leaves a modal Runtime Error in the editor (headless exits): decide whether `stop` should end the run some quieter way.
  - Whether the heartbeat advertises the live view in ready mode, before Go.
- Raise upstream (open-rigs/open-rigs), each with `*Comment/research by Claude, read/edited by Pip.*` and a short fix diff: CameraTriggerController counts the register-dump reply as a trigger (comment on #4); RunningWheel takes a Difference in Displacement mode; the template's generated files look changed under `core.autocrlf`; the template's `deploy.ps1` ignores failures; its `pyproject.toml` declares a console script with no module; its `Extensions.csproj` compiles C# Bonsai cannot (no `LangVersion` 5). Posted: #5, #6, #7, #8.
- Later: released OpenRigs packages once open-rigs ships the camera fixes and config operators (lib-open-rigs `patches/README.md`); `copier update` from `gh:open-rigs/open-rigs` once roadmap#38 lands.

## Decided

- The hardware is lib's rig list `BBoxHardware` (16 Nov 2026); no device opened by hand.
- Licensed BSD 3-Clause, as lib-open-rigs.
- The camera records Mono8 through `LogVideoFfmpeg`.
- The rig's local `rig.yml` is the master; app-rig-setup copies it one way up to the share.
