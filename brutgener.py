#
# Author: Igor Ivanov
# 2019
#
import sys
import progressbar
import time


NAME = 'brutgener'

SKIP_SYMBOL        = '_'

list_word          = []
out_name           = ''
lengths            = [0, 99999999]
elements           = [1, 1]
is_pattern         = False
pattern            = ''
pat_index          = []
position           = []
out_file           = 0


def print_help():
    BANNER = """
     _                _
    | |              | |
    | |__  _ __ _   _| |_ __ _  ___ _ __   ___ _ __
    | '_ \| '__| | | | __/ _` |/ _ \ '_ \ / _ \ '__|
    | |_) | |  | |_| | || (_| |  __/ | | |  __/ |
    |_.__/|_|   \__,_|\__\__, |\___|_| |_|\___|_|
                          __/ |
                         |___/

    Small script generating a dictionary for brut password
    
    Author: IVOGOR13 (Igor Ivanov)
    """
    print(BANNER)
    print('Usage: \n\tpython3 {}.py [OPTION...] arguments\n'.format(NAME), sep='\n')
    print("""Options: \n """ +
        """\t-l | --list <path_file>         select file with dictionary\n""" +
        """\t-o | --out  <path_file>         select a file to display the result\n\n""" +
        """\t-d | --dict=<dictionary with one-character words>   select dictionary without file\n""" +
        """\t-p | --pattern=<pattern: skip is indicated '{}'>     select pattern words\n"""
            .format(SKIP_SYMBOL) +
        """\t--max-len=<value>               maximum word length\n""" +
        """\t--min-len=<value>               minimum word length\n""" +
        """\t--max-elem=<value>              maximum number of elements in a word\n""" +
        """\t--min-elem=<value>              minimum number of elements in a word\n""" +
        """\t-h | --help                     display this help and exit\n""", sep='\n')
    print("""Example usage: \n""" +
        """\tpython3 {}.py --dict=abcdefg --pattern={}1{}2{}3{}4 -o out.txt\n"""
            .format(NAME, SKIP_SYMBOL, SKIP_SYMBOL, SKIP_SYMBOL, SKIP_SYMBOL) +
        """\tpython3 {}.py -l list.txt -o out.txt --min-elem=5 --max-elem=8 --min-len=6 --max-len=13\n"""
            .format(NAME) +
        """\tpython3 {}.py -d=0123 --max-elem=7\n"""
            .format(NAME)
        , sep='\n')
    sys.exit(0)


def follow_position(i, list_len):
    global position

    if i == 0:
        if position[i] < list_len - 1:
            position[i] = position[i] + 1
            return position
        else:
            return position

    else:
        if position[i] < list_len - 1:
            position[i] = position[i] + 1
            return position
        else:
            position[i] = 0
            follow_position(i - 1, list_len)


def get_word():
    global list_word
    global position

    word = ''
    for symb in position:
        word += list_word[symb]
    return word


def print_word():
    global is_pattern
    global pattern
    global pat_index
    global position
    global out_file
    global lengths

    word = get_word()

    if (len(word) >= lengths[0] and len(word) <= lengths[1]):
        if is_pattern:
            word, string = list(word), list(pattern)
            for index, j in enumerate(pat_index):
                string[j] = word[index]
            print(''.join(string), file=out_file)
        else:
            print(word, file=out_file)
        return True


def main():
    global list_word
    global out_name
    global position
    global pattern
    global pat_index
    global lengths
    global elements
    global out_file
    global SKIP_SYMBOL
    global is_pattern

    specified_out      = False
    is_out_in_console  = False

    progress = 0
    was_written = 0

    arg = sys.argv

    if not len(arg[1:]):
        print_help()

    else:
        for option in arg:
            if option == '-h' or option == '--help':
                print_help()

            if option == '-l' or option == '--list':
                file = arg[arg.index(option) + 1]
                file = 'list.txt'
                with open(file) as lines:
                    for line in lines:
                        list_word.append(str(line.rstrip()))

            elif option == '-o' or option == '--out':
                specified_out = True
                out_name = arg[arg.index(option) + 1]

            elif option.count('--max-len=') > 0:
                lengths[1] = int(arg[arg.index(option)].split('=')[1])

            elif option.count('--min-len=') > 0:
                lengths[0] = int(arg[arg.index(option)].split('=')[1])

            elif option.count('--max-elem=') > 0:
                elements[1] = int(arg[arg.index(option)].split('=')[1])

            elif option.count('--min-elem=') > 0:
                elements[0] = int(arg[arg.index(option)].split('=')[1])

            elif option.count('--dict=') > 0 or option.count('-d=') > 0:
                list_word = list(arg[arg.index(option)].split('=')[1])

            elif option.count('--pattern=') > 0 or option.count('-p=') > 0:
                is_pattern = True
                pattern = '='.join(arg[arg.index(option)].split('=')[1:])
                pat_index = [i for i, w in enumerate(pattern) if w == SKIP_SYMBOL]

    if not specified_out:
        print('You did not specify an output file')
        nin = input('Print results to console: [y/n]: ')
        if nin == 'y':
            is_out_in_console = True
        elif nin == 'n':
            sys.exit(0)
        else:
            print('Unknow command')
            sys.exit(0)

    if is_pattern:
        lengths = [0, 9999999]
        elements = [pattern.count(SKIP_SYMBOL), pattern.count(SKIP_SYMBOL)]


    list_word.sort()
    list_len = len(list_word)

    if elements[1] < elements[0]:
        elements[1] = elements[0]

    value = 0
    size = 0
    for i in range(elements[0], elements[1] + 1):
        x = pow(list_len, i)
        value += x
        size += x * (i + 2)

    print('Presumably words: {}'.format(value))
    print('Dictionary size: {}'.format(len(list_word)))
    print('Dictionary: \n\t{}'.format(', '.join(list_word)), sep='\n')
    if is_pattern:
        print('Pattern: \n\t{}'.format(pattern), sep='\n')
    print('Range of word length: [{}, {}]'.format(lengths[0], lengths[1]))
    print('Range of number of elements in a word: [{}, {}]'.format(elements[0], elements[1]))
    print("""Size output file: \n\t{} byte\n\t{} KiB\n\t{} MiB\n\t{} GiB """
        .format(size,
            round(size/1024.0, 2),
            round(size/1024.0/1024.0, 2),
            round(size/1024.0/1024.0/1024.0, 2)
        ), sep='\n')
    print()

    time.sleep(1)

    if value > 0:

        if not is_out_in_console:
            out_file = open(out_name, 'w')

            with progressbar.ProgressBar(max_value=value) as bar:
                for run in range(elements[0] - 1, elements[1]):
                    position = [0 for pos in range(run + 1)]

                    if print_word():
                        was_written += 1
                    progress += 1
                    bar.update(progress)

                    for i in range(pow(list_len, run + 1) - 1):
                        follow_position(run, list_len)
                        if print_word():
                            was_written += 1
                        progress += 1
                        bar.update(progress)
        else:
            out_file = sys.stdout

            for run in range(elements[0] - 1, elements[1]):
                position = [0 for pos in range(run + 1)]

                if is_out_in_console:
                    if print_word():
                        was_written += 1
                    progress += 1

                for i in range(pow(list_len, run + 1) - 1):
                    follow_position(run, list_len)
                    if print_word():
                        was_written += 1
                    progress += 1



        print()
        print('Total words: {}'.format(was_written))
        if not is_out_in_console:
            print('Successfully written to file {}'.format(out_name))

    else:
        print("Error: number of output words is zero.")


if __name__ == "__main__":
    main()
