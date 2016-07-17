__author__ = 'Prateek'
import os

SPECIAL_CHARS = '[]"-_@$().\' '

def _isUpperCase(c):
    if ('A' <= c <= 'Z') or ('0' <= c <= '9'):
        return True
    return False

def _isLowerCase(c):
    if 'a' <= c <= 'z':
        return True
    return False

def _split_on_special_chars(path):
    #sanitize the filename
    fname = os.path.basename(path.strip('\n'))

    #remove the extension name
    fname, ext = os.path.splitext(path)
    ext.strip(".")

    tokens = []
    tk = ""

    #used for basic split using the given special chars

    for c in fname:
        if c not in SPECIAL_CHARS:
            tk += c
        else:
            tokens.append(tk)
            tk = ""
    if len(tk):
        tokens.append(tk)

    return tokens

def _split_for_words(seg):
    #takes a string that has been split using special chars
    #and tries to split it such that it forms more natural
    #words and identifiers

    #this is mainly used for spliting camel casing
    #eg SiliconValley, SiliconNRGValleyS01E03

    lst = []
    tk = ""
    rev_seg = seg[::-1] #reverse the string
    #numbers and upper case letters are considered equivalent
    for c in rev_seg:
        if _isUpperCase(c):
            if len(tk):
                if _isLowerCase(tk[-1]):
                    #type : Valley
                    #		--
                    tk += c
                    lst.append(tk[::-1])
                    tk = ""
                elif _isUpperCase(tk[-1]):
                    #type : S03E01
                    #		------
                    #append the char to continue with the caps or equivalent char
                    tk += c
            else:
                #probably the first character in the current token
                tk += c

        elif _isLowerCase(c):
            if len(tk):
                if _isUpperCase(tk[-1]):
                    #type alleyS03E01
                    #         --
                    lst.append(tk[::-1])
                    tk = str(c)
                else:
                    tk += c
            else:
                tk += c

    #if no special separator is present or the first token
    #eg "hello", "helloWorld"
    if len(tk):
        lst.append(tk[::-1])

    #this list formed is in reverse order so reverse again
    return lst[::-1]

def split_file_name(fname):
    tmp = _split_on_special_chars(fname)
    lst = []
    for seg in tmp:
        t = _split_for_words(seg)
        for x in t:
            lst.append(x.lower())

    return lst

