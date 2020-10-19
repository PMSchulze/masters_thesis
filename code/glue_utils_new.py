from transformers import GPT2Tokenizer

# Load GPT2 tokenizer
tokenizer = None

def encode_single(examples):
    modified_input = ['<|start|>'+ x + '<|end|>' for x in examples['sentence']]
    return tokenizer(modified_input, truncation = True, padding = 'max_length', max_length = 1024)

def encode_nli(examples, task):
    part1, part2 = '', ''
    if task == 'QNLI':
        part1, part2 = 'question', 'sentence'
    elif task == 'MNLI':
        part1, part2 = 'premise', 'hypothesis'
    else:
        part1, part2 = 'sentence1', 'sentence2'
    modified_input = ['<|start|>'+ x + '<$>' + y + '<|end|>' for x,y in zip(examples[part1], examples[part2])]
    tok = tokenizer(modified_input, truncation = True, padding = 'max_length', max_length = 1024)
    return tok

def encode_similarity(examples, task):
    part1, part2 = 'sentence1' if task != 'QQP' else 'question1', 'sentence2' if task != 'QQP' else 'question2'
    modified_input1 = ['<|start|>'+ x + '<$>' + y + '<|end|>' for x,y in zip(examples[part1], examples[part2])]
    modified_input2 = ['<|start|>'+ y + '<$>' + x + '<|end|>' for x,y in zip(examples[part1], examples[part2])]
    tok1 = tokenizer(modified_input1, truncation = True, padding = 'max_length', max_length = 1024)
    tok2 = tokenizer(modified_input2, truncation = True, padding = 'max_length', max_length = 1024)
    out = {
        'attention_mask1': tok1['attention_mask'],
        'attention_mask2': tok2['attention_mask'],
        'input_ids1': tok1['input_ids'],
        'input_ids2': tok2['input_ids'],
    }
    return out
    
def encode(examples, task):
    single = {'CoLA', 'SST-2'}
    nli = {'QNLI', 'RTE', 'WNLI', 'MNLI'}
    similarity = {'MRPC', 'STS-B', 'QQP'}
    if task in single:
        return encode_single(examples, task)
    elif task in similarity:
        return encode_similarity(examples, task)
    else:
        return encode_nli(examples, task)
