import zmq
import json

def send_request(request):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    socket.send(json.dumps(request).encode("utf-8"))
    response = socket.recv()
    return json.loads(response.decode("utf-8"))

if __name__ == "__main__":
    # some basic tests
    tests = [
        "January",
        "December 25",
        "Decemmmber",
        "Jany 20",
        "",
        "December",
        "January 1"
    ]

    for test in tests:
        print("Sending request:", test)
        response = send_request(test)
        print("Response:", response)
        print()

