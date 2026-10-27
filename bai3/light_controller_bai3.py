import asyncio
import json

import aiocoap
from aiocoap.numbers.contentformat import ContentFormat


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


async def show_status(protocol, device_id):
    request = aiocoap.Message(code=aiocoap.GET, uri=resource_uri(device_id))
    response = await protocol.request(request).response
    print(f"Ma phan hoi CoAP: {describe_response_code(response.code)}")

    if not response.code.is_successful():
        print(f"Thong tin: {response.payload.decode('utf-8', errors='replace')}")
        return

    response_device_id, status = decode_status(response.payload, device_id)
    print(
        f"Du lieu: "
        f"{{\"device_id\":\"{response_device_id}\",\"status\":\"{status}\"}}"
    )


async def set_status(protocol, device_id, command):
    payload = json.dumps(
        {"device_id": device_id, "command": command}
    ).encode("utf-8")
    request = aiocoap.Message(
        code=aiocoap.PUT,
        uri=resource_uri(device_id),
        payload=payload,
        content_format=ContentFormat.JSON,
    )
    response = await protocol.request(request).response
    print(f"Ma phan hoi CoAP: {describe_response_code(response.code)}")

    if not response.code.is_successful():
        print(f"Thong tin: {response.payload.decode('utf-8', errors='replace')}")
        return

    response_device_id, status = decode_status(response.payload, device_id)
    action = "bat den" if status == "ON" else "tat den"
    print(f"Da {action} thiet bi {response_device_id}")


async def main():
    protocol = await aiocoap.Context.create_client_context()
    selected_device = "light01"
    print("Bo dieu khien thiet bi CoAP da san sang.")
    print(f"Thiet bi: {', '.join(DEVICE_IDS)}")
    print("Nhap lenh theo huong dan ben duoi:")
    print("  DEVICE fan01 : chon quat fan01")
    print("  ON           : bat thiet bi dang chon")
    print("  OFF          : tat thiet bi dang chon")
    print("  STATUS       : xem trang thai thiet bi dang chon")
    print("  EXIT         : thoat chuong trinh")

    try:
        while True:
            try:
                command = await asyncio.to_thread(
                    input,
                    f"[{selected_device}] Nhap lenh "
                    "(vi du: ON, STATUS, DEVICE fan01, EXIT): ",
                )
            except EOFError:
                print("\nKhong con du lieu nhap. Controller se dung.")
                break

            command = command.strip().upper()
            if command == "EXIT":
                break

            if command.startswith("DEVICE "):
                requested_device = command.partition(" ")[2].strip().lower()
                if requested_device not in DEVICE_IDS:
                    print(
                        f"Ma thiet bi khong hop le. Hay chon: "
                        f"{', '.join(DEVICE_IDS)}"
                    )
                else:
                    selected_device = requested_device
                    print(f"Da chon thiet bi {selected_device}")
                continue

            if command == "STATUS":
                print(f"Dang doc trang thai thiet bi {selected_device} (GET)...")
                try:
                    await show_status(protocol, selected_device)
                except (aiocoap.error.Error, TimeoutError, OSError) as error:
                    print(f"Gui GET that bai: {error}")
                except ValueError as error:
                    print(f"Khong doc duoc trang thai: {error}")
                continue

            if command not in {"ON", "OFF"}:
                print(
                    f"Lenh '{command}' khong hop le; gui den Server de "
                    "nhan ma loi CoAP."
                )

            print(
                f"Dang gui lenh {command} den thiet bi "
                f"{selected_device} (PUT)..."
            )
            try:
                await set_status(protocol, selected_device, command)
            except (aiocoap.error.Error, TimeoutError, OSError) as error:
                print(f"Gui PUT that bai: {error}")
            except ValueError as error:
                print(f"Khong doc duoc phan hoi: {error}")
    finally:
        await protocol.shutdown()

    print("Bo dieu khien da dung.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBo dieu khien da dung.")