"""Restate application entry point.

Registers all Restate virtual objects, workflows, and services
and starts the HTTP endpoint that the Restate server discovers.
"""

from __future__ import annotations

import restate

from restate_services.project_object import project_object
from restate_services.credit_workflow import credit_workflow
from restate_services.external_data_service import external_data_service

app = restate.app(
    services=[
        project_object,
        credit_workflow,
        external_data_service,
    ],
)
