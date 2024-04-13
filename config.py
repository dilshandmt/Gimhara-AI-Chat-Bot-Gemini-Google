import os
import google.generativeai as genai


def init_genai(model: str):
    genai.configure(api_key=os.environ['API_KEY'])
    model = genai.GenerativeModel(model)
    return model
