from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
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

test_prompt = PromptTemplate(
    template="Write a unit test for the following {language} code:\n{code}",
    input_variables=["language", "code"]
)

code_chain = LLMChain(
    llm=llm,
    prompt=code_prompt,
    output_key="code"
)

test_chain = LLMChain(
    llm=llm,
    prompt=test_prompt,
    output_key="test"
)

chain = SequentialChain(
    chains=[code_chain, test_chain],
    input_variables=["language", "task"],
    output_variables=["code", "test"]
)

result = chain({
    "language": args.language,
    "task": args.task
})

print(">>>> GENERATED CODE:")
print(result["code"])

print(">>>> GENERATED TEST:")
print(result["test"])