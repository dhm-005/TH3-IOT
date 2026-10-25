
import logging
import asyncio
import random
import json
import aiocoap
import aiocoap.resource as resource

from aiocoap.numbers.contentformat import ContentFormat


logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)


class SensorDataResource(resource.Resource):

    def __init__(self, device_id):
        super().__init__()
        self.device_id = device_id
        self.data = {}
        self.update_data()

    def update_data(self):
        # Sinh dữ liệu cảm biến mới
        self.data = {
            "device_id": self.device_id,
            "temperature": round(random.uniform(20, 40), 1),
            "humidity": round(random.uniform(30, 80), 1)
        }

    async def render_get(self, request):
        # Trả về dữ liệu cảm biến mới nhất
        content = json.dumps(self.data).encode("utf-8")

        return aiocoap.Message(
            payload=content,
            content_format=ContentFormat.JSON
        )


async def update_sensor(sensor):
    # Cập nhật dữ liệu cảm biến mỗi 3 giây
    while True:
        await asyncio.sleep(3)
        sensor.update_data()


async def main():
    # Tạo cây tài nguyên
    root = resource.Site()

    root.add_resource(
        [".well-known", "core"],
        resource.WKCResource(root.get_resources_as_linkheader)
    )

    # Đăng ký cảm biến
    device_id = "sensor01"
    sensor = SensorDataResource(device_id)

    root.add_resource(
        ["iot", "lab", device_id, "data"],
        sensor
    )

    # Khởi chạy CoAP Server
    server = await aiocoap.Context.create_server_context(
        root,
        bind=("localhost", 5683)
    )

    # Chạy tác vụ cập nhật cảm biến nền
    task = asyncio.create_task(update_sensor(sensor))

    print("Sensor CoAP Server is running")
    print("URI: coap://localhost:5683/iot/lab/sensor01/data")

    try:
        await asyncio.get_running_loop().create_future()
    finally:
        task.cancel()
        await server.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSensor CoAP Server stopped")
