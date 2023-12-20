from os import path, listdir
from rank_bm25 import BM25Okapi
from docx import Document
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline

def initialize_resources():
    tokenizer = AutoTokenizer.from_pretrained("timpal0l/mdeberta-v3-base-squad2")
    model = AutoModelForQuestionAnswering.from_pretrained("timpal0l/mdeberta-v3-base-squad2")
    question_answerer = pipeline("question-answering", model=model, tokenizer=tokenizer)

    return question_answerer

def document_to_text(file_path, context_array):
    doc = Document(file_path)
    counter = 0
    context_local = ""
    len_context = 0

    for element in doc.element.body:
        if element.tag.endswith('p'):
            text = ' '.join([run.text.strip() for run in element.iterfind('.//w:t', namespaces={
                'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})])
            for word in text.split(" "):
                if len_context < 170:
                    context_local += word + " "
                    len_context += 1
                else:
                    context_array.append(context_local)
                    len_context = 0
                    context_local = ""
                    counter += 1

    if len_context > 0:
        context_array.append(context_local)
        counter += 1

    return counter

def BM25_find_block(bm_question, block_array):
    tokenized_blocks = [block.split() for block in block_array]
    bm25 = BM25Okapi(tokenized_blocks, b=0)
    scores = bm25.get_scores(bm_question.split())
    ranked_blocks = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    max_score = 0
    max_index = 0

    for rank, (block_idx, score) in enumerate(ranked_blocks):
        if score > max_score:
            max_score = score
            max_index = block_idx

    return max_index

def bert(question, context_array, link_array, link_idx):
    # Initialize resources
    question_answerer = initialize_resources()

    max_idx = BM25_find_block(question, context_array)
    link_index = 0

    for number in link_idx:
        if max_idx > number:
            link_index += 1
        else:
            break

    context = ""
    link = link_array[link_index]
    context += context_array[max_idx]

    result = question_answerer(question + "?", context)
    start, end = result["start"], result["end"]

    #print(f"Отрывок из инструкции: {context}")
    #print(f"Ссылка на статью: {link}")
    #print(f"Ответ на вопрос: {result['answer']}")
    response = f"Отрывок из инструкции: {context} \n Ссылка на статью: {link} \n Ответ на вопрос: {result['answer']}\n"
    print(response)
    return response

def qa_bert(question):
    folder = 'D:\Chat\server\logic\output'
    context_array = []
    link_array = ['https://cfl.digtp.com/display/IT175/Access+to+systems',
                  'https://cfl.digtp.com/pages/viewpage.action?pageId=84297694',
                  'https://cfl.digtp.com/pages/viewpage.action?pageId=72791741',
                  'https://cfl.digtp.com/pages/viewpage.action?pageId=81615049',
                  'https://cfl.digtp.com/pages/viewpage.action?pageId=81614957',
                  'https://cfl.digtp.com/pages/viewpage.action?pageId=81615355',
                  'https://cfl.digtp.com/pages/viewpage.action?pageId=135957679']

    link_idx = []
    idx = -1

    for file_index, file in enumerate(listdir(folder)):
        f = path.join(folder, file)
        count = document_to_text(f, context_array)
        idx += count
        link_idx.append(idx)

    # Example usage
    return bert(question, context_array, link_array, link_idx)

