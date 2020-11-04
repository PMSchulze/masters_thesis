import re

# Write function to prepare data for usage 
# with transformers.LineByLineTextDataset.
# That is, we concatenate and use a separate line for the text 
# of each document.
def prepare_linebyline(input_file_path, output_file_path):
    docs = ['']
    with open(input_file_path, encoding="utf-8") as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip()
            if len(line) != 0:
                if line[0] != '=':
                    docs[-1] += line
            else:
                if docs[-1] != '':
                    docs.append('')
    docs.pop()
    with open(output_file_path, 'w') as text_file:
        for line in docs:
            if len(line)>=20:
                print(line, file = text_file)

# Write function to prepare data for usage 
# with transformers.LineByLineTextDataset with block_size=n.
# That is, we concatenate and use a separate line for the text 
# of each document AND jump to new line if line_length>n after the end of the
# last sentence.
def prepare_linebyline_n(input_file, n):
    docs = []
    for line in input_file:
        line_split = re.split("\s+\.|\!|\?", line)
        line_split = [l.strip()+' . ' for l in line_split if l!='\n']
        l = len(line_split)
        i = 0
        truncated_lines = []
        while i<l:
            truncated_line = line_split[i]
            if i == l-1:
                truncated_lines.append(truncated_line)
                break
            for _ in range(i,l-1):
                if len(truncated_line)<n:
                    i += 1
                    truncated_line += line_split[i]        
                else:
                    break
            truncated_lines.append(truncated_line)
            i += 1
        if truncated_lines!=['']:
            docs.extend(truncated_lines)
    docs = list(filter(None,docs))
    return docs


# Write function to split a textfile into two part: one which contains the p
# shortest documents, and another one which ontains the remaining 1-p largest
# documents.
def split_documents_by_len(input_file_path,p):
    docs, docs_short, docs_long = [], [], []
    with open(input_file_path, encoding='utf-8') as f:
        for i, l in enumerate(f):
            docs.append(l)
        docs.sort(key=len)
        split_line = round((i+1)*p)
        docs_short = docs[:split_line]
        docs_long = docs[split_line:]
    return docs_short, docs_long


# Write function to prepare data for usage 
# with transformers.TextDatasetForNextSentencePrediction.
# That is, we place each sentence on a separate line and add blank lines 
# between documents.
def prepare_nextsentence(input_file, output_file_path):
    docs = []
    for line in input_file:
        docs.append('')
        line = re.split("\s+\.|\!|\?", line)
        docs[-1] = [l.strip()+' .' for l in line if l!='\n' ]
    # del(docs[-1]); del(docs[-1][-1])
    docs_len = len(docs)
    with open(output_file_path, 'w') as text_file:
        for i, doc in enumerate(docs):
            for sentence in doc:
                if len(sentence)>=20:
                    print(sentence, file = text_file)
                if i<docs_len-1:
                    print('', file = text_file)


# Take two textfiles as input, one with short documents on each line, and
# another one with long documents on each line. Then, split each document into
# smaller chunks by iteratively adding sentences until the chunk length exceeds 
# len_short and len_long, respectively. Furthermore, drop chunks with length<20 characters, 
# and finally transfer all short chunks to short file (these are leftovers from the long cunks 
# and only amount to 3687 chunks out of 699440 total chunks, i.e., about 0.5%).
def divide_into_chunks(
    input_file_short, input_file_long, len_short, len_long
):
    docs_short = prepare_linebyline_n(
        input_file = input_file_short,
        n = len_short
    )
    docs_long = prepare_linebyline_n(
        input_file = input_file_long,
        n = len_long
    )
    docs_short_tmp, docs_long_tmp = [], []
    docs_short_tmp = [doc for doc in docs_short if len(doc)>=20]
    docs_long_tmp = [doc for doc in docs_long if len(doc)>=20]
    docs_short_out, docs_long_out = docs_short_tmp, []
    for doc in docs_long_tmp:
        if len(doc)<len_short:
            docs_short_out.append(doc)
        else:
            docs_long_out.append(doc)
    return docs_short_out, docs_long_out

