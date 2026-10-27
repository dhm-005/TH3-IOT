import argparse
import asyncio
import json
from datetime import datetime

import aiocoap


DEVICE_IDS = ("light01", "fan01", "pump01")


def resource_uri(device_id):
    return f"coap://localhost:5683/iot/lab/{device_id}/status"


def describe_response_code(code):
    descriptions = {
        aiocoap.CONTENT: "2.05 Noi dung",
        aiocoap.CHANGED: "2.04 Da cap nhat",
        aiocoap.BAD_REQUEST: "4.00 Yeu cau khong hop le",
        aiocoap.NOT_FOUND: "4.04 Khong tim thay tai nguyen",
    }
    return descriptions.get(code, f"Ma so {code.value}")


def decode_status(payload, device_id):
    try:
        data = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("Server tra ve JSON khong hop le.") from error

    if (
        not isinstance(data, dict)
        or data.get("device_id") != device_id
        or data.get("status") not in {"ON", "OFF"}
    ):
        raise ValueError("Server tra ve trang thai thiet bi khong hop le.")

    return data["device_id"], data["status"]


def display_status(payload, device_id, label):
    device_id, status = decode_status(payload, device_id)
    received_at = datetime.now().strftime("%H:%M:%S")
    print(f"[{received_at}] {label}")
    print(f"Thiet bi: {device_id}")
    print(f"Trang thai: {status}")


async def monitor_device(protocol, device_id):
    request = protocol.request(
        aiocoap.Message(
            code=aiocoap.GET,
            uri=resource_uri(device_id),
            observe=0,
        )
    )
    print(f"Dang dang ky Observe cho {device_id}...")

    try:
        initial_response = await request.response
    except (aiocoap.error.Error, TimeoutError, OSError) as error:
        print(f"Khong dang ky duoc Observe cho {device_id}: {error}")
        return

    if not initial_response.code.is_successful():
        print(
            f"Dang ky Observe cho {device_id} that bai: "
            f"{describe_response_code(initial_response.code)}"
        )
        print(f"Thong tin: {initial_response.payload.decode('utf-8', errors='replace')}")
        return

    observation = request.observation
    if observation is None:
        raise RuntimeError(
            f"Yeu cau Observe cua {device_id} khong tao duoc observation."
        )

    print(f"Da dang ky Observe cho {device_id}.")
    try:
        display_status(initial_response.payload, device_id, "Trang thai ban dau")
    except ValueError as error:
        print(f"Khong doc duoc trang thai ban dau cua {device_id}: {error}")
        return

    try:
        async for notification in observation:
            if not notification.code.is_successful():
                print(
                    f"Thong bao Observe cua {device_id} loi: "
                    f"{describe_response_code(notification.code)}"
                )
                continue

            try:
                display_status(
                    notification.payload,
                    device_id,
                    "Trang thai vua cap nhat",
                )
            except ValueError as error:
                print(f"Khong doc duoc cap nhat cua {device_id}: {error}")
    except (aiocoap.error.Error, TimeoutError, OSError) as error:
        print(f"Ket noi Observe cua {device_id} da ket thuc: {error}")


async def main():
    parser = argparse.ArgumentParser(
        description="Theo doi thiet bi bang CoAP Observe."
    )
    parser.add_argument(
        "device_id",
        nargs="*",
        choices=DEVICE_IDS,
        help=(
            "Ma thiet bi can theo doi. Mac dinh theo doi tat ca: "
            + ", ".join(DEVICE_IDS)
        ),
    )
    args = parser.parse_args()
    device_ids = args.device_id or DEVICE_IDS

    print(f"Monitor se theo doi: {', '.join(device_ids)}")
    print("Nhan Ctrl+C de dung Monitor.")
    protocol = await aiocoap.Context.create_client_context()

    try:
        await asyncio.gather(
            *(monitor_device(protocol, device_id) for device_id in device_ids)
        )
    finally:
        await protocol.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nMonitor da dung.")