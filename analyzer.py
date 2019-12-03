def analyze(filename):
    with open(filename, "r", encoding="utf-8") as fh:
        num_messages = {}
        avg_length_messages = {}
        for line in fh:
            
            name = line[21:].split(" ")[0].replace(":", "")
            if not name in num_messages.keys():
                num_messages[name] = 1
            else:
                num_messages[name] += 1

            if not name in avg_length_messages.keys():
                avg_length_messages[name] = len(line)
            else:
                avg_length_messages[name] += len(line)
            
        avg_length_messages["Sarah"] = avg_length_messages["Sarah"] / num_messages["Sarah"]
        avg_length_messages["Jannik"] = avg_length_messages["Jannik"] / num_messages["Jannik"]

        print(num_messages)
        print(avg_length_messages)


def correctLines(input_filename, output_filename):
    with open(input_filename, "r", encoding="utf-8") as input_fh, open(output_filename, "w", encoding="utf-8") as output_fh:
        input_lines = input_fh.readlines()

        # for line in input_lines:
            # print(line[:-1])
        first_line = True
        for line in input_lines:
            new_chat_line = line[0] == "["
            line = line.strip()
            if new_chat_line and not first_line:
                line = "\n" + line
            output_fh.write(line)
            first_line = False


if __name__ == "__main__":
    correctLines("_chat.txt", "out.txt")
    analyze("out.txt")
