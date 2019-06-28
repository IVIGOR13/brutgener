import sys
import progressbar

NAME = 'brutgener'

def print_help():
    print('Usage: \n\tpython3 {}.py [OPTION...] arguments'.format(NAME), sep='\n')
    print("""Options: \n """ +
        """\t-l, --list <path_file>    select file with vocabulary\n""" +
        """\t-o, --out  <path_file>    select a file to display the result\n""" +
        """\t--max-len  <value>        maximum word length\n""" +
        """\t--min-len  <value>        minimum word length\n""" +
        """\t--max-elem  <value>       maximum number of elements in a word\n""" +
        """\t--min-elem  <value>       minimum number of elements in a word\n""" +
        """\t-h, --help                display this help and exit""", sep='\n')
    sys.exit(0)

def follow(i):
    if i == 0:
        if pos[i] < list_len - 1:
            pos[i] = pos[i] + 1
        else:
            return False
    else:
        if pos[i] < list_len-1:
            pos[i] = pos[i] + 1
        else:
            pos[i] = 0
            follow(i - 1)
    return True

def get_word():
    word = ''
    for symb in pos:
        word += list_word[symb]
    return word

list_word = []
out_name = ''

min_len, max_len = 0, 99999999
min_elem, max_elem = 1, 1

arg = sys.argv

if len(arg) == 1:
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
            out_name = arg[arg.index(option) + 1]

        elif option == '--max-len':
            max_len = int(arg[arg.index(option) + 1])

        elif option == '--min-len':
            min_len = int(arg[arg.index(option) + 1])

        elif option == '--max-elem':
            max_elem = int(arg[arg.index(option) + 1])

        elif option == '--min-elem':
            min_elem = int(arg[arg.index(option) + 1])

list_word.sort()
list_len = len(list_word)

if max_elem < min_elem:
    max_elem = min_elem

pos =  []

value = 0
for i in range(min_elem, max_elem + 1):
    value += pow(list_len, i)

print('All words: {}'.format(value))
print('Vocabulary size: {}'.format(len(list_word)))
print('Vocabulary: \n\t{}'.format(', '.join(list_word)), sep='\n')

progress = 0
val_written = 0
if value > 0:
    with progressbar.ProgressBar(max_value=int(value)) as bar:
        with open(out_name, 'w') as out_file:

            for run in range(min_elem-1, max_elem):
                pos = [0 for pos in range(run + 1)]

                word = get_word()
                if len(word) >= min_len and len(word) <= max_len:
                    print(word, file=out_file)
                    val_written += 1
                    progress += 1
                    bar.update(progress)

                for i in range(pow(list_len, run + 1) - 1):
                    follow(run)
                    word = get_word()
                    if len(word) >= min_len and len(word) <= max_len:
                        print(word, file=out_file)
                        val_written += 1
                    progress += 1
                    bar.update(progress)

    print('Total words: {}'.format(val_written))
    print('Successfully written to file {}'.format(out_name))
else:
    print("Error: number of output words is zero.")
