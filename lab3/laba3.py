import re


def remove_special(text):
    return re.sub(r'\W+', '', text)

def word_with_char(text, char):
    pattern = rf'\b\w*{char}\w*\b'
    return re.findall(pattern, text)

def word_with_length(text, length):
    pattern = rf'\b\w{{{length}}}\b'
    return re.findall(pattern, text)

def word_a_b_s(text):
    pattern = r'\b[a|b]\w*s\b'
    return re.findall(pattern, text)
print("task1")
text = "apple bananas banana byby basics bats cats dogs!"
print(remove_special("Hi! My name% Ale!@x"))  
print(word_with_char(text, 'y'))  
print(word_with_length(text, 6))  
print(word_a_b_s(text)) 

print('-------------')
print("task2")

def collect_monetary_amounts(text): 
    amounts = re.findall(r'\$\d+\.\d+|\$\d+', text)
    float_amounts = [float(amount.replace('$', '')) for amount in amounts]
    return float_amounts, sum(float_amounts)

text = "First amount is $123.45, second amount is $400, and another one is $15.75."
amounts, total = collect_monetary_amounts(text)
print("Знайдені суми:", amounts)
print("Загальна сума:", total)

print('-------------')
print("task3")


def clean_code(code):   
    code = re.sub(r'\s*#.*', '', code)
   
    code = re.sub(r'\n\s*\n', '\n', code)
    return code.strip()

test_code = """
import math  # Імпорт бібліотеки

def square_root(x):
    return math.sqrt(x)  # Обчислення кореня

# Виклик функції
print(square_root(25))

"""
cleaned_code = clean_code(test_code)
print("Очищений код:\n", cleaned_code)

print('-------------')
print("task4")

def convert_date_format(text):  
    return re.sub(r'(\d{4})-(\d{2})-(\d{2})', r'\3-\2-\1', text)

sample_text = "Today's date is 2024-02-11 and another date is 2023-12-25."
converted_text = convert_date_format(sample_text)
print("Конвертований текст:", converted_text)
print('-------------')
