__author__ = 'QHe'


''' A function that copies a file but replaces all 'pattern strings' to
 'replacement strings.'''

def replace(pattern, replacement, file_1, file_2):
    try:
        fin = open(file_1,"r")
        fout = open(file_2,"w")
        for lines in fin:
            line = lines.replace(pattern, replacement)
            fout.write(line)

        fin.close()
        fout.close()
    except:
        print "Error"

if __name__ == '__main__':
    replace('pattern','replace',"words.txt","new_words.txt")

