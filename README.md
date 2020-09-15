
## Installation

```
git clone https://github.com/huggingface/transformers
cd transformers
pip install .
pip install -r ./examples/requirements.txt
```

## Generation of Token Vocabulary

### BERT
```
from tokenizers import BertWordPieceTokenizer

# Specify path of pre-training data
vocab_path = "/home/ubuntu/data/pretrain_data/wiki_train.txt"

# Initialize BERT's WordPiece tokenizer 
tokenizer = BertWordPieceTokenizer()

# Generate WordPiece token vocabulary from pre-training data
tokenizer.train(vocab_path)

# Save the vocabulary
tokenizer.save_model("/home/ubuntu/data/token_vocab/bert/")
```

## Pre-training

### BERT

For pre-training details check `pretrain_bert.py` in this repository.

#### BERT with half-sized architecture components
```
python ~/python_files/pretrain_bert.py \
    --hidden_size 384 \
    --num_hidden_layers 6 \
    --num_attention_heads 6 \
    --intermediate_size 1536 \
    --num_train_epochs 10 \
    --output_dir /home/ubuntu/models/bert/bert_half \
    --corpus_pretrain /home/ubuntu/data/pretrain_data/wiki_train.txt \
    --token_vocab /home/ubuntu/data/token_vocab/bert/
```

#### BERT with three-quarter-sized architecture components
```
python ~/python_files/pretrain_bert.py \
    --hidden_size 576 \
    --num_hidden_layers 9 \
    --num_attention_heads 9 \
    --intermediate_size 2304 \
    --num_train_epochs 10 \
    --output_dir /home/ubuntu/models/bert/bert_threequarter \
    --corpus_pretrain /home/ubuntu/data/pretrain_data/wiki_train.txt \
    --token_vocab /home/ubuntu/data/token_vocab/bert/
```

Hyperparameters               | bert_half
------------------------------| -----------------
hidden_size                   | 384
num_hidden_layers             | 6
num_attention_heads           | 6
intermediate_size             | 1536
num_train_epochs              | 10
attention_probs_dropout_prob  | 0.1
hidden_dropout_prob           | 0.1
block_size                    | 128
learning_rate                 | 1e-4
weight_decay                  | 0.01
warmup_steps                  | 1820
adam_beta1                    | 0.9
adam_beta2                    | 0.999
adam_epsilon                  | 1e-6
per_device_train_batch_size   | 64
 

## Fine-tuning

### GLUE

- DATA DOWNLOAD: `python utils/download_glue_data.py --data_dir ~/data/glue --tasks all`
- RUN SCRIPT IN TRANSFORMERS REPO!

```
export GLUE_DIR=~/data/glue
export MODEL=bert
export VARIANT=bert_half
export SEED=2020

cp /home/ubuntu/data/token_vocab/$MODEL/vocab.txt /home/ubuntu/models/$MODEL/$VARIANT/vocab.txt

for TASK in SST-2 QNLI RTE CoLA WNLI QQP MRPC STS-B MNLI
do
    python ./examples/text-classification/run_glue.py \
        --model_name_or_path /home/ubuntu/models/$MODEL/$VARIANT \
        --task_name ${TASK} \
        --save_total_limit 1\
        --do_train \
        --do_eval \
        --data_dir $GLUE_DIR/${TASK} \
        --max_seq_length 128 \
        --per_device_train_batch_size=32   \
        --learning_rate 2e-5 \
        --num_train_epochs 3.0 \
        --output_dir /home/ubuntu/fine_tuned/$MODEL/$VARIANT/glue/${TASK}/ \
        --overwrite_output_dir \
        --seed $SEED
done
```

GLUE tasks                    | bert_half        
------------------------------| -----------------
SST-2                         | 86.24            
QNLI                          | 83.12
RTE                           | 55.23
CoLA                          | 12.59
WNLI                          | 39.44
QQP                           | 82.08
MRPC                          | 81.25
STS-B                         | 69.40
MNLI                          | 
