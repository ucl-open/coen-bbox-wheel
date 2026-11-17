"""The task file's schema: config/task-bbox.yml, which rig-control copies at launch and again at Go with the form's edits;
the workflow reads the copy (TaskPath) at Go and logs it as Settings_Task. The box's one task setting is how long to record."""

from typing import Literal

from open_rigs.core.task import Task
from pydantic import Field
from swc.aeon.schema import BaseSchema

from ucl_open_coen_bbox_wheel import __semver__


class UclOpenCoenBboxWheelTaskParameters(BaseSchema):
    """Task params."""

    run_length_minutes: int = Field(
        default=30,
        ge=1,
        le=9999,
        description="How long to record, in whole minutes (1 to 9999): the run takes this many minutes of camera frames from the experiment folder's creation, just after Go, and then ends",
    )


class UclOpenCoenBboxWheelTaskLogic(Task):
    """Top-level task logic schema."""

    version: Literal[__semver__] = __semver__
    name: Literal["UclOpenCoenBboxWheel"] = Field(default="UclOpenCoenBboxWheel", description="Name of the task")
    task_parameters: UclOpenCoenBboxWheelTaskParameters
