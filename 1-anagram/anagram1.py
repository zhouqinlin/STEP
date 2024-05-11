def read_file(file_name):
    words = []
    try:
        with open(file_name, "r") as file:
            for line in file:
                word = line.strip()
                words.append(word)
    except FileNotFoundError:
        print("File not found!")
    return words


def binary_search_anagram(target_string, dictionary):
    n = len(dictionary)
    left = 0
    right = n - 1
    founded_words = []
    while left <= right:
        mid = (left + right) // 2
        if dictionary[mid][0] < target_string:
            left = mid + 1
        elif dictionary[mid][0] > target_string:
            right = mid - 1
        else:  # dictionary[mid][0] == target_string
            founded_words.append(dictionary[mid][1])
            for i in range(mid - 1, -1, -1):
                if dictionary[i][0] == target_string:
                    founded_words.append(dictionary[i][1])
                else:
                    break
            for i in range(mid + 1, len(dictionary)):
                if dictionary[i][0] == target_string:
                    founded_words.append(dictionary[i][1])
                else:
                    break
            return sorted(founded_words)
    return founded_words


def find_anagram(random_word, dictionary):
    sorted_random_word = "".join(sorted(random_word))
    new_dictionary = []
    for word in dictionary:
        new_dictionary.append(("".join(sorted(word)), word))
    new_dictionary.sort()
    anagram = binary_search_anagram(sorted_random_word, new_dictionary)
    return anagram


if __name__ == "__main__":
    word_file = "words.txt"
    dictionary = read_file(word_file)
    anagram = find_anagram("leap", dictionary)
    print(anagram)
    anagram = find_anagram("p", dictionary)
    print(anagram)
    anagram = find_anagram("acdr", dictionary)
    print(anagram)
