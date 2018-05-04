import csv
import re
from string import Template

text = ''

with open('paragraph.txt') as f:
    text = f.read()

# pattern match for words. Can include hyphens but not start with them
# (to eliminate dashes from word count)
p = re.compile(r'\b\w[\w-]*\b')
m = p.findall(text)

# word count = num matches
word_count = len(m)

# Sentences = Strings occuring before line end punctuation
sentences = re.split(r'(?<=[.!?]) +', text)
sentence_count = len(sentences)

# Only counting alphas for letter count
letter_count = len(re.findall(r'[a-zA-Z-]', text))

# Don't count spaces; that rewards the illiterates
average_letters = round(letter_count/word_count, 2)

sentence_length = word_count / sentence_count

# OK templates are cool. Substitute in the variables
result = Template("""
Paragraph Analysis
-----------------
Approximate Word Count: $word_count
Approximate Sentence Count: $sentence_count
Average Letter Count: $average_letters
Average Sentence Length: $sentence_length
""")

# substitute in the values
result = result.substitute(word_count=word_count, \
    sentence_count=sentence_count, average_letters=average_letters, \
    sentence_length=sentence_length)

# Print and write to file
print(result)

with open('result.txt', 'w') as f :
    f.write(result)
