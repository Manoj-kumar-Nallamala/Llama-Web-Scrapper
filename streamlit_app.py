# -*- coding: utf-8 -*-
"""streamlit_app.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1e2OdTMV6LjPfU-4jALCuEzIDfSmf8By-
"""



import streamlit as st
from sentence_transformers import SentenceTransformer, util
import numpy as np
sentences = [
    "The sun sets over the hills.",
    "A gentle breeze rustles the leaves.",
    "The city lights flicker as night falls.",
    "A cat sleeps peacefully on the windowsill.",
    "Waves gently lap against the shore."
]

# Load the model
from sentence_transformers import SentenceTransformer
import torch

# Initialize the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Embed the sentences
embeddings = model.encode(sentences, convert_to_tensor=True)

# Save the embeddings
torch.save(embeddings, 'sentence_embeddings.pt')

# Load the precomputed embeddings for later use
loaded_embeddings = torch.load('sentence_embeddings.pt')


def find_most_similar(input_sentence, sentence_embeddings, top_k=1):
    input_embedding = model.encode(input_sentence, convert_to_tensor=True)
    cos_scores = util.pytorch_cos_sim(input_embedding, sentence_embeddings)[0]
    top_results = np.argpartition(-cos_scores, range(top_k))[0:top_k]

    similar_sentences = [(sentences[idx], cos_scores[idx].item()) for idx in top_results]
    return similar_sentences

# Streamlit interface
st.title("Sentence Similarity Finder")

user_input = st.text_input("Enter a sentence")

if user_input:
    similar_sentences = find_most_similar(user_input, loaded_embeddings, top_k=5)
    for sentence, score in similar_sentences:
        st.write(f"Sentence: {sentence}")
        st.write(f"Similarity Score: {score}")



