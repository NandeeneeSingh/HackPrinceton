import json
import torch
import pandas as pd
from datasets import Dataset
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import Trainer, TrainingArguments
from sklearn.model_selection import train_test_split

# Read JSON data into pandas dataframe
with open('data.json', 'r') as f:
    data = json.load(f)

# Convert the list of definitions into a dataframe
definitions = data['definitions']
dataframe = pd.DataFrame(definitions)

# EDA: Check the structure and summary of the dataframe
print(dataframe.info())
print(dataframe.describe())
print(dataframe.head())

# Split data into training and validation sets using pandas
train_df, val_df = train_test_split(dataframe, test_size=0.1)

# Convert dataframes to datasets
trainDS = Dataset.from_pandas(train_df)
valDS = Dataset.from_pandas(val_df)

# Initialize tokenizer
tokenizer = T5Tokenizer.from_pretrained("t5-small")

# Tokenize function
def tokenize_function(examples):
    term = " ".join(examples['term']) if isinstance(examples['term'], list) else examples['term']
    inputTexts = [term for term in examples['term']]
    targetTexts = examples['definition']

    modelInputs = tokenizer(inputTexts, padding="max_length", truncation=True, max_length=128)
    labels = tokenizer(targetTexts, padding="max_length", truncation=True, max_length=128)

    modelInputs['labels'] = labels['input_ids']
    return modelInputs

# Tokenize the training and validation datasets
trainDS = trainDS.map(tokenize_function, batched=True)
valDS = valDS.map(tokenize_function, batched=True)

# Initialize the T5 model
model = T5ForConditionalGeneration.from_pretrained("t5-small")

# Set training arguments
trainingArgs = TrainingArguments(
    output_dir='./results',
    num_train_epochs=10,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10
)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=trainingArgs,
    train_dataset=trainDS,
    eval_dataset=valDS
)

# Train the model
trainer.train()

# Evaluate the model
results = trainer.evaluate()
print(results)
