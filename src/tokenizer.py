# -*- coding: utf-8 -*-
import re

regs = [
    r'\d.\d.\d',
    r'\d,\d,\d',
    r'\d.\d',
    r'\d,\d',
    r'\d-\d-\d',
    r'\d-\d',
    r'\d/\d/\d',
    r'\d/\d',
    r'^(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/[^\s]*)?$'
]

punctuals = [
    '“',
    '”',
    '...',
    '…',
    '[', ']',
    ',', '.',
    '/', ';',
    '\'', '-',
    '=', '!',
    '@', '$',
    '#', '%',
    '^', '&',
    '*', '(',
    ')', '\\',
    '\"', ':',
    '<', '>',
    '?', '{',
    '}'
]

def split_sign(inputStr):
    for reg in regs:
        matcher = re.search(reg, inputStr)
        if matcher:
            inputStr = inputStr.replace(matcher.group(), " " + matcher.group() + " ")
            return inputStr.strip()
    if inputStr in punctuals:
        return inputStr.strip()
    for punctual in punctuals:
        if punctual in inputStr:
            inputStr = inputStr.replace(punctual, " " + punctual + " ")
    return inputStr.strip()

def tokenizer_sentence(sentence):
    tokens = sentence.split(' ')
    new_sent = ''
    for token in tokens:
        string = split_sign(token)
        new_sent += string + " "
    new_sent = new_sent.replace(r"\s+", " ")
    return new_sent.strip()

def split_sentence(sentence):
    sentences_list = []
    sentence = tokenizer_sentence(sentence)
    tokens = sentence.split(" ")
    sentence = ""
    for token in tokens:
        if token == "." or token == "!" or token == "?":
            sentences_list.append(sentence.strip() + " " + token)
            sentence = ""
        else:
            sentence+=token + " "
    return sentences_list

if __name__ == '__main__':
    print(tokenizer_sentence('Hôm nay tôi đi học.'))