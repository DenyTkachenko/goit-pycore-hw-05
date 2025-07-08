from functools import wraps

"""
Note: KeyError handling is not included in the input_error decorator, 
as it is considered a system-level error rather than an input error. 
To maintain the decorator's universality, KeyError is handled 
within each function where it may occur. This allows each function 
to return a custom error message specific to its context.
"""

#Decorator
def input_error(cmd='', expected_args=None):
    if expected_args is None:
        expected_args = []

    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (ValueError, IndexError):
                usage = f'{cmd} ' + ' '.join(f'<{arg}>' for arg in expected_args)
                return f'The "{cmd}" command expects {len(expected_args)} arguments. Usage: {usage}'
            except Exception as e:
                return f"Error: {e}"
        return inner
    return decorator

def parse_input(user_input):
    if not user_input.strip():
        return "", []
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error('add', ['name', 'phone'])
def add_contact(args, contacts):
    name, phone = args
    key = name.capitalize()

    if key in contacts:
        return f"Contact with name: {name} already exists."
    contacts[key] = phone
    return "Contact added."


@input_error('change', ['name', 'phone'])
def change_contact(args, contacts):
    name, phone = args
    key = name.capitalize()

    if key not in contacts:
        return f"Contact with name: {name} does not exist."

    contacts[key] = phone
    return "Contact updated."

@input_error('phone', ['name'])
def show_phone(args, contacts):
    name = args[0]
    key = name.capitalize()

    if key not in contacts:
        return f"Contact with name: {name} does not exist."

    return contacts[key]

def show_all(contacts):
    if not contacts:
        return "No contacts found."

    return contacts

def main():
    contacts = {}
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        match command:
            case "close" | "exit":
                print("Good bye!")
                break
            case "hello":
                print("How can I help you?")
            case "add":
                print(add_contact(args, contacts))
            case "change":
                print(change_contact(args, contacts))
            case "phone":
                print(show_phone(args, contacts))
            case "all":
                print(show_all(contacts))
            case _:
                print("Invalid command.")

if __name__ == "__main__":
    main()