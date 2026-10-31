import asyncio
import aiocoap

async def main():

    uri = "coap://127.0.0.1:5683/iot/lab/message"

    try:
        protocol = await aiocoap.Context.create_client_context()

        print("CoAP Client")
        print("Sending GET request...")
        print("URI:", uri)

        request = aiocoap.Message(
            code=aiocoap.GET,
            uri=uri
        )

        response = await protocol.request(request).response

        print("\nResponse:")
        print("Code:", response.code)
        print("Payload:", response.payload.decode("utf-8"))

        student_id = "B23DCCN355"
        student_name = "Do Thi Thu Hue"

        message = (
            f"Xin chao tu CoAP Client - "
            f"{student_id} - {student_name}"
        )

        print("\nSending POST request...")
        print("Payload:", message)

        request = aiocoap.Message(
            code=aiocoap.POST,
            uri=uri,
            payload=message.encode("utf-8")
        )

        response = await protocol.request(request).response

        print("\nResponse:")
        print("Code:", response.code)
        print("Payload:", response.payload.decode("utf-8"))

        await protocol.shutdown()

    except Exception as e:
        print("\nError: Khong the ket noi den CoAP Server!")
        print("Chi tiet:", e)


if __name__ == "__main__":
    asyncio.run(main())
