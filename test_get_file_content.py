from functions.get_file_content import get_file_content

def test_get_file_content():
    content = get_file_content("calculator", "lorem.txt")
    print("File len:", len(content))
    print(f"Was truncated? {'truncated at' in content}")


    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))
    print(get_file_content("calculator", "pkg/does_not_exist.py"))
test_get_file_content()
