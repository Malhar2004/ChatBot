from django.shortcuts import render
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
import os
import json
from django.conf import settings

from django.http import JsonResponse
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
import chromadb
from llama_index.llms.groq import Groq

# llm = Groq(model="mixtral-8x7b-32768", api_key="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")

# Define the path to the data directory
DATA_DIR = os.path.join(settings.BASE_DIR, 'data')
# Initialize your query engine and index
documents = SimpleDirectoryReader(DATA_DIR).load_data()

# Initialize Chroma client
db = chromadb.PersistentClient(path="./chroma_db")

# Create collection
chroma_collection = db.get_or_create_collection("quickstart")

# Assign Chroma as the vector_store to the context
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
# Create your index
# now it is loading the index from vector store(chromaDB)
index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)

query_engine = index.as_query_engine()

# # Create your views here.


def chat_view(request):

    return render(request, 'chatbotApp/index.html')


def send_message(request):
    if request.method == 'POST':
        # Load JSON data from request body
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()  # Trim whitespace
        if user_message:
            print("User message:", user_message)
            # Process user's message and generate response
            response = query_engine.query(user_message)     #llm.complete(user_message)
            print("Response:", response)
            if response is not None:
                response_text = response.text.strip()
                response_data = {'response': response_text}
                print(response_data)
            else:
                response_data = {'response': 'Sorry, I didn\'t understand that.'}
        else:
            # Handle empty user message
            response_data = {'response': 'Please provide a message.'}

        return JsonResponse(response_data)


