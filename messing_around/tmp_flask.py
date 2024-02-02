import asyncio

import flask
import unsync

app = flask.Flask(__name__)


@unsync.unsync
def unsync_thread_task():
    flask.g.unsync_thread = "unsync_thread"


@unsync.unsync
async def unsync_async_task():
    flask.g.unsync_async = "unsync_async"


async def async_task():
    flask.g.foo = "async"


with app.app_context():
    asyncio.run(async_task())  # contrived example, but hopefully illustrates the point
    print(flask.g.foo)

    # I fell down this rabbit hole for a while, surprisingly hard to trace what is happening here
    unsync_async_task().result()  # asyncio copies the current Context when running tasks, so flask.g is still accessible in the async scope but is now global data accessible from multiple threads. Setting a context local will be local to this scope
    print(flask.g.unsync_async)

    unsync_thread_task().result()  # threads copy the current Context at the time of creation
    print(flask.g.unsync)  # unreachable
