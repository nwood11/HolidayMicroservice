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
        "01-01-2024",   # January 1st, 2024 (New Years)
        "12-25-2024",   # December 25th, 2024(Christmas)
        "13-32-2024",   # Not a real date
        "01-20-2023",   # January 20th, 2023 (not a holiday)
        "",             # Empty string
        "12-2024",      # Whole month of December
        "01-2024",      # Whole month of January
        "09-03-2018",   # September 3, 2018 (Labor ssDay)
        "03-2024"       # Whole month of March
    ]

    for test in tests:
        print("Sending request:", test)
        response = send_request(test)
        print("Response:", response)
        print()
