from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import asyncio
from google import genai

from concurrent.futures import TimeoutError
from functools import partial

# Load environment variables from .env file
load_dotenv()

# Access your API key and initialize Gemini client correctly
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

class MemoryPod(BaseModel):
    """
    MemoryPod is a class that represents a memory  in the system.
    
    """
    fact : str = Field(..., description="A fact that is stored in the memory.")
    importance: float = Field(..., description="A measure of how important the fact is.")
    source: str = Field(..., description="The source of the fact.")

read_memory = [MemoryPod(
                            fact="its raining.",
                            importance=0.9,
                            source="Wikipedia"),MemoryPod(
                            fact="we are planning to go to the beach on a bright day",
                            importance=0.8,
                            source="Wikipedia"),MemoryPod(
                            fact="looks like this august is rainy and september will be better",
                            importance=0.7,
                            source="Wikipedia")]

facts = [fact.fact for fact in read_memory]
print(facts)
print("\n############## important facts ################\n")

user_inputs = " ".join(facts)
query  = "when can you book us the tickets for the beach trip"

def call_llm(prompt: str) -> None:
    response = client.models.generate_content(
                             model="gemini-2.0-flash",
                             contents=prompt)
    return (response.text)
print("\n##############################\n")


def extract_facts(user_inputs):
    """ extract important facts from the user inputs """
    prompt = F"""extract the important facts from {user_inputs}  """
    return call_llm(prompt)
print(extract_facts(user_inputs))
factors =[]
factors.append(extract_facts(user_inputs))

print("\n#############  travel agent reply  #################\n")


def get_next_step(query):
    """ get the next step based on the user inputs """
    prompt = f""" you are a helpful travel assistant. you are given context as below:
                  context : {factors}
                  read the context and decide what best possible answer you can give to the user
                  for the below query.
                    query: {query}
                 
             
               answer: """
    return call_llm(prompt)




print("\n##############################\n")
print(get_next_step(user_inputs))
print("\n##############################\n")