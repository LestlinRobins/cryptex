from PyPDF2 import PdfReader
import pdfplumber

# Parsing the text from response sheet of the candidate
response_sheet_reader = PdfReader("Test Response Data/answers.pdf")
number_of_pages_in_response_sheet = len(response_sheet_reader.pages)
response_sheet_text = ''
for line in range(number_of_pages_in_response_sheet):
    page = response_sheet_reader.pages[line]
    response_sheet_text = response_sheet_text + page.extract_text()

# Getting exam details like date and shift and candidate details
candidate_details = response_sheet_text.split()
application_no = candidate_details[candidate_details.index('No') + 1]
candidate_name = ' ' 
candidate_name = candidate_name.join(candidate_details[candidate_details.index('Name') + 1:candidate_details.index('Roll')])
exam_date = candidate_details[candidate_details.index('Date') + 1]
exam_time = candidate_details[candidate_details.index('Time') + 1:candidate_details.index('Time') + 6]
roll_no = candidate_details[candidate_details.index('Roll') + 2]
if exam_time[0] == '3:00':
    exam_shift = 'Second'
else:
    exam_shift = 'First'

# Removing unwanted things
response_sheet_text = response_sheet_text.replace("JEE April 2024", '')
response_sheet_text = response_sheet_text.replace("Application No "+ application_no, '')
response_sheet_text = response_sheet_text.replace("Candidate Name "+ candidate_name, '')
response_sheet_text = response_sheet_text.replace("Roll No " + roll_no, '')
response_sheet_text = response_sheet_text.replace("Test Date "+ exam_date, '')
response_sheet_text = response_sheet_text.replace("Test Time " + ' '.join(exam_time), '')
response_sheet_text = response_sheet_text.replace("Subject B. Tech", '')

# In case of download links in the pdf, this bit of code removes it from the details.
waste = ' '.join(candidate_details[0:4])
if '/' in waste and 'PM' in waste and 'cdn3.digialm.com' in waste:
    response_sheet_text = response_sheet_text.replace(waste,'')

# Continuing removal of common unwanted things
response_sheet_text = response_sheet_text.replace("Section :  Mathematics Section A", '')
response_sheet_text = response_sheet_text.replace("Section :  Mathematics Section B", '')
response_sheet_text = response_sheet_text.replace("Section :  Physics Section A", '')
response_sheet_text = response_sheet_text.replace("Section :  Physics Section B", '')
response_sheet_text = response_sheet_text.replace("Section :  Chemistry Section A", '')
response_sheet_text = response_sheet_text.replace("Section :  Chemistry Section B", '')
response_sheet_text = response_sheet_text.replace("Section : Mathematics Section A", '')
response_sheet_text = response_sheet_text.replace("Section : Mathematics Section B", '')
response_sheet_text = response_sheet_text.replace("Section : Physics Section A", '')
response_sheet_text = response_sheet_text.replace("Section : Physics Section B", '')
response_sheet_text = response_sheet_text.replace("Section : Chemistry Section A", '')
response_sheet_text = response_sheet_text.replace("Section : Chemistry Section B", '')
response_sheet_text = response_sheet_text.split('Q.')
response_sheet_text.remove(response_sheet_text[0])
# Now we got each question as its own line in the list called text

# Initiating a list for holding question parameters as individual dictionary items.
response_sheet_details = []

# Each 'question' is one line which contains that question's all parameters
for question_line in response_sheet_text:
    question_No = 0
    question_ID = None
    status = 'Not Answered'
    chosen_option = '--'
    chosen_option_ID = '--'
    numerical_answer = '--'
    question_line = question_line.split('\n')
    # Now we get a list called question_line which contains each parameter of the said question as a list object for iteration convenience.
    for question_parameter in question_line:
        question_No = question_line[0]
        if 'Question ID' in question_parameter:
            question_ID = question_parameter.replace('Question ID : ','')
            question_ID = question_ID.replace(' ','')
        if 'Status' in question_parameter:
            status = question_parameter.replace('Status :','')
            if status == 'Not Attempted and':
                status = 'Not Answered'
            if status == 'Marked For Review' or status == ' Marked For Review':
                status = 'Answered'
            if status == ' Answered':
                status = 'Answered'
            if status == ' Not Answered':
                status = 'Not Answered'
        if 'Chosen Option' in question_parameter:
            chosen_option = question_parameter.replace('Chosen Option : ','')
            if 'Option ' in response_sheet_text[int(question_No)-1]:
                details = response_sheet_text[int(question_No)-1]
                details = details.split('\n')
                newlist = [ele for ele in details if 'Option '+chosen_option+' ID' in ele]
                if len(newlist)==0:
                    chosen_option_ID = '--'
                else:
                    chosen_option_ID = newlist[0]
                    chosen_option_ID = chosen_option_ID.replace('Option '+chosen_option+' ID : ','')
                    chosen_option_ID = chosen_option_ID.replace(' ','')
        if 'Answer :' in question_parameter:
            numerical_answer = question_parameter.replace('Answer :','')
    response_sheet_details.append({'Question No.':question_No, 'Question ID' : question_ID, 'Question Status' : status, 'Chosen Option':chosen_option, 'Chosen Option ID': chosen_option_ID, 'Numerical Answer':numerical_answer, 'Marks Obtained':0})

# For counting number of answered questions
answered_qns_no = 0
answered_maths_sectionA_qns_no = 0
answered_maths_sectionB_qns_no = 0
answered_physics_sectionA_qns_no = 0
answered_physics_sectionB_qns_no = 0
answered_chemistry_sectionA_qns_no = 0
answered_chemistry_sectionB_qns_no = 0

for each_question in response_sheet_details:
    # print(each_question)   # Prints each line/question parameters in the list response_sheet_details. Each question parameters is stored as dict.

    # Question numbers 1 to 30 is maths, 31 to 60 is physics, and 61 to 90 is maths.
    if each_question['Question Status'] == 'Answered' and int(each_question['Question No.']) in range(1,21):
        answered_maths_sectionA_qns_no +=1
    if each_question['Question Status'] == 'Answered' and int(each_question['Question No.']) in range(21,31):
        answered_maths_sectionB_qns_no +=1
    if each_question['Question Status'] == 'Answered' and int(each_question['Question No.']) in range(31,51):
        answered_physics_sectionA_qns_no +=1
    if each_question['Question Status'] == 'Answered' and int(each_question['Question No.']) in range(51,61):
        answered_physics_sectionB_qns_no +=1
    if each_question['Question Status'] == 'Answered' and int(each_question['Question No.']) in range(61,81):
        answered_chemistry_sectionA_qns_no +=1
    if each_question['Question Status'] == 'Answered' and int(each_question['Question No.']) in range(81,91):
        answered_chemistry_sectionB_qns_no +=1

answered_qns_no = answered_maths_sectionA_qns_no + answered_maths_sectionB_qns_no + answered_physics_sectionA_qns_no + answered_physics_sectionB_qns_no + answered_chemistry_sectionA_qns_no + answered_chemistry_sectionB_qns_no

# Now parsing the text from the FINAL answer key published by NTA
pdf = pdfplumber.open("answerkey.pdf")
answer_key_data = ''
# Iterate over each page and extract the text of each page.
for number, pageText in enumerate(pdf.pages):
   text = pageText.extract_text().split()
   # Getting the answer key for the required day and shift only
   if text[27] == exam_date.replace('/','.') and text[31] == exam_shift:  
      answer_key_data = text

# Removing unwanted things
del answer_key_data[0:56]

answer_key = {}
for i in answer_key_data:
   # Getting the question ID:option ID/numerical answer pair for maths.
   if answer_key_data.index(i) in range (0, 180, 6):
      answer_key[i] = answer_key_data[answer_key_data.index(i)+1]
   # Getting the question ID:option ID/numerical answer pair for physics.
   if answer_key_data.index(i) in range (2, 182, 6):
      answer_key[i] = answer_key_data[answer_key_data.index(i)+1]
   # Getting the question ID:option ID/numerical answer pair for chemistry.
   if answer_key_data.index(i) in range (4, 184, 6):
      answer_key[i] = answer_key_data[answer_key_data.index(i)+1]

marks = 0
for i in response_sheet_details:
    for j in answer_key:
        if i['Question ID'] == j:
            if i['Chosen Option ID'] == answer_key[j] or i['Numerical Answer']==answer_key[j]:
                marks+=4
                i['Marks Obtained'] = 4
            elif (i['Chosen Option ID'] != answer_key[j] and i['Chosen Option ID'] != '--') or (i['Numerical Answer']!=answer_key[j] and i['Numerical Answer']!= '--'):
                marks -=1
                i['Marks Obtained'] = -1
            elif answer_key[j] == 'DROP':
                marks +=4 
                i['Marks Obtained'] = 4

# Displaying all the details parsed in a proper manner
print('Candidate Application Number:', application_no)
print('Candidate Name:', candidate_name, '\n')
print('Exam Date:', exam_date)
print('Exam Shift:', 'First Shift - 9:00 A.M. to 12:00 P.M.' if exam_shift == 'First' else 'Second Shift - 3:00 P.M. to 6:00 P.M.', '\n')
print('Total number of questions answered:', answered_qns_no)
print('Number of questions answered in Mathematics section A: ', answered_maths_sectionA_qns_no)
print('Number of questions answered in Mathematics section B: ', answered_maths_sectionB_qns_no)
print('Number of questions answered in Physics section A: ', answered_physics_sectionA_qns_no)
print('Number of questions answered in Physics section B: ', answered_physics_sectionB_qns_no)
print('Number of questions answered in Chemistry section A: ', answered_chemistry_sectionA_qns_no)
print('Number of questions answered in Chemistry section B: ', answered_chemistry_sectionB_qns_no)
# print(response_sheet_details)
print('\nTotal Marks Obtained: ', marks)

