import random
from langchain.chat_models import ChatOpenAI
from app.chat.models import ChatArgs
from app.chat.vector_stores import retriever_map
from app.chat.llms import llm_map
from app.chat.memory import memory_map
from app.chat.chains.retrieval import StreamingConversationalRetrievalChain
from app.web.api import (
    set_conversation_components,
    get_conversation_components
)
from app.chat.score import random_component_by_score

def select_component(
    component_type,
    component_map,
    chat_args
):
    components = get_conversation_components(chat_args.conversation_id)
    previous_component = components[component_type]
    
    if previous_component:
        # this is not the first message in the conversation
        # so we can reuse the same component!
        build_component = component_map[previous_component]
        return previous_component, build_component(chat_args)
    else:
        # this is the first message in the conversation
        # so we need to pick a random component to use
        random_component_name = random_component_by_score(component_type, component_map)
        build_component = component_map[random_component_name]
        component = build_component(chat_args)
        set_conversation_components(
            chat_args.conversation_id,
            llm="",
            retriever=random_component_name,
            memory="",
        )
        return random_component_name, component

def build_chat(chat_args: ChatArgs):
    """
    :param chat_args: ChatArgs object containing
        conversation_id, pdf_id, metadata, and streaming flag.

    :return: A chain

    Example Usage:

        chain = build_chat(chat_args)
    """

    retriever_name, retriever = select_component(
        "retriever",
        retriever_map,
        chat_args
    )
    
    llm_name, llm = select_component(
        "llm",
        llm_map,
        chat_args
    )
    
    memory_name, memory = select_component(
        "memory",
        memory_map,
        chat_args
    )
    
    print(f"Using components: llm={llm_name}, retriever={retriever_name}, memory={memory_name}")
    
    set_conversation_components(
        chat_args.conversation_id,
        llm=llm_name,
        retriever=retriever_name,
        memory=memory_name,
    )
        
    condense_question_llm = ChatOpenAI(streaming=False)
    
    return StreamingConversationalRetrievalChain.from_llm(
        llm=llm,
        condense_question_llm=condense_question_llm,
        memory=memory,
        retriever=retriever
    )
