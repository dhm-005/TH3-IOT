
import logging
import asyncio
import json

from datetime import datetime
from aiocoap import Context, Message, GET


logging.basicConfig(level=logging.INFO)

URI = "coap://localhost:5683/iot/lab/sensor01/data"


async def main():
    protocol = await Context.create_client_context()
    count = 0

    print("Monitoring CoAP Client is running")
    print("Press Ctrl+C to stop\n")

    try:
        while True:
            try:
                # Gửi yêu cầu GET
                request = Message(
                    code=GET,
                    uri=URI
                )

                response = await protocol.request(request).response

                # Phân tích dữ liệu JSON
                payload = json.loads(
                    response.payload.decode("utf-8")
                )

                now = datetime.now().strftime("[%H:%M:%S]")
                count += 1

                device_id = payload["device_id"]
                temperature = payload["temperature"]
                humidity = payload["humidity"]

                print(f"{now} Received sensor data")
                print()
                print("Device:", device_id)
                print(f"Temperature: {temperature} C")
                print(f"Humidity: {humidity} %")
                print()

                # Kiểm tra cảnh báo
                warning = False

                if temperature > 35:
                    print("CANH BAO: Nhiet do cao")
                    warning = True

                if humidity < 40:
                    print("CANH BAO: Do am thap")
                    warning = True

                if not warning:
                    print("Trang thai: Binh thuong")

                print("\n------------------------------\n")

            except Exception as e:
                print("Failed to fetch sensor data:", e)
                print("Will retry in 3 seconds...\n")

            # Truy vấn định kỳ
            await asyncio.sleep(3)

    finally:
        await protocol.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nMonitoring CoAP Client stopped")
