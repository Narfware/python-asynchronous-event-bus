from event_bus import EventBus
import time
import threading


def main():
    bus = EventBus()
    bus.add_handlers("user_created", [send_email, destroy_company, send_message, compute_cosmos])

    create_user = CreateUser(bus)

    create_user.execute({"name": "Joana", "email": "joanadoe@gmail.com"})


def send_email(data):
    time.sleep(4)
    print(f'email sended to {data.get("email")} in thread {threading.get_ident()}')


def send_message(data):
    time.sleep(3)
    print(f'message sended to {data.get("email")} in thread {threading.get_ident()}')


def compute_cosmos(data):
    time.sleep(2)
    print(f"cosmos computed in thread {threading.get_ident()}")


def destroy_company(data):
    time.sleep(1)
    print(f"destroying company in thread {threading.get_ident()}")
    raise Exception("Company destroyed successfully")


class CreateUser:
    def __init__(self, event_bus):
        self.event_bus = event_bus

    def execute(self, user_data):
        print(f"creating user {user_data.get('name')}")

        self.event_bus.emit("user_created", user_data)

        print("user created")


main()
