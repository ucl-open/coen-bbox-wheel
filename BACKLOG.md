# Backlog

## 15 Nov 2026: Pip's decisions after the audit cycles

- `deploy.ps1` runs bonsai.sgen once, in `regenerate-schemas` (same `Generated.cs` byte for byte), and drops `git submodule update` (no submodules) and the `calibration\` folder (the box has none). The unused task model (`task.py`, `examples\task.py`), open_rigs' `ExperimentSession` and `pydantic-settings` are gone: the schema and generated C# hold `BehaviourBoxRig` only. `swc-aeon` is pinned to the commit `uv.lock` held (Pip: pinned in all repos), not a branch.
- Licensed BSD 3-Clause, as lib-open-rigs (Pip): `LICENSE` is lib-open-rigs' with the holder "Coen Lab, University College London", and `pyproject.toml` says `BSD-3-Clause`, not MIT.

## Audit cycle 5 (15 Nov 2026)

- First pytest tests (`tests\test_rig_template.py`, pytest in the `dev` group): the template is what `examples\rig.py` writes (e118138's stale template fails it), it loads as `BehaviourBoxRig`, and `regenerate-schemas` exits with sgen's code (054f823's carry-on fails it). `check-workflow.ps1` fails on a template value still `CHANGE-ME` that its Replace does not fill (it would have built as the text) and fills `rigId` as S1, a box's code, not B1. `deploy.ps1`'s Quick Sync warning says the workflow then stops after Go and to set `codec: libx264`.

## Audit cycle 4 (15 Nov 2026)

- Deleted what nothing used: `task.py`'s `reader` and `data_reader` imports and `rig.py`'s `LiveView` re-export (schema, generated C# and rig template regenerate byte-identical); `pyproject.toml`'s commented-out `[project.urls]`; the `.gitignore` lines for `Bonsai/Settings/`, C extensions, PyInstaller, installer logs, Sphinx, Jupyter, IPython and pyenv (`git status --ignored` unchanged); the inline `RunningWheel`'s two `ExternalizedMapping` nodes copied from the include, which nothing set (check-workflow, and a headless run to "The port 'COM97' does not exist"). This file's finished history is cut to one line per item, and the "not changed" reasons that later code overturned (the 29 Oct tool-restore order and `os.system`, the inline `StreamController`, `RecordedFrames`, deploy keeping a machine's layout) are gone; the stories are in git log.

## Audit cycle 3 (15 Nov 2026)

- `scripts\deploy.ps1` no longer copies `config\main.layout` itself: `.bonsai\Setup.ps1`, which it runs, does the same copy through lib-open-rigs' `setup-bonsai.ps1` (tested: a changed machine layout replaced, the old one kept as `main.saved.layout`). `check-workflow.ps1` step 4 drops its own writer refusal, which step 5's `workflow_lint` makes by type (tested with a CsvWriter, VideoWriter and FfmpegVideoWriter), its checks for `ext:HarpDeviceSchema` and `SessionJson` (no C# class left, so step 2 fails on them) and an unused temp folder. `main.bonsai` drops five unused namespaces (`dsp`, `sys`, `cv`, `zmq`, `netmq`; check-workflow and a headless run to "The port 'COM97' does not exist"). `THIRD-PARTY-NOTICES.md` names every package as lib-open-rigs' under its BSD 3-Clause `LICENSE` (it called the lab's MIT and named 0.1.0 files). The "Re-pin open-rigs once rig-config-resolver is merged" item is gone: `pyproject.toml` pins Coen-Lab/lib-open-rigs `main`.

## Audit cycle 2 (15 Nov 2026)

- `scripts\deploy.ps1` stops with exit 1 on a failed cmdlet or .NET call (`$ErrorActionPreference = 'Stop'`): a rig.yml it could not write, or a layout it could not copy, printed the error and exited 0. The Quick Sync probe stays a warning. `scripts\check-workflow.ps1`'s C# build takes stderr without dying on it (Windows PowerShell makes a merged stderr line fatal under 'Stop').
- Checked headless with rig.yml variants (port COM97, no Go): trigger0Frequency 0, no `cameraTriggerController`, exposure 25,000 and an unknown key each stop at Start naming the problem; a missing `portName` says "Value cannot be null. Parameter name: PortName"; an empty rig.yml says only "Object reference not set to an instance of an object."; a missing `rootPath` reaches ready mode.

## Audit cycle 1 (15 Nov 2026)

- Names and docs brought up to date: app-rig-control, app-rig-setup and its `update-workflows.ps1`, the Hardware page and `RigHardware.json`'s `boards`, the template's `codec: h264_qsv`, `ConfigRoot` reaching four nodes, the second camera's `EnableTrigger1`, the RunningWheel and Camera descriptions; `RecordVideo`'s unused `SampleInterval` (no window, no reader) removed; the broken `examples\session.py` (`Experiment` never imported) deleted; the schema check no longer runs sgen twice now `regenerate.py` checks its run.

## Audit cycle 1 (15 Nov 2026): not changed

- The inline RunningWheel, though lib-open-rigs' include reads Position since OpenRigs.Devices 0.1.1-coen-lab.6: moving onto it belongs to the planned move onto `LabRig` and `RigHardware` (Open, below).

## Audit rounds 1 to 3 (15 Nov 2026): not changed

- `.bonsai\Setup.ps1` is the same 15 lines in five task repos (coen-dome-navigation, coen-dome-decision-making, coen-behaviour-box, coen-qc-calibrate-valve, coen-qc-preflight-rig): each repo needs its own bootstrap.
- rig.yml read through `BehaviourBoxRig`, not `LabRig`: `BehaviourBoxRig` is lib-open-rigs' own model, a box's choice of `LabRig`'s parts, not a second reader.

## Open

- Move onto lib's LabRig (ReadLabRig), lib's check-workflow wrapper and RigHardware/RunningWheel; then delete lib's BehaviourBoxRig, the generated C# and config/rig-template.yml; test on BBOX-1 before rollout (Pip, 15 Nov 2026)

## Check on the rig

- **Quick Sync and LogVideoFfmpeg.** The camera recorded by `OpenRigs.Logging:LogVideoFfmpeg` with the template's `videoEncoder: {codec: h264_qsv}` (14 Nov 2026) was checked offline only (`RecordVideo` headless with fake frames and libx264, 150 == 150, `check-videos` clean). Run 30 minutes on GEEK-BBOX1: 90,000 frames == 90,000 CSV rows, CPU, no dropped-frame warning. A rig.yml deployed before 14 Nov 2026 has no `videoEncoder` and encodes with `libx264` until one is added.
- **Session manifest.** Seen on GEEK-BBOX1 (1 Nov 2026): `completed`, `stopped` and `ended-early`. Still to see: `error` (a pulled trigger cable, with the GapWatchdog's message), and the overnight copy checking and copying a real (non-test) experiment to the server.
- **Wheel distance.** Turn the wheel exactly 10 turns during a recording: the `Encoder` value in `BehaviorBoard-Main\BehaviorBoard-Main_44_*.bin` (`AnalogData`) should change by 10 x `countsPerRev` (40,960 at 4096), unwrapping the 16-bit counter, which is about 471 cm on the 150 mm wheel. The inline wheel is in Position mode; a wrong sign or scale points at `countsPerRev` or the encoder wiring. The live view's `BehaviorBoard-Main.encoder` has not been seen moving either.
- **Board clock after a power-cycle.** The clock is set to UTC in every run since 30 Oct 2026 (from the board's own time since 3 Nov 2026: 20 agent-like starts, 0 failed). Still to see: the first session after a board power-cycle.
- **Lost board messages shift every later `harpTime`.** Seen once, 30 Oct 2026 18:04 on GEEK-BBOX1 (`ses-fixkey`, test config): for about 0.4 s, 9 s after Start, both `Camera0Frame` (92) and `AnalogData` (44) lost messages in the board's own log, while the camera got every pulse. Frames pair with trigger events in order, so after the 9 missing events every row's time was 9 frames (0.18 s) late, and the frame counter shows nothing. Not seen in the 14 other runs that day. Checks for now: gaps over 30 ms between `BehaviorBoard-Main_92_*` events, or a step in `harpTime` where `cameraClockNs` steps one period (README). A fix (pairing on time rather than order, or stopping on a gap) is open.
- **A controller `stop` leaves a modal Runtime Error in the editor** (`ExperimentStoppedException`, which is how `stop` ends the workflow so every file closes; 31 Oct 2026). The experiment is clean, but somebody has to click OK at the rig before the next Start; headless it just exits. Decide whether `stop` should end the run some quieter way.
- **Live view in ready mode.** Whether app-rig-setup's heartbeat advertises the stream in ready mode, before Go, was not seen (31 Oct 2026).
- Done on GEEK-BBOX1, 29 Oct to 3 Nov 2026 (results in git log): register dump, camera preview, live exposure and gain, board clock, named devices and hourly chunks, start-up order, live view (a 30-minute run with a listener, a remote viewer), ready mode.

## Raise upstream (open-rigs/open-rigs)

Found while building this workflow on 28 Oct 2026. Open each with the line `*Comment/research by Claude, read/edited by Pip.*` and a fix diff where it is short.

- **BehaviorBoard never sets the board's clock.** Posted 30 Oct 2026 as [open-rigs#6](https://github.com/open-rigs/open-rigs/issues/6); the draft and patch are on GEEK-BBOX1 in `C:\Users\Coen lab\.claude\skills\behaviour-box-performance\`. Once it ships, remove the local `Clock` group and the `HarpClockSet` gate in `Logging`.
- **CameraTriggerController counts the register-dump reply as a trigger.** Comment on open-rigs#4, which already covers the Camera1 subject parsing the Camera0 register and StartCameras not starting output 1. Both trigger subjects parse every `BehaviorEvents` message, so with `DumpRegisters` on, the Read reply of `Camera0Frame` becomes one extra trigger at startup and the first CSV row comes out early. Fix: `FilterMessageType` (Include, Event) before each `Parse`. This repo filters locally in the `Camera` group.
- **RunningWheel takes a Difference in Displacement mode.** New issue. The include sets `EncoderMode` to `Displacement` and still runs `Difference`, `ConvertSigned` and `Accumulate`, which suits `Position` (a running count). The firmware settles it: in Displacement mode `app.c` reports `previous - timer_cnt` and then sets `previous = timer_cnt`, the change over each 2 ms sample, so the chain telescopes to the current sample minus the first, a speed sample rather than a distance. Fix: `Position` with the chain as is, or `Displacement` without the `Difference`. Not the same as ucl-open/acquisition#9 (encoder reset racing the subscription).
- **Template: generated files make a deployed clone look changed.** New issue, with the `.gitattributes` lines from this repo. `deploy.ps1` regenerates `*.Generated.cs` (written LF by bonsai.sgen) and the schema JSON and rig template (written CRLF by Python), so with `core.autocrlf=true`, Git for Windows' default, a fresh deploy leaves `git status` reporting the C# file as modified, and with `false` the other two.
- **Template: `deploy.ps1` ignores failures.** New issue. No native step's exit code is checked, `Setup.ps1` exits 0 whatever Bonsai's restore returned, and `regenerate.py` ignores `os.system`, so a failed deploy exits 0. This repo's fix: `Assert-Success` after each step, and `regenerate.py` checks its sgen run.
- **Template: a new project's first deploy writes the C# classes to the project root.** Posted 29 Oct 2026 as [open-rigs#5](https://github.com/open-rigs/open-rigs/issues/5). This repo restores the tools first and creates `src\Extensions` before `Push-Location`.
- **Template: `pyproject.toml` declares a console script with no module.** New issue. `<project> = "<package>.cli:main"`, but the template has no `cli.py`; running it fails with `ModuleNotFoundError`. Removed here.
- **Template: `Extensions.csproj` compiles C# that Bonsai cannot.** New issue. Bonsai compiles a workflow's `Extensions` folder itself with the .NET Framework's csc (C# 5), but the template's `Extensions.csproj` builds with the SDK's current C#, so `dotnet build` and the editor pass `$"..."` and other C# 6 features that stop the workflow at Start with "Error building script extensions" (this repo's 52cc533, fixed in 4b4cb4d). Fix: `<LangVersion>5</LangVersion>`, as this repo now has.
- **StreamController names a session the folder does not have.** Posted 30 Oct 2026 as [open-rigs#7](https://github.com/open-rigs/open-rigs/issues/7); this repo streams with OpenRigs.LiveView's `StreamDevices`, which takes the key from the folder, so it does not depend on the fix.
- **Live view has no "recording ended" signal.** Posted 30 Oct 2026 as [open-rigs#8](https://github.com/open-rigs/open-rigs/issues/8).
- **FFmpeg writer for LogVideo.** Tracked in ucl-open/av-dome#25 and ucl-open/support#9. Add this repo as a second user: Bonsai.Vision's writer crashed 30-minute sessions on the box's N150; this repo now uses lib-open-rigs' `LogVideoFfmpeg`.

## Later

- Switch to released OpenRigs packages once open-rigs publishes one with the camera fixes and the config operators ([lib-open-rigs](https://github.com/Coen-Lab/lib-open-rigs) `patches/README.md`, "Switching to upstream").
- Move `copier.yml` handling to upstream once roadmap#38's fix lands, then `copier update` from `gh:open-rigs/open-rigs`.

## app-rig-setup

- **Back up `rig.yml` to the share.** Decided 28 Oct 2026: the rig's local `rig.yml` is the master and is edited there; app-rig-setup copies it one way up to `K:\config\<MACHINE>\`, so a rig runs while the server is down. Not server-to-rig (`config/` on the share is writable by rigs only) and not a two-way mirror. The plan is in app-rig-setup's `BACKLOG.md`.

## Audit 2 Nov 2026 (rig.yml-driven Harp identity, dump and register map): not changed

- `usbSerial` required in the schema for `behaviorBoard` only: it is the only Harp kind in this schema, and `RecordHarpDevices` requires it of any Harp device.

## Audit 1 Nov 2026 (session manifest v2, OpenRigs.Manifest): not changed

Do not raise again without new information.

- Without ExperimentControl, an error elsewhere in the workflow is recorded as `stopped` with `error: null`: the node cannot see it, and the manifest's notes say so. Connect a run input (as this workflow does) where the cause matters.
- A saved workflow writes ExperimentManifest's settings twice, on the group and on its inner `ExperimentManifestSettings`: the group's are what hand-written XML (this repo's) uses, the inner node is what survives Bonsai's copies. Tested: load, the editor's copy, save and reload keep one settings node.
- A missing `PathPrefix` stops the workflow at build rather than running without a manifest: a session with no record is the thing to stop for.
- `expected.found` is counted at the node's writes and not refreshed by the overnight copy, which checks presence itself.

## Audit 28 Oct 2026: not changed

Do not raise again without new information.

- Unused template packages in `.bonsai/Bonsai.config` (Sleap, Pylon, TensorFlow and others): harmless, and keeping parity with the template eases `copier update`.
- Unused PulseController classes and the `version` Literal in the rig schema: both come from the upstream schema and break nothing today.
- Rebuilding the local packages to compare hashes: the patches (now commits in lib-open-rigs) applied to 3788bfb reproduce the built source tree exactly, and nupkg hashes are not deterministic.
- Sending `StopCameras` at startup: the Behavior firmware stops the camera outputs whenever the board goes to Standby, which Bonsai does on disconnect; only a hard crash leaves them running.
- `main.bonsai` without its generator script: the committed XML is the artefact and is edited from now on.

## Audit 29 Oct 2026 (bonsai.sgen deploy): not changed

- Running sgen once instead of twice (regenerate.py's and deploy's give byte-identical output here): template parity; left to the maintainers as a question in the upstream issue.

## Audit 30 Oct 2026 (clock, camera, named devices, live view): not changed

Do not raise again without new information.

- Shortening the board-clock `StartupWatchdog` below the 5 s before the triggers start: tried at 4 s, and it stopped every run. Its time counts from the workflow's subscription, before the config and camera are up; in 35 sessions on 30 Oct 2026 no CSV row was on the power-on count.
- Holding the triggers until the clock is set: the clock was set within the first second in every run, and the StartupWatchdog stops the run if it is not.
- `SynchronizeTimestamp` truncating to whole seconds (board up to 1 s behind the PC): Bonsai.Harp's own operator, the README says so, and frames and board events share the Harp clock within a session.
- The clock write landing during the board's open-time dump: Bonsai.Harp's `Device` holds events back until the OperationControl echo and reads commands from straight after its write; every 30 Oct file is UTC-named.
- One 1,000 us margin for every binning and trigger rate: OpenRigs.Video's own default exposure is `1e6 / 50 - 1000`, its `TriggeredSpinnaker` sets `TriggerOverlap` to `ReadOut`, and 19,000 us ran at the full 50 Hz.
- The camera arming before `ExposureFitsTrigger` refuses: the camera waits for its subject, which never comes; at 19,001 us ffmpeg never started and no experiment folder was made.
- A `/` or `\` in `SubjectId` or `SessionId` making folders before the session key stops the run: rare, the message names the cause, and the run stops before the first trigger.
- A Windows firewall prompt for this repo's `Bonsai.exe` (it has no program rule): the port rule for 5556 and 5558 is there, and the loopback listener got every message in the 30-minute run.
- Saving the workflow writing panel values into `main.bonsai`: the README says never to save.
- `Bonsai.config`'s four preview packages written by hand: the restore installed them, every DLL is present, and the preview opened in every 30 Oct test.
- `config\main.layout` line endings: it is CRLF, git normalises it, and Bonsai reads it either way.
- One reusable camera group (subject names externalized) instead of a copy per camera: one camera today, and the restructure moves node indices and can only be proven on the rig. README lists what a copy takes.
- One `SubscribeSubject` per device per scope, fanned out, instead of two or three: fewer labels to retype, but the same layout churn, and a misspelt label already stops the build.
- Checking the kind half of `RigDevice`'s name against the group it reads (`Camera` selector, `Camera-...` name): only a hand-renamed kind breaks it, and RigDevice sees a dictionary, not the key it came from.
- A clearer error than YamlDotNet's "Property 'trigger0Frequency' not found" for a file in the old layout: README quotes it, and GEEK-BBOX1, the only rig on it, is regrouped.
- `RigDevice` reading `Name` once when the workflow is built, not per element: Bonsai's convention for a property nothing maps.
- `camera.overhead.triggerFrequency` beside the board's `trigger0Frequency`: the upstream schema's field; the template's header says this rig takes the rate from the board.
