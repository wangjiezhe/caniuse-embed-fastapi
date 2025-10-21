# type: ignore

from server import app
from workers import WorkerEntrypoint


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        import asgi

        return await asgi.fetch(app, request.js_object, self.env)
