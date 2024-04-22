# Summarizing the given text using the given models

from transformers import pipeline
from Globals import *
from transformers import AutoTokenizer, AutoModelForCausalLM

# Defining the summarizers for the respective models
bart_summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
flan_t5_summarizer = pipeline("summarization", model="google/flan-t5-base")

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf", use_auth_token=hg_token)
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-hf", use_auth_token=hg_token)


# Function to get the summary using LLama
def get_summary_llama(text):
    query = f"""Summarize the following text: {text}"""
    print(f"Query:\n{query}")
    # Tokenizing  the input
    input_ids = tokenizer.encode(query, return_tensors='pt')
    print("input_ids done")
    # Generate the summary using the model
    summary_ids = model.generate(input_ids, max_new_tokens = 50)
    print("summary_ids done")
    # Decode the generated summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary



# Function to get the summary of a very long text by dividing it into chunks and then processing it.
def summarize_long_text(text, max_length=1024, min_length=50, model="bart"):
    if model == "llama_2":
        summary = get_summary_llama(text)
        return summary

    elif model == "flan_t5":
        summarizer = flan_t5_summarizer
    else:
        summarizer = summarizer = bart_summarizer

    chunks = [text[i : i + max_length] for i in range(0, len(text), max_length)]
    summaries = []

    for chunk in chunks:
        summary = summarizer(chunk, max_length = max_length, max_new_tokens=50, min_length=min_length, do_sample=True)[0]['summary_text']
        summaries.append(summary)

    combined_summary = ' '.join(summaries)
    return combined_summary


# Wrapper function that calls the summarize_text function
def summarize_file(input = text_file_path, model="bart"):
    with open(input, "r") as f:
        text = f.read()
    summary = summarize_long_text(text=text, model=model)
    return summary


