import json
import torch
import pandas as pd
from datasets import Dataset
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import Trainer, TrainingArguments
from sklearn.model_selection import train_test_split

# read JSON data into pandas dataframe
with open('data.json', 'r') as f:
    data = json.load(f)

# convert the list of definitions into a dataframe
definitions = data['definitions']
dataframe = pd.DataFrame(definitions)

# EDA: Check the structure and summary of the dataframe
print(dataframe.info())
print(dataframe.describe())
print(dataframe.head())

# split data into training and validation sets using pandas
train_df, val_df = train_test_split(dataframe, test_size=0.1)

# convert dataframes to datasets
trainDS = Dataset.from_pandas(train_df)
valDS = Dataset.from_pandas(val_df)

# initialize tokenizer
tokenizer = T5Tokenizer.from_pretrained("t5-small")

# tokenize function
def tokenize_function(examples):
    term = " ".join(examples['term']) if isinstance(examples['term'], list) else examples['term']
    inputTexts = [term for term in examples['term']]
    targetTexts = examples['definition']

    modelInputs = tokenizer(inputTexts, padding="max_length", truncation=True, max_length=128)
    labels = tokenizer(targetTexts, padding="max_length", truncation=True, max_length=128)

    modelInputs['labels'] = labels['input_ids']
    return modelInputs

# tokenize the training and validation datasets
trainDS = trainDS.map(tokenize_function, batched=True)
valDS = valDS.map(tokenize_function, batched=True)

# initialize the T5 model
model = T5ForConditionalGeneration.from_pretrained("t5-small")

# set training arguments
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

# initialize the trainer
trainer = Trainer(
    model=model,
    args=trainingArgs,
    train_dataset=trainDS,
    eval_dataset=valDS
)

# Train the model
trainer.train()

# evaluate model
results = trainer.evaluate()
print(results)

# function to generate simplified definitions
def generate_model(terms):
    definitions = []
    for term in terms:
        inputText = f"define: {term}"
        inputID = tokenizer.encode(inputText, return_tensors="pt")

        model.eval()
        with torch.no_grad():
            output = model.generate(inputID, max_length=128)

            predictedDef = tokenizer.decode(output[0], skip_special_tokens=True)
            definitions.append(predictedDef)
    return definitions

# Example of using the model to generate definitions
known_conditions = ["Arthritis"]
simplified_definitions = generate_model(known_conditions)
for condition, definition in zip(known_conditions, simplified_definitions):
    definition = f"Simplified definition of '{condition}': {definition}")
    return definition
