import argparse
import os


def positive_int_type(value):
    """Raise an error if the provided value is not a positive integer. Return it otherwise."""
    i = int(value)
    if i <= 0:
        raise argparse.ArgumentTypeError(f'{value} is not a positive int.')
    return i


def existing_filename_type(value):
    """Raise an error if the provided value is not the name of an existing file. Return it otherwise."""
    if not os.path.isfile(value):
        raise argparse.ArgumentTypeError(f'{value} is not the name of a file that exists.')
    return value


def not_existing_filename_type(value):
    """Raise an error if the provided value is the name of an existing file. Return it otherwise."""
    if os.path.isfile(value):
        raise argparse.ArgumentTypeError(f'{value} is not the name of a file that does not exists.')
    return value


def is_default_args(namespace):
    """Return true if all of the arguments in the namespace are the default value. Return false otherwise."""
    return (namespace.content is None) and (namespace.content_filename is None) and (namespace.filename is None) and \
           (not namespace.print) and (namespace.num_samples == 1) and (namespace.num_words == 1023) and \
           (namespace.output_filename is None) and (namespace.title is None) and (namespace.title_filename is None)


def create_parser():
    """Create and return a parser with a usage string and all the arguments this program can take."""
    usage_str = """
        USAGE:      python ArticleGenerator.py <options>
        EXAMPLES:   (1) python ArticleGenerator.py
                        - Opens the ArticleGenerator GUI
                    (2) python ArticleGenerator.py -f example.txt -o sample.txt -n 5
                    OR  python ArticleGenerator.py --filename example.txt --output-filename sample.txt --num_samples 3 
                        - Generates 3 articles with the title and initial content specified in \'example.txt\' and 
                        writes them to \'sample1.txt\', \'sample2.txt\', and \'sample3.txt\'.
        """
    parser = argparse.ArgumentParser(usage_str)
    parser.add_argument('-f', '--filename', dest='filename', type=existing_filename_type,
                        help='Use the title and initial content in a file with the specified filename, containing the '
                             'title in the first line and initial content (if any) in the second line.')
    parser.add_argument('-o', '--output_filename', dest='output_filename',
                        type=not_existing_filename_type,
                        help='Write the generated sample to a new file with the specified filename. The sample number '
                             'is appended to the filename before the extension if multiple samples are generated.')
    parser.add_argument('-p', '--print', dest='print', action='store_true',
                        help='Print the generated sample(s) to console.')
    parser.add_argument('-n', '--num_samples', dest='num_samples', default=1, type=positive_int_type,
                        help='Use the specified value to dictate how many samples are generated. Default: 1')
    parser.add_argument('-w', '--num_words', dest='num_words', default=1023, type=positive_int_type,
                        help='Use the specified value to dictate the maximum number of words in each sample. '
                             'Default: 1023')
    parser.add_argument('-t', '--title_filename', dest='title_filename', type=existing_filename_type,
                        help='Use the title in a file with the specified filename, containing the title in the first '
                             'line. This will be ignored if a filename for \'--filename\' is specified.')
    parser.add_argument('-c', '--content_filename', dest='content_filename', type=existing_filename_type,
                        help='Use the initial content in a file with the specified filename, containing the initial '
                             'content in the first line. This will be ignored if no filename for \'--title-filename\' '
                             'is specified.')
    parser.add_argument('-T', '--title', dest='title',
                        help='Use the specified title. This will be ignored if a filename for \'filename\' or '
                             '\'--title_filename\' is specified.')
    parser.add_argument('-C', '--content', dest='content',
                        help='Use the specified initial content. This will be ignored if no title for \'title\' is '
                             'specified.')
    return parser


def parse_arguments():
    """Create a parser and use it to parse the arguments given by Python, then return the parsed arguments."""
    parser = create_parser()
    parsed_args = parser.parse_args()
    return parsed_args


if __name__ == '__main__':
    args = parse_arguments()
    from generator import Generator

    gen = Generator.get_instance()

    if is_default_args(args):
        gen.launch_gui()
    elif not args.output_filename and not args.print:
        raise argparse.ArgumentError('Output has not been set to either console or an output file.')
    elif args.output_filename and args.output_filename in [args.filename, args.title_filename, args.content_filename]:
        raise argparse.ArgumentError('Output filename cannot be the same as an input filename.')
    elif args.filename:
        gen.generate_from_single_file(args.filename, args.num_samples, args.print, args.output_filename)
    elif args.title_filename:
        gen.generate_from_files(args.title_filename, args.content_filename, args.num_samples, args.print,
                                args.output_filename)
    elif args.title:
        gen.generate(args.title, args.content, args.num_samples, args.print, args.output_filename)
