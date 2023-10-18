

import pygame
import multiprocessing
import time
class JoystickController:
    def __init__(self):
        pygame.init()
        self.joysticks = []
        self.initialize_joysticks()
        self.data_queue = multiprocessing.Queue()  # Use a Queue for data
        self.process = None
        self.terminate_event = multiprocessing.Event()  # Initialize the termination event

    def __del__(self):
        self.stop_update_process()

    def initialize_joysticks(self):
        num_joysticks = pygame.joystick.get_count()
        for i in range(num_joysticks):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            self.joysticks.append(joystick)

    def check_joystick_connection(self):
        connected_joysticks = []
        for joystick in self.joysticks:
            if joystick.get_init():
                connected_joysticks.append(joystick)
        return connected_joysticks

    def update(self, sampling_frequency=10):
        # Calculate the time interval between updates based on the sampling frequency
        update_interval = 1.0 / sampling_frequency

        while not self.terminate_event.is_set():
            start_time = time.time()

            joystick_data_list = []
            connected_joysticks = self.check_joystick_connection()
            
            for joystick in connected_joysticks:
                pygame.event.get()
                num_axes = joystick.get_numaxes()
                num_buttons = joystick.get_numbuttons()

                axes = [0.0] * num_axes
                buttons = [False] * num_buttons

                for i in range(num_axes):
                    axes[i] = joystick.get_axis(i)

                for i in range(num_buttons):
                    buttons[i] = joystick.get_button(i)

                joystick_data = {
                    "axes": axes,
                    "buttons": buttons
                }
                joystick_data_list.append(joystick_data)
            # Put the data into the queue
            self.data_queue.put(joystick_data_list)

            elapsed_time = time.time() - start_time

            # Sleep to maintain the desired update frequency
            if elapsed_time < update_interval:
                time.sleep(update_interval - elapsed_time)

    def start_update_process(self, sampling_frequency=10):
        self.process = multiprocessing.Process(target=self.update, args=(sampling_frequency,))
        self.process.start()

    def get_data(self):
        data = []
        while not self.data_queue.empty():
            data.extend(self.data_queue.get())
        print("Data retrieved:", data)
        return data

    def stop_update_process(self):
        if self.process:
            #pygame. quit()
            self.terminate_event.set()  # Set the termination event
            self.process.join()  # Wait for the process to exit

    def run(self):
        self.start_update_process()
