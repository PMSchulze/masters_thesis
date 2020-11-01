
## 0. Installation

```
git clone https://github.com/huggingface/transformers
cd transformers
pip install .
pip install -r ./examples/requirements.txt
```

Version: 3.4.0

## 1. Generation of Token Vocabulary

### 1.1. BERT
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

### 1.2. GPT-2
```
from tokenizers import ByteLevelBPETokenizer

# Specify path of pre-training data
vocab_path = "/home/ubuntu/data/pretrain_data/wiki_train.txt"

# Initialize GPT's BPE tokenizer 
tokenizer = ByteLevelBPETokenizer()

# Generate BPE token vocabulary from pre-training data
tokenizer.train(files=vocab_path, vocab_size=30_000, min_frequency=2, special_tokens=['<|endoftext|>', '<pad>'])

# Save the vocabulary
tokenizer.save_model("/home/ubuntu/data/token_vocab/gpt2/")

```

### 1.3. RoBERTa
```
from tokenizers import ByteLevelBPETokenizer

# Specify path of pre-training data
vocab_path = "/home/ubuntu/data/pretrain_data/wiki_train.txt"

# Initialize RoBERTa's BPE tokenizer 
tokenizer = ByteLevelBPETokenizer()

# Generate BPE token vocabulary from pre-training data
tokenizer.train(files=vocab_path, vocab_size=30_000, min_frequency=2, special_tokens=['<s>','<pad>','</s>','<mask>'])

# Save the vocabulary
tokenizer.save_model("/home/ubuntu/data/token_vocab/roberta/")
```
## 2. Pre-training

### 2.1. BERT

For pre-training details check `pretrain_bert.py` in this repository.

```
for VARIANT in 128_2_2_512_12 128_2_2_512_15 128_2_2_512_17
do
    NEPOCHS=$(echo $VARIANT | cut -d'_' -f 5)
    NWARMUP=$(($NEPOCHS*182))
    python /home/ubuntu/masters_thesis/code/pretrain_bert.py \
        --hidden_size $(echo $VARIANT| cut -d'_' -f 1) \
        --num_hidden_layers $(echo $VARIANT| cut -d'_' -f 2) \
        --num_attention_heads $(echo $VARIANT| cut -d'_' -f 3) \
        --intermediate_size $(echo $VARIANT| cut -d'_' -f 4) \
        --num_train_epochs $NEPOCHS \
        --warmup_steps $NWARMUP \
        --output_dir /home/ubuntu/models/bert/${VARIANT} \
        --corpus_pretrain /home/ubuntu/data/pretrain_data/wiki_train.txt \
        --token_vocab /home/ubuntu/data/token_vocab/bert/
done
```

#### Number of Training Epochs

Hyperparameters               | 128_2_2_512_10 | 128_2_2_512_12 | 128_2_2_512_15 | 128_2_2_512_17 | 128_2_2_512_20 
------------------------------| ----------|-----------------|----------------|---------------------|-----------------
hidden_size                   | 128       | 128    | 128         |  128           | 128                 
num_hidden_layers             | 2         | 2      | 2           |    2           | 2                   
num_attention_heads           | 2         | 2      | 2           |    2           | 2                   
intermediate_size             | 512       | 512    | 512         |  512           | 512                 
num_train_epochs              | 10        | 12     | 15          |   17           | 20                  
attention_probs_dropout_prob  | 0.1       | 0.1    | 0.1         |  0.1           | 0.1                 
hidden_dropout_prob           | 0.1       | 0.1    | 0.1         |  0.1           | 0.1                 
block_size                    | 128       | 128    | 128         |  128           | 128                
learning_rate                 | 1e-4      | 1e-4   | 1e-4        | 1e-4           | 1e-4               
weight_decay                  | 0.01      | 0.01   | 0.01        | 0.01           | 0.01               
warmup_steps                  | 1820      | 2184   | 2730        | 3094           | 3640               
adam_beta1                    | 0.9       | 0.9    | 0.9         |  0.9           | 0.9                
adam_beta2                    | 0.999     | 0.999  | 0.999       |0.999           | 0.999              
adam_epsilon                  | 1e-6      | 1e-6    | 1e-6        | 1e-6           | 1e-6               
per_device_train_batch_size   | 64        | 64      | 64          |   64           | 64                 
number of parameters          | 4,385,920 | 4,385,920 | 4,385,920 | 4,385,920      | 4,385,920                 
time (hh:mm:ss)               | 03:13:07  | 03:51:02| 04:48:27    | 05:27:13       | 07:31:24           


#### Number of Hidden Layers

Hyperparameters               | 128_2_2_512_10 |128_3_2_512_10 | 128_4_2_512_10 | 128_5_2_512_10 |128_6_2_512_10 |
------------------------------| ----------|----------|----------|----------|----------|
hidden_size                   | 128       |128       |128       | 128      | 128      |
num_hidden_layers             | 2         |3         |4         |5         |6         |
num_attention_heads           | 2         |2         |2         |2         |2         |
intermediate_size             | 512       |512       |512       |512       |512       |
num_train_epochs              | 10        |10        |10        |10        |10        |
attention_probs_dropout_prob  | 0.1       |0.1       |0.1       |0.1       |0.1       |
hidden_dropout_prob           | 0.1       |0.1       |0.1       |0.1       |0.1       |
block_size                    | 128       |128       |128       |128       |128       |
learning_rate                 | 1e-4      |1e-4      |1e-4      |1e-4      |1e-4      |
weight_decay                  | 0.01      |0.01      |0.01      |0.01      |0.01      |
warmup_steps                  | 1820      |1820      |1820      |1820      |1820      |
adam_beta1                    | 0.9       |0.9       |0.9       |0.9       |0.9       |
adam_beta2                    | 0.999     |0.999     |0.999     |0.999     |0.999     |
adam_epsilon                  | 1e-6      |1e-6      |1e-6      |1e-6      |1e-6      |
per_device_train_batch_size   | 64        | 64      | 64          |   64           | 64                 
number of parameters   | 4,385,920 |4,584,192 |4,782,464 |4,980,736 |5,179,008 |
time (hh:mm:ss)               | 03:13:07  |03:32:14  |03:49:09  |04:06:48  |04:19:44  |

#### Number of Attention Heads

Hyperparameters               | 128_2_2_512_10 | 128_2_4_512_10 | 128_2_8_512_10 |128_2_16_512_10 |128_2_32_512_10 |
------------------------------| ----------|----------|----------|----------|----------|
hidden_size                   | 128       |128       |128       |128       |128       |
num_hidden_layers             | 2         |2         |2         |2         |2         |
num_attention_heads           | 2         |4         |8         |16        |32        |
intermediate_size             | 512       |512       |512       |512       |512       |
num_train_epochs              | 10        |10        |10        |10        |10        |
attention_probs_dropout_prob  | 0.1       |0.1       |0.1       |0.1       |0.1       |
hidden_dropout_prob           | 0.1       |0.1       |0.1       |0.1       |0.1       |
block_size                    | 128       |128       |128       |128       |128       |
learning_rate                 | 1e-4      |1e-4      |1e-4      |1e-4      |1e-4      |
weight_decay                  | 0.01      |0.01      |0.01      |0.01      |0.01      |
warmup_steps                  | 1820      |1820      |1820      |1820      |1820      |
adam_beta1                    | 0.9       |0.9       |0.9       |0.9       |0.9       |
adam_beta2                    | 0.999     |0.999     |0.999     |0.999     |0.999     |
adam_epsilon                  | 1e-6      |1e-6      |1e-6      |1e-6      |1e-6      |
per_device_train_batch_size   | 64        | 64      | 64          |   64           | 64                 
number of parameters   | 4,385,920 |4,385,920 |4,385,920 |4,385,920 |4,385,920 |
time (hh:mm:ss)               | 03:13:07  |3:13:42   |03:16:19  |03:23:43  |03:36:20  |

#### Hidden Size

Hyperparameters               | 128_2_2_512_10 | 160_2_2_540_10 | 192_2_2_786_10 |288_2_2_1152_10 |384_2_2_1536_10 |
------------------------------| ----------|----------|----------|----------|----------|
hidden_size                   | 128       |160       |192       |288       |384       |
num_hidden_layers             | 2         |2         |2         |2         |2         |
num_attention_heads           | 2         |2         |2         |2         |2         |
intermediate_size             | 512       |540       |786       |1152      |1536      |
num_train_epochs              | 10        |10        |10        |10        |10        |
attention_probs_dropout_prob  | 0.1       |0.1       |0.1       |0.1       |0.1       |
hidden_dropout_prob           | 0.1       |0.1       |0.1       |0.1       |0.1       |
block_size                    | 128       |128       |128       |128       |128       |
learning_rate                 | 1e-4      |1e-4      |1e-4      |1e-4      |1e-4      |
weight_decay                  | 0.01      |0.01      |0.01      |0.01      |0.01      |
warmup_steps                  | 1820      |1820      |1820      |1820      |1820      |
adam_beta1                    | 0.9       |0.9       |0.9       |0.9       |0.9       |
adam_beta2                    | 0.999     |0.999     |0.999     |0.999     |0.999     |
adam_epsilon                  | 1e-6      |1e-6      |1e-6      |1e-6      |1e-6      |
per_device_train_batch_size   | 64        | 64      | 64          |   64           | 64                 
number of parameters   | 4,385,920 |5,546,200 |6,899,940 |11,020,320 |15,615,360 |
time (hh:mm:ss)               | 03:13:07  |3:35:53   |03:47:11  |04:41:14  |5:21:55   |

#### All Dimensions

Hyperparameters               | 384_6_6_1536_10 | 384_6_6_1536_20 | 192_3_3_786_10 | 192_3_3_786_20 | 128_2_2_512_10 | 128_2_2_512_20
------------------------------| ----------|-----------------|----------------|---------------------|-----------------|----------
hidden_size                   | 384       | 384    | 192         |  192           | 128                 | 128
num_hidden_layers             | 6         | 6      | 3           |    3           | 2                   |   2
num_attention_heads           | 6         | 6      | 3           |    3           | 2                   |   2
intermediate_size             | 1536      | 1536   | 786         |  786           | 512                 | 512
num_train_epochs              | 10        | 20     | 10          |   20           | 10                  |  20
attention_probs_dropout_prob  | 0.1       | 0.1    | 0.1         |   0.1          | 0.1                 |  0.1
hidden_dropout_prob           | 0.1       | 0.1    | 0.1         |  0.1           | 0.1                 |  0.1
block_size                    | 128       | 128    | 128         |  128           | 128                |  128
learning_rate                 | 1e-4      | 1e-4   | 1e-4        | 1e-4           | 1e-4                  | 1e-4
weight_decay                  | 0.01      | 0.01   | 0.01        | 0.01           | 0.01                | 0.01
warmup_steps                  | 1820      | 3640   | 1820        | 3640           | 1820                | 3640
adam_beta1                    | 0.9       | 0.9    | 0.9         |  0.9           | 0.9                 | 0.9
adam_beta2                    | 0.999     | 0.999  | 0.999       |0.999           | 0.999               | 0.999
adam_epsilon                  | 1e-6      | 1e-6   | 1e-6        | 1e-6           | 1e-6                 | 1e-6
per_device_train_batch_size   | 64        | 64      | 64          |   64           | 64                 
number of parameters   | 22,713,216| 22,713,216 | 7,351,734 |7,351,734     | 4,385,920            | 4,385,920
time (hh:mm:ss)               | 08:17:47  |16:35:57| 07:29:36    | 08:22:00       | 03:13:07             | 07:31:24


### 2.2. GPT-2

For pre-training details check `pretrain_gpt2.py` in this repository.

```
for VARIANT in 544_2_2_2176_10 128_36_2_512_10 192_2_2_768_10
do
    NEPOCHS=$(echo $VARIANT | cut -d'_' -f 5)
    NWARMUP=$(($NEPOCHS*182))
    python /home/ubuntu/masters_thesis/code/pretrain_gpt2.py \
        --hidden_size $(echo $VARIANT| cut -d'_' -f 1) \
        --num_hidden_layers $(echo $VARIANT| cut -d'_' -f 2) \
        --num_attention_heads $(echo $VARIANT| cut -d'_' -f 3) \
        --intermediate_size $(echo $VARIANT| cut -d'_' -f 4) \
        --num_train_epochs $NEPOCHS \
        --warmup_steps $NWARMUP \
        --output_dir /home/ubuntu/models/gpt2/${VARIANT} \
        --corpus_pretrain /home/ubuntu/data/pretrain_data/wiki_train.txt \
        --token_vocab /home/ubuntu/data/token_vocab/gpt2/
done
```

### 2.3. RoBERTa

For pre-training details check `pretrain_roberta.py` in this repository.

```
for VARIANT in 544_2_2_2176_10 128_36_2_512_10 192_2_2_768_10
do
    NEPOCHS=$(echo $VARIANT | cut -d'_' -f 5)
    NWARMUP=$(($NEPOCHS*182))
    python /home/ubuntu/masters_thesis/code/pretrain_roberta.py \
        --hidden_size $(echo $VARIANT| cut -d'_' -f 1) \
        --num_hidden_layers $(echo $VARIANT| cut -d'_' -f 2) \
        --num_attention_heads $(echo $VARIANT| cut -d'_' -f 3) \
        --intermediate_size $(echo $VARIANT| cut -d'_' -f 4) \
        --num_train_epochs $NEPOCHS \
        --warmup_steps $NWARMUP \
        --output_dir /home/ubuntu/models/robert/${VARIANT} \
        --corpus_pretrain /home/ubuntu/data/pretrain_data/wiki_train.txt \
        --token_vocab /home/ubuntu/data/token_vocab/roberta/
done
```


## 3. Fine-tuning

### 3.1. BERT

#### 3.1.1. GLUE

- Data download: `python utils/download_glue_data.py --data_dir ~/data/glue --tasks all`
- We report accuracy for all tasks execpt for CoLA (MCC), QQP (F1), MRPC (F1) and STS-B (Spearman's Corr)

```
export GLUE_DIR=/home/ubuntu/data/glue
export MODEL=bert
export SEED=2020

for VARIANT in 128_2_2_512_12 128_2_2_512_15 128_2_2_512_17
do
    cp /home/ubuntu/data/token_vocab/$MODEL/vocab.txt /home/ubuntu/models/$MODEL/${VARIANT}/vocab.txt

    for TASK in SST-2 QNLI RTE CoLA WNLI QQP MRPC STS-B MNLI
    do
        python /home/ubuntu/transformers/examples/text-classification/run_glue.py \
            --model_name_or_path /home/ubuntu/models/$MODEL/${VARIANT} \
            --task_name ${TASK} \
            --save_total_limit 1\
            --do_train \
            --do_eval \
            --data_dir $GLUE_DIR/${TASK} \
            --max_seq_length 128 \
            --per_device_train_batch_size=32   \
            --learning_rate 2e-5 \
            --num_train_epochs 3.0 \
            --output_dir /home/ubuntu/fine_tuned/$MODEL/${VARIANT}/glue/${TASK}/ \
            --overwrite_output_dir \
            --seed $SEED
    done
done
```

##### Number of Training Epochs

GLUE tasks                    | 128_2_2_512_10 | 128_2_2_512_12 | 128_2_2_512_15 | 128_2_2_512_17 | 128_2_2_512_20
------------------------------|-----------|-----------------|-----------------|------------------|-----------------
SST-2                         | 77.98     | 77.98           | 79.47           | 80.05           |78.78
QNLI                          | 61.12     | 61.76           | 61.69           | 62.44           |62.51 
RTE                           | 50.54     | 54.87           | 47.29           | 50.90           |54.51
CoLA                          | 0.0       | 0.0             | 0.0             | 0.0             |0.0
WNLI                          | 57.75     | 54.93           | 56.34           | 53.52           |53.52
QQP                           | 63.94     | 63.58           | 64.29           | 64.95           |63.40            
MRPC                          | 81.22     | 81.22           | 81.22           | 81.22           |81.22
STS-B                         | -9.52     | -6.98           | -15.36          | -17.93          |15.8
MNLI                          | 55.04/55.43|54.79/56.19     | 55.46/56.45     | 56.51/57.20     |55.57/56.26
**Average (without WNLI)**    | **47.71** | **48.58**       | **46.88**       | **47.35**       | **51.56**
**Average (with WNLI)**       | **48.83** | **49.28**       | **47.93**       | **48.04**       | **51.77**

##### Number of Hidden Layers

GLUE tasks                    | 128_2_2_512_10 |128_3_2_512_10 | 128_4_2_512_10 | 128_5_2_512_10 |128_6_2_512_10 
------------------------------|-----------|-----------------|-----------------|-------------------|---------------
SST-2                         | 77.98     | 81.31           | 79.93           | 81.89           | 81.65        
QNLI                          | 61.12     | 62.24           | 63.13           | 63.66           | 64.60          
RTE                           | 50.54     | 50.90           | 46.21           | 50.90           | 53.07          
CoLA                          | 0.0       | 0.0             | 0.0             | 0.0             | 0.0           
WNLI                          | 57.75     | 53.52           | 59.15           | 56.34           | 35.21           
QQP                           | 63.94     | 65.84           | 66.48           | 69.21           | 72.47          
MRPC                          | 81.22     | 81.22           | 81.22           | 81.29           | 81.28     
STS-B                         | -9.52     | -5.71           | -11.95          | -10.44          | -13.53     
MNLI                          |55.04/55.43|56.33/57.34      |56.08/57.09      | 57.86/58.49     |63.05/64.52
**Average (without WNLI)**        | **47.71**     | **49.14**           | **47.76**           | **49.38**          | **50.51**
**Average (with WNLI)**           | **48.83**     | **49.63**           | **49.03**           | **50.15**           | **48.81**

##### Number of Attention Heads

GLUE tasks                    | 128_2_2_512_10 |128_2_4_512_10 | 128_2_8_512_10 | 128_2_16_512_10 |128_2_32_512_10 
------------------------------|-----------|-----------------|-----------------|-------------------|---------------
SST-2                         | 77.98     | 77.98           | 77.87           | 77.29           | 76.38        
QNLI                          | 61.12     | 62.15           | 61.69           | 61.08           | 61.93          
RTE                           | 50.54     | 54.15           | 48.73           | 50.90           | 53.43          
CoLA                          | 0.0       | 0.0             | 0.0             | 0.0             | 0.0           
WNLI                          | 57.75     | 54.93           | 47.89           | 54.30           | 57.75           
QQP                           | 63.94     | 64.29           | 65.01           | 64.55           | 65.97          
MRPC                          | 81.22     | 81.22           | 81.22           | 81.22           | 81.22     
STS-B                         | -9.52     | -9.84           | -10.49          | 1.30            | -7.26     
MNLI                          |55.04/55.43|55.20/56.48      |54.46/55.55      |55.54/56.52      |55.26/55.61
**Average (without WNLI)**        | **47.71**     | **48.3**        | **47.45**       | **49.11**| **48.41**
**Average (with WNLI)**           | **48.83**     | **49.04**           | **47.50**           | **49.68**           | **49.45**

##### Hidden Size

GLUE tasks                    | 128_2_2_512_10 |160_2_2_540_10 | 192_2_2_786_10 |288_2_2_1152_10 |384_2_2_1536_10 |
------------------------------|-----------|-----------------|-----------------|-------------------|---------------
SST-2                         | 77.98     | 80.28           | 81.77           | 81.42           | 82.11        
QNLI                          | 61.12     | 61.61           | 61.63           | 64.56           | 66.48          
RTE                           | 50.54     | 59.20           |53.79            | 54.51           | 54.87          
CoLA                          | 0.0       | 0.0             | 0.0             | 0.0             | 5.92           
WNLI                          | 57.75     | 60.56           | 54.93           | 50.70           | 38.03           
QQP                           | 63.94     | 64.51           | 65.40           | 67.25           | 75.83          
MRPC                          | 81.22     | 81.22           | 81.22           | 81.34           | 79.13     
STS-B                         | -9.52     | -10.59          | 8.14            | 6.32            | 10.61
MNLI                          |55.04/55.43|56.00/57.07      | 59.11/60.51     | 61.59/62.48     | 64.28/66.21
**Average (without WNLI)**    | **47.71** | **49.16**       | **51.56**       | **52.24**       | **55.15**
**Average (with WNLI)**       | **48.83**   | **50.43**       | **51.93**       | **52.06**       | **53.24**

##### All Dimensions

GLUE tasks                    | 384_6_6_1536_10 | 384_6_6_1536_20 | 192_3_3_786_10 | 192_3_3_786_20 | 128_2_2_512_10 | 128_2_2_512_20
------------------------------|-----------|-----------------|-----------------|-------------------|---------------|-----------------
SST-2                         | 86.24     | 87.04           | 80.73           | 82.00           | 77.98           |78.78
QNLI                          | 83.12     | 83.85           | 64.14           | 66.37           | 61.12           |62.51 
RTE                           | 55.23     | 55.23           | 51.26           | 53.79           | 50.54           |54.51
CoLA                          | 12.59     | 18.99           | 0.0             | 0.0             | 0.0             |0.0
WNLI                          | 39.44     | 32.39           | 52.11           | 59.15           | 57.75           |53.52
QQP                           | 82.08     | 87.12           | 67.34           | 68.75           | 63.94           |63.40            
MRPC                          | 81.25     | 81.99           | 81.61           | 81.92           | 81.22           |81.22
STS-B                         | 69.40     | 77.47           | 15.11           | 9.2             | -9.52           |-15.8
MNLI                          | 72.76/74.30|73.43/74.95     | 59.76/60.98     | 61.34/62.55     |55.04/55.43      |55.57/56.26
**Average (without WNLI)**    | **68.02** | **70.83**       | **52.65**       | **53.07**       | **47.58**       | **47.57**
**Average (with WNLI)**       | **64.85** | **66.55**       | **52.59**       | **53.75**       | **48.72**       | **48.23**


#### 3.1.2. Language Modeling: Penn Tree Bank (PTB)

- For LM one should use PTB, as the models are already pre-trained on Wikipedia data (so downstream task should not be on Wikipedia); see https://arxiv.org/abs/2005.14165, section 3.1.1
- Unfortunately, PTB is not publicly available (at least not in raw form)
- There exists, however, a public sample of PTB: https://github.com/nlp-compromise/penn-treebank
- We use this sample, extracting only the sentences from the json file and applying a manual train/test split

```
export MODEL=bert
export TRAIN_FILE=/home/ubuntu/data/ptb/ptb_train.txt
export TEST_FILE=/home/ubuntu/data/ptb/ptb_test.txt

for VARIANT in 128_2_2_512_10 128_2_2_512_12 128_2_2_512_15 128_2_2_512_17 128_2_2_512_20 \
128_3_2_512_10 128_4_2_512_10 128_5_2_512_10 128_6_2_512_10 \
128_2_4_512_10 128_2_8_512_10 128_2_16_512_10 128_2_32_512_10 \
160_2_2_540_10 192_2_2_786_10 288_2_2_1152_10 384_2_2_1536_10 \
384_6_6_1536_10 384_6_6_1536_20 192_3_3_786_10 192_3_3_786_20 
do
    cp /home/ubuntu/data/token_vocab/$MODEL/vocab.txt /home/ubuntu/models/$MODEL/${VARIANT}/vocab.txt

    python /home/ubuntu/transformers/examples/language-modeling/run_language_modeling.py \
        --output_dir=/home/ubuntu/fine_tuned/$MODEL/${VARIANT}/language_modeling \
        --model_type=$MODEL \
        --model_name_or_path=/home/ubuntu/models/$MODEL/${VARIANT} \
        --do_train \
        --train_data_file=$TRAIN_FILE \
        --do_eval \
        --eval_data_file=$TEST_FILE \
        --mlm \
        --block_size 128 \
        --num_train_epochs 3.0 \
        --overwrite_output_dir
done
```

#### Number of Training Epochs

Version                      | 128_2_2_512_10 | 128_2_2_512_12 | 128_2_2_512_15 | 128_2_2_512_17 | 128_2_2_512_20
------------------------------|-----------|-----------------|-----------------|------------------|-----------------
Perplexity                    | 112.35     | 103.91         | 87.77           | 88.14           |81.36

#### Number of Hidden Layers

Version                       | 128_2_2_512_10 |128_3_2_512_10 | 128_4_2_512_10 | 128_5_2_512_10 |128_6_2_512_10 
------------------------------|-----------|-----------------|-----------------|-------------------|---------------
Perplexity                    | 112.35     | 92.00           | 82.43           | 71.87           | 67.92   

#### Number of Attention Heads

Version                       | 128_2_2_512_10 |128_2_4_512_10 | 128_2_8_512_10 | 128_2_16_512_10 |128_2_32_512_10 
------------------------------|-----------|-----------------|-----------------|-------------------|---------------
Perplexity                    | 112.35     | 104.65          | 111.20          | 116.02            | 136.83       

#### Hidden Size

Version                       | 128_2_2_512_10 |160_2_2_540_10 | 192_2_2_786_10 |288_2_2_1152_10 |384_2_2_1536_10 |
------------------------------|-----------|-----------------|-----------------|-------------------|---------------
Perplexity                    | 112.35     | 92.16          | 77.38           | 57.05           | 47.26        

#### All Dimensions

Version                       | 384_6_6_1536_10 | 384_6_6_1536_20 | 192_3_3_786_10 | 192_3_3_786_20 | 128_2_2_512_10 | 128_2_2_512_20
------------------------------|-----------|-----------------|-----------------|-------------------|---------------|-----------------
Perplexity                    | 27.60     | 21.70           | 58.92           | 46.92          | 112.35           |81.36


### 3.2. GPT-2

#### 3.2.1 GLUE

Single-sentence tasks (CoLA and SST-2):
```
export TASK=SST-2
for VARIANT in 128_2_2_512_10 192_2_2_786_10 288_2_2_1152_10 384_2_2_1536_10 128_5_2_512_10 128_10_2_512_10 128_18_2_512_10
do
    python /home/ubuntu/python_files/finetune_single_gpt2.py \
        --task $TASK \
        --eval_data /home/ubuntu/data/glue/$TASK/dev.tsv \
        --train_data /home/ubuntu/data/glue/$TASK/train.tsv \
        --batch_size 32 \
        --seed 42 \
        --token_vocab /home/ubuntu/data/token_vocab/gpt2/ \
        --hidden_size $(echo $VARIANT| cut -d'_' -f 1) \
        --model_name_or_path /home/ubuntu/lrz_share/models/gpt2/${VARIANT}/ \
        --num_train_epochs 3 \
        --output_dir /home/ubuntu/lrz_share/fine_tuned/gpt2/glue/${VARIANT}/
done
```

#### 3.2.2 Language Modeling: Penn Tree Bank (PTB)

```
export MODEL=gpt2
export VARIANT=384_6_6
export TRAIN_FILE=/home/ubuntu/data/ptb/ptb_train.txt
export TEST_FILE=/home/ubuntu/data/ptb/ptb_test.txt

for VARIANT in 128_2_2_512_10 160_2_2_540_10 192_2_2_786_10 288_2_2_1152_10 384_2_2_1536_10
do
    cp /home/ubuntu/data/token_vocab/$MODEL/* /home/ubuntu/models/$MODEL/${VARIANT}/

    python /home/ubuntu/transformers/examples/language-modeling/run_language_modeling.py \
        --output_dir=/home/ubuntu/fine_tuned/$MODEL/${VARIANT}/language_modeling \
        --model_type=$MODEL \
        --model_name_or_path=/home/ubuntu/models/$MODEL/${VARIANT} \
        --do_train \
        --train_data_file=$TRAIN_FILE \
        --do_eval \
        --eval_data_file=$TEST_FILE \
        --block_size 128 \
        --save_total_limit 1
done
```

