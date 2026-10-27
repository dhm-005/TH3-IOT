import asyncio
import json

import aiocoap
import aiocoap.resource as resource
from aiocoap.numbers.contentformat import ContentFormat


DEVICE_IDS = ("light01", "fan01", "pump01")


class SmartLightResource(resource.ObservableResource):
    def __init__(self, device_id):
        super().__init__()
        self.device_id = device_id
        self.status = "OFF"
        self._observer_count = 0

    def _status_message(self):
        payload = json.dumps(
            {"device_id": self.device_id, "status": self.status}
        ).encode("utf-8")
        return aiocoap.Message(
            code=aiocoap.CONTENT,
            payload=payload,
            content_format=ContentFormat.JSON,
        )

    async def render_get(self, request):
        return self._status_message()

    async def render_put(self, request):
        try:
            payload = json.loads(request.payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return aiocoap.Message(
                code=aiocoap.BAD_REQUEST,
                payload=b"Du lieu gui len phai la JSON UTF-8 hop le.",
            )

        if not isinstance(payload, dict):
            return aiocoap.Message(
                code=aiocoap.BAD_REQUEST,
                payload=b"Du lieu gui len phai la mot doi tuong JSON.",
            )

        command = payload.get("command")
        if payload.get("device_id") != self.device_id or not isinstance(
            command, str
        ):
            return aiocoap.Message(
                code=aiocoap.BAD_REQUEST,
                payload=(
                    f"Can dung device_id {self.device_id} va command ON hoac OFF."
                ).encode("utf-8"),
            )

        command = command.strip().upper()
        if command not in {"ON", "OFF"}:
            return aiocoap.Message(
                code=aiocoap.BAD_REQUEST,
                payload=b"Lenh khong hop le. Chi chap nhan ON hoac OFF.",
            )

        print(f"Nhan lenh PUT: thiet bi={self.device_id}, lenh={command}")
        previous_status = self.status
        self.status = command

        if self.status != previous_status:
            print(
                f"Trang thai {self.device_id} thay doi: "
                f"{previous_status} -> {self.status}"
            )
            self.updated_state()
            print(f"Da gui thong bao Observe: {self.status}")
        else:
            print(f"Trang thai {self.device_id} giu nguyen: {self.status}")

        response = self._status_message()
        response.code = aiocoap.CHANGED
        return response

    def update_observation_count(self, newcount):
        if newcount > self._observer_count:
            print(f"Co Monitor dang ky theo doi {self.device_id}")
        elif newcount < self._observer_count:
            print(f"Mot Monitor ngung theo doi {self.device_id}")
        self._observer_count = newcount


async def main():
    site = resource.Site()
    site.add_resource(
        [".well-known", "core"],
        resource.WKCResource(site.get_resources_as_linkheader),
    )
    for device_id in DEVICE_IDS:
        site.add_resource(
            ["iot", "lab", device_id, "status"],
            SmartLightResource(device_id),
        )

    server = await aiocoap.Context.create_server_context(
        site,
        bind=("localhost", 5683),
    )

    print("CoAP Server da khoi dong.")
    print(f"Thiet bi mo phong: {', '.join(DEVICE_IDS)}")
    for device_id in DEVICE_IDS:
        print(f"Tai nguyen: /iot/lab/{device_id}/status")
        print(f"Dia chi: coap://localhost:5683/iot/lab/{device_id}/status")

    try:
        await asyncio.get_running_loop().create_future()
    finally:
        await server.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nCoAP Server da dung.")