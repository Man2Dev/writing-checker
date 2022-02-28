from datetime import datetime

import language_tool_python

from database import insert_exam, insert_match

tool = language_tool_python.LanguageTool("en-US")

question_name = input("Please enter your question name: ")
question = input("Please enter your question: ")
answer = input("Please enter your answer: ")

matches = tool.check(answer)
miatakes_number = len(matches)
autoCorrected = tool.correct(answer)
created = datetime.now()

exam = (question_name, question, miatakes_number, answer, autoCorrected, created)
exam_id = insert_exam(exam)


for match in matches:
    errText = match.message
    errOffset = match.offsetInContext
    errLength = match.errorLength
    context = match.context
    category = match.category
    ruleIssue = match.ruleIssueType
    sentence = match.sentence
    numberSuggestions = len(match.replacements)
    ruleID = match.ruleId
    Suggestions = match.replacements

    m = (
        errText,
        errOffset,
        errLength,
        context,
        category,
        ruleIssue,
        sentence,
        ruleID,
        numberSuggestions,
        str(Suggestions),
        exam_id,
    )

    insert_match(m)

print("Thanks for trying our app, you can see the results in database.db")

tool.close()  # Call `close()` to shut off the server when you're done.
