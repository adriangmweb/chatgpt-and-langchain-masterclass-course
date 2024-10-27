from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import argparse

load_dotenv()
parse = argparse.ArgumentParser()
parse.add_argument("--task", type=str, default="return a list of numbers")
parse.add_argument("--language", type=str, default="python")
args = parse.parse_args()

llm = OpenAI()

code_prompt = PromptTemplate(
    template="Write a very short {language} function that will {task}",
    input_variables=["language", "task"],
)

code_chain = LLMChain(
    llm=llm,
    prompt=code_prompt
)

result = code_chain({
    "language": args.language,
    "task": args.task
})

print(result["text"])