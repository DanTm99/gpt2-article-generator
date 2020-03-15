import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from generator import Generator


class Gui:
    """This class respects the singleton design pattern and handles the GUI."""
    __instance = None

    # Constants
    MIN_WINDOW_WIDTH = 600
    MIN_WINDOW_HEIGHT = 300
    ROOT_PAD_X = 2
    ROOT_PAD_Y = 2
    HOME_PAD_X = 2
    HOME_PAD_Y = 2

    @classmethod
    def get_instance(cls):
        """Return the instance of this class. If it doesn't exist construct it first."""
        if cls.__instance is None:
            cls()
        return cls.__instance

    def __init__(self):
        """Initialise a Generator instance if there is none. For internal use only."""
        if Gui.__instance is None:
            Gui.__instance = self
        else:
            raise Exception("Attempted initialisation of singleton class Gui.")

        self.root = None

        # Home
        self.home = None
        self.title_option = None
        self.title_text = None
        self.initial_content_option = None
        self.initial_content_text = None
        self.number_of_samples = None
        self.words_per_sample = None

        self.create_gui()

        self.root.mainloop()

    def start(self):
        self.root.mainloop()

    def create_gui(self):
        # Window
        self.root = tk.Tk()
        self.root.title("Article Generator")
        self.root.minsize(width=self.MIN_WINDOW_WIDTH, height=self.MIN_WINDOW_HEIGHT)
        self.root.resizable(False, False)

        self.create_home()

    def create_home(self):
        self.home = tk.LabelFrame(self.root, padx=self.ROOT_PAD_X, pady=self.ROOT_PAD_Y, borderwidth=0,
                                  highlightthickness=0)
        self.home.pack()

        # Title
        # Label
        title_label = tk.Label(self.home, text="Title:")
        title_label.grid(row=0, column=0, padx=self.HOME_PAD_X, pady=self.HOME_PAD_Y, sticky=tk.W)
        # Option Menu
        self.title_option = tk.StringVar(value='Text')
        title_option_menu = tk.OptionMenu(self.home, self.title_option, 'Text', 'File',
                                          command=self.on_title_option_menu_update)
        title_option_menu.grid(row=0, column=1, padx=self.HOME_PAD_X, pady=self.HOME_PAD_Y, sticky=tk.W)
        # Text Entry
        self.title_text = tk.Text(self.home, width=50, height=1, font=("Helvetica", 10))
        self.title_text.grid(row=0, column=2, padx=self.HOME_PAD_X, pady=self.HOME_PAD_Y, sticky=tk.W)
        # Do nothing when the user tries to enter a newline character
        self.title_text.bind('<Return>', lambda x: 'break')

        # Initial Content
        # Label
        initial_content_label = tk.Label(self.home, text="Initial Content:")
        initial_content_label.grid(row=1, column=0, padx=self.HOME_PAD_X, pady=self.HOME_PAD_Y, sticky=tk.W)
        # Dropdown
        self.initial_content_option = tk.StringVar(value='Text')
        initial_content_option_menu = tk.OptionMenu(self.home, self.initial_content_option, 'Text', 'File',
                                                    command=self.on_initial_content_option_menu_update)
        initial_content_option_menu.grid(row=1, column=1, padx=self.HOME_PAD_X, pady=self.HOME_PAD_Y, sticky=tk.W)
        # Text Entry
        self.initial_content_text = tk.Text(self.home, width=50, height=10, font=("Helvetica", 10), wrap=tk.WORD)
        self.initial_content_text.grid(row=1, column=2, padx=self.HOME_PAD_X, pady=self.HOME_PAD_Y, sticky=tk.W)

        # Number of Samples
        # Label
        number_of_samples_label = tk.Label(self.home, text="Number of Samples:")
        number_of_samples_label.grid(row=2, column=0, padx=self.HOME_PAD_X, pady=self.HOME_PAD_Y, sticky=tk.W)
        # Spinbox
        self.number_of_samples = tk.IntVar(value=1)
        number_of_samples_spinbox = tk.Spinbox(self.home, from_=1, to=99, width=9, textvariable=self.number_of_samples)
        number_of_samples_spinbox.grid(row=2, column=1, columnspan=2, padx=self.HOME_PAD_X, pady=self.HOME_PAD_Y,
                                       sticky=tk.W)

        # Words Per Sample
        # Label
        words_per_sample_label = tk.Label(self.home, text="Max Words Per Sample:")
        words_per_sample_label.grid(row=3, column=0, padx=self.HOME_PAD_X, pady=self.HOME_PAD_Y, sticky=tk.W)
        # Spinbox
        self.words_per_sample = tk.IntVar(value=1023)
        words_per_sample_spinbox = tk.Spinbox(self.home, from_=1, to=1023, width=9, textvariable=self.words_per_sample)
        words_per_sample_spinbox.grid(row=3, column=1, columnspan=2, padx=self.HOME_PAD_X, pady=self.HOME_PAD_Y,
                                      sticky=tk.W)

        # Generate Button
        generate_button = tk.Button(self.home, text='Generate', command=self.submit)
        generate_button.grid(row=4, column=1, columnspan=2, padx=self.HOME_PAD_X, pady=self.HOME_PAD_Y)

    def submit(self):
        try:
            number_of_samples = int(self.number_of_samples.get())
            assert number_of_samples > 0
        except (ValueError, AssertionError):
            messagebox.showerror('Invalid Value', 'Number of samples must be a positive number.')
            return

        try:
            words_per_sample = int(self.words_per_sample.get())
            assert (words_per_sample > 0) and (words_per_sample < 1024)
        except (ValueError, AssertionError):
            messagebox.showerror('Invalid Value', 'Words per sample must be a whole number between 1 and 1023.')
            return

        title = self.title_text.get('1.0', tk.END).rstrip()
        if len(title) == 0:
            messagebox.showerror('Invalid Title', 'Title must not be blank.')
            return

        initial_content = self.initial_content_text.get('1.0', tk.END)

        samples = Generator.get_instance().generate_as_tuple(title, initial_content, number_of_samples,
                                                             words_per_sample)

        Gui.SampleViewer(samples)

    def on_title_option_menu_update(self, value):
        self.on_option_menu_update(value, self.title_option, self.title_text)

    def on_initial_content_option_menu_update(self, value):
        self.on_option_menu_update(value, self.initial_content_option, self.initial_content_text)

    def on_option_menu_update(self, value, option_menu, text_field):
        if value == 'Text':
            text_field.config(state='normal')
        else:
            if len(text_field.get('1.0', tk.END)) > 1:
                response = messagebox.askyesno('Continue?', 'This will overwrite the contents of the title field.\n'
                                                            'Would you like to continue?')
                if not response:  # If the user responded with No
                    option_menu.set('Text')
                    text_field.config(state='normal')
                    return

            filename = filedialog.askopenfilename(initialdir='/', title='Open',
                                                  filetypes=(('Text Files (*.txt)', '*.txt'),
                                                             ('All Files (*.*)', '*.*')))
            if filename:
                with open(filename, 'r', errors='surrogateescape') as f:
                    title = f.readline().rstrip()
                text_field.config(state='normal')
                text_field.delete('1.0', tk.END)  # Clear the contents of the field
                text_field.insert('1.0', title)
                text_field.config(state='disabled')
            else:  # If the user did not select a file
                option_menu.set('Text')
                text_field.config(state='normal')

    class SampleViewer:
        # Constants
        WINDOW_PAD_X = 2
        WINDOW_PAD_Y = 2
        TEXT_FRAME_PAD_X = 2
        TEXT_FRAME_PAD_Y = 2

        def __init__(self, samples):
            self.window = None
            self.left_button = None

            self.title = samples[0][0]
            self.samples = [sample[1] for sample in samples]
            self.right_button = None

            self.title_text = None
            self.sample_text = None
            self.current_sample_index = 0

            self.text_frame = None

            self.create_window()
            self.window.mainloop()

        def create_window(self):
            self.window = tk.Toplevel()
            self.window.title(self.title)
            self.window.resizable(False, False)
            # self.window.minsize(width=self.MIN_WINDOW_WIDTH, height=self.MIN_WINDOW_HEIGHT)
            self.window.grab_set()

            self.create_buttons()
            self.update_buttons()

            self.create_text_frame()
            self.update_sample()

        def create_text_frame(self):
            self.text_frame = tk.LabelFrame(self.window, borderwidth=0, highlightthickness=0)
            self.text_frame.grid(row=0, column=0, columnspan=2, padx=self.WINDOW_PAD_X, pady=self.WINDOW_PAD_Y)

            self.title_text = tk.Text(self.text_frame, width=100, height=1, font=("Helvetica", 10),
                                      padx=self.TEXT_FRAME_PAD_X, pady=self.TEXT_FRAME_PAD_Y)
            self.title_text.insert(tk.END, self.title)
            self.title_text.configure(state='disabled')

            self.title_text.grid(row=0, column=0)

            self.sample_text = tk.Text(self.text_frame, width=100, height=20, font=("Helvetica", 10), wrap=tk.WORD,
                                       padx=self.TEXT_FRAME_PAD_X, pady=self.TEXT_FRAME_PAD_Y, state='disabled')
            self.sample_text.grid(row=1, column=0)

        def create_buttons(self):
            self.left_button = tk.Button(self.window, text='<', command=self.previous_sample)
            self.left_button.grid(row=1, column=0, padx=self.WINDOW_PAD_X, pady=self.WINDOW_PAD_Y, sticky=tk.E)
            self.right_button = tk.Button(self.window, text='>', command=self.next_sample)
            self.right_button.grid(row=1, column=1, padx=self.WINDOW_PAD_X, pady=self.WINDOW_PAD_Y, sticky=tk.W)

        def previous_sample(self):
            if self.current_sample_index == 0:
                messagebox.showerror('Error', 'First sample reached. No previous sample exists.')

            self.current_sample_index -= 1
            self.update_sample()
            self.update_buttons()

        def next_sample(self):
            if self.current_sample_index == (len(self.samples) - 1):
                messagebox.showerror('Error', 'Last sample reached. No next sample exists.')

            self.current_sample_index += 1
            self.update_sample()
            self.update_buttons()

        def update_sample(self):
            self.sample_text.configure(state='normal')
            self.sample_text.delete("1.0", "end")
            self.sample_text.insert(tk.END, self.samples[self.current_sample_index])
            self.sample_text.configure(state='disabled')

        def update_buttons(self):
            self.left_button.config(state='normal')
            self.right_button.config(state='normal')

            if self.current_sample_index == 0:
                self.left_button.config(state='disabled')

            if self.current_sample_index == (len(self.samples) - 1):
                self.right_button.config(state='disabled')
