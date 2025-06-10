import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hello, i am piyush"
tokens = enc.encode(text)

print(tokens)

tokens = [13225, 11, 575, 939, 173566, 1776]

decoded = enc.decode(tokens)
print("Decoded: ", decoded)
