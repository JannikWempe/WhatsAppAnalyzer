from collections import Counter, OrderedDict
import functools

def print_runtime(func):
    import time
    @functools.wraps(func)
    def wrapper_print_runtime(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f'Debug: Runtime of {func.__name__}: {time.time()-start}s')
        return result
    return wrapper_print_runtime

@print_runtime
def analyze(filename):
    with open(filename, "r", encoding="utf-8") as fh:
        content = fh.readlines()

        counts = dict(getCountMessages(content))
        names = list(counts.keys())

        # counts["total"] = sum([count for count in counts.values()])
        print(counts)

        total_msg_length = getTotalMsgLength(content, names)
        print(total_msg_length)

        avg_msg_length = {name: total_msg_length[name] / counts[name] for name in names}
        print(avg_msg_length)

        getCountEmoticons(content, names)


def count_words(text):
    text = ",".join(text).lower() 
    skips = [".", ", ", ":", ";", "'", '"'] 
    for ch in skips: 
        text = text.replace(ch, "") 
    word_counts = Counter(text.split(" ")) 
    print(OrderedDict(word_counts.most_common()))

def getTotalMsgLength(text, names):
    total_msg_length = {name: 0 for name in names}
    for line in text:
        name = getNameFromLine(line)
        msg = " ".join(line[21:].split(": ")[1:])
        msg_length = len(msg)
        total_msg_length[name] += msg_length

    return total_msg_length

def getCountMessages(text):
    return Counter([line[21:].split(" ")[0].replace(":", "") for line in text])

def getCountEmoticons(text, names):
    count_emoticons = {name: 0 for name in names}
    emoticons_unicode_range = range(12582, 128692)
    for line in text:
        name = getNameFromLine(line)
        count_emoticons[name] += len(list(filter(lambda x: ord(x) in emoticons_unicode_range, line)))
    print(count_emoticons)

def getNameFromLine(line):
    return line[21:].split(" ")[0].replace(":", "")


def correctLines(input_filename, output_filename):
    with open(input_filename, "r", encoding="utf-8") as input_fh, open(output_filename, "w", encoding="utf-8") as output_fh:
        input_lines = input_fh.readlines()

        first_line = True
        for line in input_lines:
            new_chat_line = line[0] == "[" and line[3] == "."
            line = line.strip()
            if new_chat_line and not first_line:
                line = "\n" + line
            output_fh.write(line)
            first_line = False


if __name__ == "__main__":
    correctLines("_chat.txt", "out.txt")
    analyze("out.txt")
