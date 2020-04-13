import os

from gpt2handler import Gpt2Handler


class Generator:
    """This class respects the singleton design pattern and facilitates communication between the other components."""
    __instance = None

    @classmethod
    def get_instance(cls):
        """Return the instance of this class. If it doesn't exist construct it first."""
        if cls.__instance is None:
            cls()
        return cls.__instance

    def __init__(self):
        """Initialise a Generator instance if there is none. For internal use only."""
        if Generator.__instance is None:
            Generator.__instance = self
        else:
            raise Exception("Attempted initialisation of singleton class Gui.")

        Gpt2Handler.get_instance()  # Create instance of Gpt2Handler

    @staticmethod
    def launch_gui():
        """Get the instance of the GUI and start it."""
        from gui import Gui
        Gui.get_instance().start()

    @staticmethod
    def generate_as_tuple(title, initial_content='', num_samples=1, num_words=1023):
        """Use gpt2 to generate an article as a tuple then return it."""
        return Gpt2Handler.get_instance().generate_as_tuple(title, initial_content, num_samples, num_words)

    def generate_from_single_file(self,
                                  input_filename,
                                  num_samples=1,
                                  print_output=False,
                                  output_file=None,
                                  num_words=1023):
        """Read the title and initial content from a single file then use gpt2 to generate an article
        and return it as a single string."""
        with open(input_filename, 'r', errors='surrogateescape') as f:
            file_contents = f.readlines()

        title = file_contents[0].rstrip()
        initial_content = '' if len(file_contents) < 2 else file_contents[1].rstrip()

        return self.generate(title, initial_content, num_samples, print_output, output_file, num_words)

    def generate_from_files(self,
                            title_filename,
                            content_filename=None,
                            num_samples=1,
                            print_output=False,
                            output_file=None,
                            num_words=1023):
        """Read the title from a file and initial content from another file then use gpt2 to generate an article
        and return it as a single string."""
        with open(title_filename, 'r', errors='surrogateescape') as title_file:
            title = title_file.readline().rstrip()

        if content_filename:
            with open(content_filename, 'r', errors='surrogateescape') as content_file:
                initial_content = content_file.readline().rstrip()
        else:
            initial_content = ''

        return self.generate(title, initial_content, num_samples, print_output, output_file, num_words)

    def generate(self,
                 title,
                 initial_content=None,
                 num_samples=1,
                 print_output=False,
                 output_file=None,
                 num_words=1023):
        """Use gpt2 to generate an article based on a given title and initial content."""
        if not initial_content:
            initial_content = ''
        samples = Gpt2Handler.get_instance().generate_as_tuple(title, initial_content, num_samples, num_words)
        samples_str = [sample[0] + '\n' + sample[1] for sample in samples]

        if print_output:  # Print each article to the console is specified to
            for sample in samples_str:
                print(sample)
        if output_file:  # Write each of the samples to their own file if a base filename is specified
            self.write_samples_to_file(output_file, samples_str)

        return samples_str

    def write_samples_to_file(self, filename, samples):
        """Write the given samples to a file. If there is more than one, write each to its own file."""
        if len(samples) == 1:
            self.write_sample_to_file(filename, samples[0])
        else:
            base, extension = os.path.splitext(filename)
            for i in range(len(samples)):
                new_filename = base + str(i) + extension
                self.write_sample_to_file(new_filename, samples[i])

    def write_sample_to_file(self, filename, sample):
        """Write a given sample to a file specified by te filename."""
        with open(filename, 'w+', errors='surrogateescape', encoding='utf-8') as f:
            f.write(sample)
