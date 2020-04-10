import logging
import os

# Source: https://github.com/tensorflow/tensorflow/issues/27023#issuecomment-475544248
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Used to disable TensorFlow printing debug messages
# Source: https://github.com/tensorflow/tensorflow/issues/8340#issuecomment-332212742
logging.getLogger('tensorflow').disabled = True  # Used to disable TensorFlow printing warning messages

import gpt_2_simple as gpt2
import re

DEFAULT_CONFIG = {
    'model_name': '124M',
    'run_name': '124M_article_generator_model',  # The name of the model
    'top_k': '0',  # How many previous words to consider when generating a new word. 0 means unlimited
    'include_prefix': 'True',
    'return_as_list': 'True',
    'truncate': '<|endoftext|><|startoftext|>'  # Truncate the sample where it contains this substring
}
# A dictionary from argument names to a lambda that determines how to parse the string representing its value
GENERATE_ARGUMENT_PARSER = {
    'model_name': lambda s: s,
    'run_name': lambda s: s,
    'temperature': lambda f: float(f),
    'top_k': lambda i: int(i),
    'top_p': lambda f: float(f),
    'include_prefix': lambda b: b == 'True',
    'return_as_list': lambda b: b == 'True',
    'truncate': lambda s: s
}


class Gpt2Handler:
    """This class respects the singleton design pattern and handles interacting with gpt2 to generate text."""
    __instance = None

    @classmethod
    def get_instance(cls):
        """Return the instance of this class. If it doesn't exist construct it first."""
        if cls.__instance is None:
            cls()
        return cls.__instance

    def __init__(self):
        """Initialise a Generator instance if there is none. For internal use only."""
        if Gpt2Handler.__instance is None:
            Gpt2Handler.__instance = self
        else:
            raise Exception("Attempted initialisation of singleton class Generator.")

        # Start the TensorFlow session and load the model into it.
        self.sess = gpt2.start_tf_sess()
        self.run_name = DEFAULT_CONFIG['run_name']
        self.download_model()
        self.load_model()

    def download_model(self):
        """Download the 124M gpt2 model if it is not downloaded"""
        if not gpt2.is_gpt2_downloaded():
            gpt2.download_gpt2()

    def load_model(self):
        """Load the gpt2 model. If it has already been loaded, reset it first."""
        try:
            gpt2.load_gpt2(self.sess, run_name=self.run_name)
        except FileNotFoundError:
            raise Exception(f'Model is missing. Place \'{self.run_name}\' in the checkpoint folder and try again.')

    def generate(self, title, initial_content='', num_samples=1, num_words=1023):
        """Generate a sample with the specified title and initial content."""
        initial_content = initial_content.replace('\n', ' ')  # Remove newlines
        # Convert the input into the correct format for the model
        prefix = '<|startoftext|>\n' \
                 + ('=' * 5) + 'TITLE' + ('=' * 5) + '\n' + title + '\n' \
                 + ('=' * 5) + 'CONTENT' + ('=' * 5) + '\n' + initial_content

        generate_args = self.parse_generate_arguments(DEFAULT_CONFIG)
        samples = gpt2.generate(self.sess, prefix=prefix, nsamples=num_samples, length=num_words, **generate_args)

        return samples

    def generate_as_tuple(self, title, initial_content='', num_samples=1, num_words=1023):
        """Generate a sample as a tuple in the form [title, content] with the specified title and initial content."""
        return [self.sample_to_tuple(sample) for sample in
                self.generate(title, initial_content, num_samples, num_words)]

    @staticmethod
    def sample_to_tuple(sample):
        """Take a sample and return a list where the first value is the title and the second value is the content."""
        # Remove the startoftext token and the title header
        no_title_header = sample.split('<|startoftext|>\n' + ('=' * 5) + 'TITLE' + ('=' * 5) + '\n')[1]
        # Remove any remaining tokens using a regex that matches substrings that start with '<|' and end with '|>'
        no_tokens = re.sub('<\\|[^|>]*\\|>', '', no_title_header)
        # Replace multiple adjacent spaces with a single space
        no_repeating_spaces = re.sub(' +', ' ', no_tokens)
        # Convert the sample into a list consisting of the title and sample without the sample header
        split_sample = no_repeating_spaces.split('\n' + ('=' * 5) + 'CONTENT' + ('=' * 5) + '\n')[:2]
        return split_sample

    @staticmethod
    def parse_generate_arguments(arguments):
        """Convert generate arguments from string to the correct respective types using GENERATE_ARGUMENT_PARSER."""
        return_value = {}
        for key in arguments:
            return_value[key] = GENERATE_ARGUMENT_PARSER[key](arguments[key])

        return return_value
