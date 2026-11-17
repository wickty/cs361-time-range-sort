"""Independent time-range client. Start microservice.py in another terminal."""
import json
import zmq

ADDRESS = "tcp://127.0.0.1:5554"
TESTS = [
    ("Date range", {"action": "range", "items": [
        {"id": 1, "date": "2026-10-01"}, {"id": 2, "date": "2026-10-10"},
        {"id": 3, "date": "2026-10-20"}], "field": "date",
        "start": "2026-10-05", "end": "2026-10-15"}),
    ("Inclusive boundaries and ascending order", {"action": "range", "items": [
        {"id": 2, "date": "2026-10-15"}, {"id": 1, "date": "2026-10-05"}],
        "field": "date", "start": "2026-10-05", "end": "2026-10-15"}),
    ("Invalid range", {"action": "range", "items": [], "field": "date",
        "start": "2026-10-15", "end": "2026-10-05"}),
]


def call_service(socket, request):
    socket.send_json(request)
    return socket.recv_json()


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.setsockopt(zmq.RCVTIMEO, 3000)
    socket.setsockopt(zmq.SNDTIMEO, 3000)
    socket.setsockopt(zmq.LINGER, 0)
    socket.connect(ADDRESS)
    try:
        for label, request in TESTS:
            print(f"\n--- {label} ---")
            print("REQUEST:", json.dumps(request))
            reply = call_service(socket, request)
            print("RESPONSE:", json.dumps(reply))
    except zmq.Again:
        print("Timed out. Start the microservice in another terminal first.")
        raise SystemExit(1)
    finally:
        socket.close()
        context.term()


if __name__ == "__main__":
    main()
