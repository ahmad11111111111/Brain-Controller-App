import json
from .joystick_controller import JoystickController
from libbci import InputDevice


class Joystick(InputDevice):

    def __init__(self):
        self.joystick_controller = JoystickController()
        self.joystick_controller.initialize_joysticks()

    def get_input(self):
        data = self.joystick_controller.get_data()

        # Write data to a file with newline-separated JSON format
        filename = "joystick_data.txt"
        with open(filename, "a") as file:
            for instance in data:
                json.dump(instance, file)
                file.write('\n')  # Add a newline after each instance
        return None  # Return None after writing the data
