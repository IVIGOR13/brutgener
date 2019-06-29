import sys
import progressbar

NAME = 'brutgener'

def print_help():
    print('Usage: \n\tpython3 {}.py [OPTION...] arguments\n'.format(NAME), sep='\n')
    print("""Options: \n """ +
        """\t-l, --list <path_file>         select file with dictionary\n""" +
        """\t-o, --out  <path_file>         select a file to display the result\n\n""" +
        """\t-d, --dict=<dictionary with one-character words>   select dictionary without file\n""" + 
        """\t-p, --pattern=<pattern: skip is indicated '_'>     select pattern words\n\n""" +
        """\t--max-len=<value>              maximum word length\n""" +
        """\t--min-len=<value>              minimum word length\n""" +
        """\t--max-elem=<value>             maximum number of elements in a word\n""" +
        """\t--min-elem=<value>             minimum number of elements in a word\n\n""" +
        """\t-h, --help                     display this help and exit\n""", sep='\n')
    print("""Example usage: \n\tpython3 {}.py --dict=abcdefg --pattern=_1_2_3_4 -o out.txt\n""".format(NAME) +
        """\tpython3 {}.py -l list.txt -o out.txt --min-elem=5 --max-elem=8 --min-len=6 --max-len=13\n""".format(NAME), sep='\n')
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

is_file = False
is_pattern = False
is_out = False
voc = []

pat = '_'
pattern = ''
pat_len = 0
pat_index = []


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
            is_file = True

        elif option == '-o' or option == '--out':
            is_out = True
            out_name = arg[arg.index(option) + 1]

        elif option.count('--max-len=') > 0:
            max_len = int(arg[arg.index(option)].split('=')[1])

        elif option.count('--min-len=') > 0:
            min_len = int(arg[arg.index(option)].split('=')[1])

        elif option.count('--max-elem=') > 0:
            max_elem = int(arg[arg.index(option)].split('=')[1])

        elif option.count('--min-elem=') > 0:
            min_elem = int(arg[arg.index(option)].split('=')[1])

        elif option.count('--dict=') > 0 or option.count('-d=') > 0:
            voc = list(arg[arg.index(option)].split('=')[1])

        elif option.count('--pattern=') > 0 or option.count('-p=') > 0:
            is_pattern = True
            pattern = '='.join(arg[arg.index(option)].split('=')[1:])
            pat_len = pattern.count(pat)
            pat_index = [i for i, w in enumerate(pattern) if w == '_']

if not is_out:
    print('You did not specify an output file')
    sys.exit(0)

if not is_file:
    list_word = voc

if is_pattern:
    min_len, max_len = 0, 9999999
    min_elem, max_elem = pat_len, pat_len


list_word.sort()
list_len = len(list_word)

if max_elem < min_elem:
    max_elem = min_elem

pos =  []

value = 0
for i in range(min_elem, max_elem + 1):
    value += pow(list_len, i)

print('All words: {}'.format(value))
print('Dictionary size: {}'.format(len(list_word)))
print('Dictionary: \n\t{}'.format(', '.join(list_word)), sep='\n')
if is_pattern:
    print('Pattern: \n\t{}'.format(pattern), sep='\n')
print('Range of word length: [{}, {}]'.format(min_len, max_len))
print('Range of number of elements in a word: [{}, {}]'.format(min_elem, max_elem))

progress = 0
val_written = 0
if value > 0:
    with progressbar.ProgressBar(max_value=int(value)) as bar:
        with open(out_name, 'w') as out_file:

            for run in range(min_elem-1, max_elem):
                pos = [0 for pos in range(run + 1)]

                word = get_word()
                if len(word) >= min_len and len(word) <= max_len:
                    if is_pattern:
                            word = list(word)
                            string = list(pattern)
                            for index, j in enumerate(pat_index):
                                string[j] = word[index]
                            print(''.join(string), file=out_file)
                    else:
                        print(word, file=out_file)
                    val_written += 1
                    progress += 1
                    bar.update(progress)

                for i in range(pow(list_len, run + 1) - 1):
                    follow(run)
                    word = get_word()
                    if len(word) >= min_len and len(word) <= max_len:
                        if is_pattern:
                            word = list(word)
                            string = list(pattern)
                            for index, j in enumerate(pat_index):
                                string[j] = word[index]
                            print(''.join(string), file=out_file)
                        else:
                            print(word, file=out_file)
                        val_written += 1
                    progress += 1
                    bar.update(progress)

    print('Total words: {}'.format(val_written))
    print('Successfully written to file {}'.format(out_name))
else:
    print("Error: number of output words is zero.")
