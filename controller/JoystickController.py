
class JoystickController:
    def __init__(self):
        pygame.init()
        self.joysticks = []
        self.initialize_joysticks()
        self.data_queue = multiprocessing.Queue()  # Use a Queue for data
        self.process = None
        self.terminate_event = multiprocessing.Event()  # Initialize the termination event

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

    def update(self):
        while not self.terminate_event.is_set():  # Exit when termination event is set
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
           # pygame.quit()

            # Put the data into the queue
            self.data_queue.put(joystick_data_list)
           # print("Data put into the queue:", joystick_data_list)
            time.sleep(0.1)   
    def start_update_process(self):
        self.process = multiprocessing.Process(target=self.update)
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
