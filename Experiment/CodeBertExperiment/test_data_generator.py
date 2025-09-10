import json
import textwrap

def generate_python_functions(n=69):
    dataset = []
    templates = [
        ("add", "Adds two numbers", "def {name}(x, y):\n    return x + y"),
        ("subtract", "Subtracts y from x", "def {name}(x, y):\n    return x - y"),
        ("multiply", "Multiplies two numbers", "def {name}(x, y):\n    return x * y"),
        ("divide", "Divides x by y safely", "def {name}(x, y):\n    return x / y if y != 0 else None"),
        ("power", "Raises x to the power of y", "def {name}(x, y):\n    return x ** y"),
        ("factorial", "Computes factorial of n", textwrap.dedent(
            "def {name}(n):\n"
            "    if n == 0:\n"
            "        return 1\n"
            "    result = 1\n"
            "    for i in range(1, n+1):\n"
            "        result *= i\n"
            "    return result"
        )),
        ("fibonacci", "Returns n-th Fibonacci number", textwrap.dedent(
            "def {name}(n):\n"
            "    a, b = 0, 1\n"
            "    for _ in range(n):\n"
            "        a, b = b, a+b\n"
            "    return a"
        )),
        # Boolean / conditional
        ("is_even", "Checks if a number is even", "def {name}(n):\n    return n % 2 == 0"),
        ("is_odd", "Checks if a number is odd", "def {name}(n):\n    return n % 2 != 0"),
        ("is_prime", "Checks if a number is prime", textwrap.dedent(
            "def {name}(n):\n"
            "    if n < 2:\n"
            "        return False\n"
            "    for i in range(2, int(n**0.5)+1):\n"
            "        if n % i == 0:\n"
            "            return False\n"
            "    return True"
        )),
        ("is_palindrome", "Checks if string is a palindrome", "def {name}(s):\n    return s == s[::-1]"),
        # String
        ("reverse_string", "Reverses a string", "def {name}(s):\n    return s[::-1]"),
        ("count_vowels", "Counts vowels in a string", textwrap.dedent(
            "def {name}(s):\n"
            "    vowels='aeiouAEIOU'\n"
            "    return sum(1 for ch in s if ch in vowels)"
        )),
        ("capitalize_words", "Capitalizes every word in string", "def {name}(s):\n    return ' '.join(w.capitalize() for w in s.split())"),
        # List
        ("sum_list", "Returns sum of a list", "def {name}(lst):\n    return sum(lst)"),
        ("max_list", "Returns maximum value in a list", "def {name}(lst):\n    return max(lst)"),
        ("min_list", "Returns minimum value in a list", "def {name}(lst):\n    return min(lst)"),
        ("flatten_list", "Flattens a nested list", textwrap.dedent(
            "def {name}(lst):\n"
            "    return [item for sublist in lst for item in sublist]"
        )),
        ("filter_even", "Filters even numbers from a list", "def {name}(lst):\n    return [x for x in lst if x % 2 == 0]"),
        ("filter_odd", "Filters odd numbers from a list", "def {name}(lst):\n    return [x for x in lst if x % 2 != 0]"),
        # Dictionary
        ("invert_dict", "Inverts keys and values in a dict", "def {name}(d):\n    return {v:k for k,v in d.items()}"),
        ("merge_dicts", "Merges two dictionaries", "def {name}(d1, d2):\n    return {**d1, **d2}"),
        ("count_keys", "Counts keys in a dictionary", "def {name}(d):\n    return len(d.keys())")
    ]
    
    for i in range(n):
        fname, desc, code = templates[i % len(templates)]
        func_name = f"{fname}_{i}"  # unique name per entry
        entry = {
            "code": code,
            "nl_desc": desc,
            "func_name": func_name,
            "code_with_desc": f"{desc} [SEP] {code}"
        }
        dataset.append(entry)
    
    return dataset

if __name__ == "__main__":
    data = generate_python_functions(69)

    # save to file
    with open("./datas/python_test_data.json", "w") as f:
        json.dump(data, f, indent=2)

    print("✅ Generated python_test_data.json with", len(data), "entries")
