import language_tool_python

tool = language_tool_python.LanguageTool("en-US")

# input text
text = "A sentence with a error in the Hitchhiker’s Guide tot he Galaxy. hallo how are yoo."

matches = tool.check(text)

# printing all mistakes
i = 0
for match in matches:
    i += 1
    print(f"\nMatch {i}:")
    print(match.message)

print("\n")

print("Number of mistakes:\t", len(matches))
print("Input text:\t\t", text)
print("Auto Correted:\t\t", language_tool_python.utils.correct(text, matches), "\n")

tool.close()  # Call `close()` to shut off the server when you're done.