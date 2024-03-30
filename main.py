from subprocess import run
from threading import Thread


# word size input, dictionary name
size = int(input("Word size: "))
dictionary = "simple3.txt"

# tracking of trees
maximum = 0
word_count = 0
words = ["", ""]

# tracking threads & thread data
thread_count = 10    # amount of threads
threads = []         # list of threads
words_visited = 0    # count of words seen from dictionary in start loop
active_words = []    # list of words being checked
active_indexes = []  # list of indexes being checked

# init lists based on thread count
for i in range(thread_count):
    threads.append(0)
    active_words.append("")
    active_indexes.append(0)


# runs the ladder check given a word and the words index in the dictionary
def check_word(word_a: str, start: int):
    global maximum, words, lines

    # starting at the word after the given word, for each word in the dict:
    for k in range(start + 1, len(lines)):
        # get the word, check its size
        word_b = lines[k].replace("\n", "")
        if len(word_b) != size:
            continue

        # if it's the correct size, run the C-program and capture the output
        output = run("./ladder", input=f"{size}\n{dictionary}\n{word_a}\n{word_b}",
                     capture_output=True, text=True, timeout=3).stdout

        # take just the number given as the longest height of the ladder
        n = int(output[output.find("Word Ladder height") + 21:])

        # if this height is the greatest so far, record the size and words used
        if n > maximum:
            words[0] = word_a
            words[1] = word_b
            maximum = n


if __name__ == "__main__":
    # open the dictionary, get the lines
    with open(dictionary, "r") as d:
        lines = d.readlines()

    # get the line count
    line_count = len(lines)

    # for each line (word):
    while words_visited < line_count:
        # for each thread
        for i in range(thread_count):
            # index protection
            if words_visited >= line_count:
                break

            # get the word
            word = lines[words_visited].replace("\n", "")

            # if the size is incorrect:
            while len(word) != size:
                # go to the next word
                words_visited += 1

                # index protection
                if words_visited >= line_count:
                    break

                # get the word
                word = lines[words_visited].replace("\n", "")

            # save the word in the thread-used lists
            active_words[i] = word
            active_indexes[i] = words_visited
            words_visited += 1

        # create `thread_count` threads
        for j in range(thread_count):
            # don't double-check if end of dict was reached
            if word_count >= line_count: break

            # increase words checked, create a thread to check that word and start it
            word_count += 1
            threads[j] = Thread(target=check_word, args=(active_words[j], active_indexes[j]))
            threads[j].start()

        # wait for all active threads to finish
        for j in range(thread_count):
            # don't double-check if end of dict was reached
            if word_count >= line_count: break

            threads[j].join(timeout=None)

        # after each thread set is done, update user on progress
        print(f"Max after {word_count} words checked: {maximum}, with {words[0]} and {words[1]}")

    # print final count
    print(f"Final Max of {maximum} with the words {words[0]} and {words[1]}, after checking a total of {word_count} words.")

##############################################
# Final Stats From Running
##############################################
# 3 - 0962 words checked.   ivy ->   pro in 11
# 4 - 3862 words checked.  atap ->  unau in 18
# 5 - 0015 words checked. above -> parol in 25
