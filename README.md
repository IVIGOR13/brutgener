# brutgener
Small script generating a dictionary for brut password.

<p align="center">
  <img width="700" src="https://github.com/IVIGOR13/brutgener/blob/master/example_anim.svg">
</p>

## Interface

```
  BRUTGENER

  Usage:
          python3 brutgener.py [OPTION...] arguments

  Options:
          -l | --list <path_file>         select file with dictionary
          -o | --out  <path_file>         select a file to display the result

          -d | --dict=<dictionary with one-character words>   select dictionary without file
          -p | --pattern=<pattern: skip is indicated '_'>     select pattern words
          --max-len=<value>               maximum word length
          --min-len=<value>               minimum word length
          --max-elem=<value>              maximum number of elements in a word
          --min-elem=<value>              minimum number of elements in a word
          -h | --help                     display this help and exit

  Example usage:
          python3 brutgener.py --dict=abcdefg --pattern=_1_2_3_4 -o out.txt
          python3 brutgener.py -l list.txt -o out.txt --min-elem=5 --max-elem=8 --min-len=6 --max-len=13
          python3 brutgener.py -d=0123 --max-elem=7
```

# Installation

Repository cloning
```
$ git clone https://github.com/IVIGOR13/brutgener.git
```
Tuning
```
$ pip3 install progressbar2
```
Launch
```
$ cd brutgener
$ python3 brutgener.py --help
```
