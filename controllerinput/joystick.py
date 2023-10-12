import csv
import datetime
from controllerinput import joystick_controller


# ... (other imports and class definitions)

class Joystick(InputDevice):

    def __init__(self):
        self.joystick_controller = JoystickController()
        self.joystick_controller.initialize_joysticks()

    def get_input(self):
        data = self.joystick_controller.get_data()

        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        filename = datetime.datetime.now().strftime("%Y-%m-%d") + ".csv"

        with open(filename, "a", newline='') as csvfile:
            fieldnames = ['Timestamp', 'Joystick Output']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write a row for each instance of joystick data
            for instance in data:
                writer.writerow({'Timestamp': timestamp, 'Joystick Output': json.dumps(instance)})

        return None  # Return None after writing the data




#create a 2 colum csv file with one colum as the timestamp otherr joystick output.
#have the filename be the date. 
