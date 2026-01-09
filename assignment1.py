def reverse_words(string: str) -> str:
    """
    Returns the input string reversed alphanumerically, 
    i.e. the symbols and spaces are unchanged, only the words are reversed

    Time/Space Complexity: O(n), where n is length of input string

    Approach Explanation:
    Iterate through the string while skipping through the non-alphanumerical characters.
    When an alphanumerical character is found, mark it as `start` use a different loop
    to iterate through until the string ends / another non-alphanumerical character is found
    then perform the reversal from the `start` index.
    """

    arr = list(string) # convert to array for efficient mutability
    n = len(arr)
    i = 0

    while i < n:
        # skip the char if it's a symbol
        if not arr[i].isalnum():
            i += 1
            continue

        # perform the reverse
        start = i
        while i < n and arr[i].isalnum():
            i += 1

        arr[start:i] = arr[start:i][::-1]


    return "".join(arr)

def main():
    test_str = "String; 2be reversed..."
    result = reverse_words(test_str)
    assert result == "gnirtS; eb2 desrever..."

    assert reverse_words("") == ""
    assert reverse_words("hello world!") == "olleh dlrow!"
    assert reverse_words("a1b2c3") == "3c2b1a"
    assert reverse_words("one   two three") == "eno   owt eerht"
    assert reverse_words("!@# $%^") == "!@# $%^"
    assert reverse_words("word!word?word.") == "drow!drow?drow."
    assert reverse_words("123 456 789") == "321 654 987"

if __name__ == "__main__":
    main()
