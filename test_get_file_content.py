from functions.get_file_content import get_file_content

print("TEST1: Lorem Ipsum")
lorem_content = get_file_content("calculator", "lorem.txt")
print(f"Length: {len(lorem_content)}")
print(f"Ends with: {lorem_content[-60:]}")

print("TEST2: main.py")
print(get_file_content("calculator", "main.py"))

print("TEST3: calculator.py")
print(get_file_content("calculator", "pkg/calculator.py"))

print("TEST4: not allowed")
print(get_file_content("calculator", "/bin/cat"))

print("TEST5: not exist")
print(get_file_content("calculator", "pkg/does_not_exist.py"))