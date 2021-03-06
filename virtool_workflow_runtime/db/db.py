"""Functions for accessing the Virtool database."""
import asyncio
from os import getenv
from typing import Optional, Any

from motor.motor_asyncio import AsyncIOMotorClient

from virtool_core.db.bindings import BINDINGS
from virtool_core.db.core import DB, Collection
from virtool_core.utils import timestamp
from virtool_workflow import WorkflowFixture, Workflow, WorkflowExecutionContext

DATABASE_CONNECTION_URL_ENV = "DATABASE_CONNECTION_URL"
DATABASE_CONNECTION_URL_DEFAULT = "mongodb://localhost:27017"
DEFAULT_DATABASE_NAME = "virtool"


class VirtoolDatabase(WorkflowFixture, param_names=["database", "db"]):
    """
    An interface to the Virtool database.

    Individual database Collections can be accessed as attributes or as items.

    .. code-block::
        database = VirtoolDatabase()
        caches = database.caches
        # or
        caches = database["caches"]
    """

    def __init__(self,
                 db_name: Optional[str] = DEFAULT_DATABASE_NAME,
                 db_conn_url: Optional[str] = None):
        """
        :param db_name: The name of the MongoDB database. 'virtool' will
            be used if None is provided.
        :param db_conn_url: The MongoDB connection URL. If None is provided
            the value of the 'DATABASE_CONNECTION_URL` environment variable
            is used. If the variable is not set then 'mongodb://localhost:27017' is used.
        """
        if not db_conn_url:
            db_conn_url = getenv(DATABASE_CONNECTION_URL_ENV,
                                 default=DATABASE_CONNECTION_URL_DEFAULT)

        self._client = AsyncIOMotorClient(db_conn_url, io_loop=asyncio.get_event_loop())[db_name]
        self._db = DB(self._client, None)

        for binding in BINDINGS:
            setattr(self, binding.collection_name, getattr(self._db, binding.collection_name))

    @staticmethod
    def __fixture__() -> Any:
        """Return an instance of :class:`VirtoolDatabase` to be used as a workflow fixture."""
        return VirtoolDatabase()

    def __getitem__(self, item) -> Collection:
        """Get a particular database collection."""
        return getattr(self._db, item)

    def send_updates_to_database_for_job(
            self,
            job_id: str,
            context: WorkflowExecutionContext,
            workflow: Workflow
    ):
        """
        Send updates to the jobs database when the WorkflowExecutionContext is updated.

        :param job_id: Id of the job in the Virtool database
        :param context: The :class:`WorkflowExecutionContext` instance
        :param workflow: The :class:`Workflow` being executed
        """
        async def _send_update(_, update: str):
            await self._db.jobs.update_one({"_id": job_id}, {
                "$set": {
                    "state": str(context.state)
                },
                "$push": {
                    "status": {
                        "state": str(context.state),
                        "stage": workflow.steps[context.current_step - 1].__name__,
                        "error": context.error,
                        "progress": context.progress,
                        "update": update,
                        "timestamp": timestamp(),
                    }
                }
            })

        context.on_update(_send_update)
