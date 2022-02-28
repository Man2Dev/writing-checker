from datetime import datetime

import language_tool_python

from database import answer, insert_exam, insert_match, question

tool = language_tool_python.LanguageTool("en-US")

matches = tool.check(answer)
miatakes_number = len(matches)
autoCorrected = tool.correct(answer)
created = datetime.now()

exam = ("Question 1", question, miatakes_number, answer, autoCorrected, created)
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

tool.close()  # Call `close()` to shut off the server when you're done.
