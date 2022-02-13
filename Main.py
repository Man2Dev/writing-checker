import language_tool_python

tool = language_tool_python.LanguageTool("en-US")

# input text
text = "a santence with a error in the Hitchhiker’s Guide tot he Galaxy. hallo how are yoo."

matches = tool.check(text)

print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

# printing all mistakes
i = 0
for match in matches:
    print(f"\nMatch {i+1}:")
    print("1\nMessage:\n", match.message, "\n")
    print("2\nOffset:", matches[i].offsetInContext, "\n")
    print("3\nerrorLength:", matches[i].errorLength, "\n")
    print("4\ncontext:", matches[i].context, "\n")
    print("5\nCategory:", matches[i].category, "\n")
    print("6\nRule Issue Type:", matches[i].ruleIssueType, "\n")
    print("7\nSentence:", matches[i].sentence, "\n")
    print("A\nID [Suggestion]:\n", matches[i].ruleId, matches[i].replacements, "\n")
    print("B\nMatche:\n", matches[i])
    print("-----------------------------------------------------------------")
    i += 1

print("\n##############################################################################################################")

print("Number of mistakes:\t", len(matches))
print("Input text:\t\t", text)
print("Auto Correted:\t\t", tool.correct(text))
print("Auto Correted:\t\t", language_tool_python.utils.correct(text, matches))

print("##############################################################################################################")

tool.close()  # Call `close()` to shut off the server when you're done.
