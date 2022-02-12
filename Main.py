import language_tool_python
tool = language_tool_python.LanguageTool('en-US')
text = 'A sentence with a error in the Hitchhiker’s Guide tot he Galaxy'
matches = tool.check(text)

print("Number of mistakes:", len(matches), "\n")

i = 0
for match in matches:
    i += 1
    print(f"\nMatch {i}:")
    print(match.message)

print("Auto Correted:\n", tool.correct(text))


tool.close() # Call `close()` to shut off the server when you're done.