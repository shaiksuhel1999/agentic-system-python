from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("<model_name_here>")

text = """<text-here>"""
tokens = tokenizer.tokenize(text)
print(tokens)

input_ids = tokenizer.encode(text)

print(len(input_ids))