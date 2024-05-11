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


def word_counter(word, i):    
    cnt = [0] * 29
    for c in word:
        # cnt[0:26]: the times of occurrence of alphabet[i] in word
        cnt[ord(c) - ord('a')] += 1
        # cnt[-1]: whether any alphabet exists in the word or not
        cnt[-1] |= 1 << (ord(c) - ord('a'))
    score = calculate_score(cnt)
    # cnt[-2]: the score of word
    cnt[-2] = score
    # cnt[-3]: the index of word in dictionary
    cnt[-3] = i
    return cnt


def calculate_score(word_list):
    scores = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]
    score = 0
    for i in range(26):
        score += scores[i] * word_list[i]
    return score


def find_max_anagram(random_word, new_dictionary):
    target_word_list = word_counter(random_word, 0)
    alphabets = target_word_list[-1]
    max_anagram_index = -1
    for l in new_dictionary:
        if l[-1] & alphabets != l[-1]:
            continue
        is_anagram = True
        for i in range(26):
            if target_word_list[i] < l[i]:
                is_anagram = False
                break
        # new_dictionary is in descending order by word score
        # The first anagram found has the highest score
        if is_anagram:
                max_anagram_index = l[-3]
                return max_anagram_index
                
    return max_anagram_index


def output_max_anagrams(target_words, dictionary, output_file):
    new_dictionary = []
    for i, word in enumerate(dictionary):
        cnt = word_counter(word, i)
        new_dictionary.append(cnt)
    # Sort the new_dictionary in descending order by word score
    new_dictionary = sorted(new_dictionary, key=lambda x: x[-2], reverse=True)
    
    with open(output_file, 'w') as file:
        for random_word in target_words:
            max_anagram_index = find_max_anagram(random_word, new_dictionary)
            max_anagram = dictionary[max_anagram_index] if max_anagram_index != -1 else "Not Found!"
            file.write(max_anagram + '\n')
        


if __name__ == "__main__":
    word_file = "words.txt"
    dictionary = read_file(word_file)
    small_words = read_file("small.txt")
    medium_words = read_file("medium.txt")
    large_words = read_file("large.txt")
    
    output_max_anagrams(small_words, dictionary, "small_answer.txt")
    # You answer is correct! Your score is 193.
    print("Done")
    output_max_anagrams(medium_words, dictionary, "medium_answer.txt")
    # You answer is correct! Your score is 18911.
    print("Done")
    output_max_anagrams(large_words, dictionary, "large_answer.txt")
    # You answer is correct! Your score is 244642.
    print("Done")
    
