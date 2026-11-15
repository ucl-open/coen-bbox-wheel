# The behaviour box's rig schema is the lab's, in lib-open-rigs (open_rigs.rigs.lab_rig's BehaviourBoxRig,
# a box's choice of the lab rig model's parts), not this workflow's: every workflow on a behaviour box
# reads the same rig.yml, so they all take it from there.
from open_rigs.components.harp_boards import BehaviorBoard
from open_rigs.components.video import SpinnakerCamera, VideoEncoder
from open_rigs.rigs.lab_rig import BehaviourBoxRig

__all__ = ["BehaviorBoard", "BehaviourBoxRig", "SpinnakerCamera", "VideoEncoder"]
