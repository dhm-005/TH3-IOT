
import asyncio
from datetime import datetime

import aiocoap
import aiocoap.resource as resource


class MessageResource(resource.Resource):

    def __init__(self):
        super().__init__()
        self.latest_message = "Xin chao tu CoAP Server"

    async def render_get(self, request):
        print("\nGET request received: /iot/lab/message")

        payload = self.latest_message.encode("utf-8")

        return aiocoap.Message(
            code=aiocoap.CONTENT,
            payload=payload
        )
    
    async def render_post(self, request):
        message = request.payload.decode("utf-8")
        self.latest_message = message
        current_time = datetime.now().strftime("%H:%M:%S")

        print("\nPOST request received:")
        print("Payload:", message)
        print("Time:", current_time)

        return aiocoap.Message(
            code=aiocoap.CHANGED,
            payload="Server da nhan thong diep".encode("utf-8")
        )


async def main():
    root = resource.Site()
    root.add_resource(
        ["iot", "lab", "message"],
        MessageResource()
    )

    await aiocoap.Context.create_server_context(
        root,
        bind=("127.0.0.1", 5683)
    )

    print("CoAP Server started on port 5683")
    print("Resource: coap://localhost:5683/iot/lab/message")

    await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nCoAP Server stopped.")
