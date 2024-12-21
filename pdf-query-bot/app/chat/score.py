import random
from app.chat.redis import client

def random_component_by_score(component_type: str, component_map: dict) -> str:
    """
    This function retrieves the scores for a given component type from the langfuse client.
    The scores are aggregated and used to determine a random component name based on the scores.
    The probability of selecting a component is proportional to its score.

    :param component_type: The type of component for which to select a random component.
    :param component_map: A dictionary mapping component names to their respective build functions.

    :return: The name of the randomly selected component.

    Example Usage:

    random_component_by_score('llm', llm_map)
    """

    if component_type not in ['llm', 'retriever', 'memory']:
        raise ValueError("Invalid component type")
    
    score_values = client.hgetall(f"{component_type}_score_values")
    score_counts = client.hgetall(f"{component_type}_score_counts")
    
    component_names = component_map.keys()
    average_scores = {}
    for name in component_names:
        score = int(score_values.get(name, 1))
        count = int(score_counts.get(name, 1))
        average = score / count
        average_scores[name] = max(average, 0.1)
        
    print(average_scores)
        
    # Weighted random selection
    sum_scores = sum(average_scores.values())
    random_value = random.uniform(0, sum_scores)
    cumulative = 0
    for name, score in average_scores.items():
        cumulative += score
        if cumulative >= random_value:
            return name

def score_conversation(
    conversation_id: str, score: float, llm: str, retriever: str, memory: str
) -> None:
    """
    This function interfaces with langfuse to assign a score to a conversation, specified by its ID.
    It creates a new langfuse score utilizing the provided llm, retriever, and memory components.
    The details are encapsulated in JSON format and submitted along with the conversation_id and the score.

    :param conversation_id: The unique identifier for the conversation to be scored.
    :param score: The score assigned to the conversation.
    :param llm: The Language Model component information.
    :param retriever: The Retriever component information.
    :param memory: The Memory component information.

    Example Usage:

    score_conversation('abc123', 0.75, 'llm_info', 'retriever_info', 'memory_info')
    """

    score = min(max(score, 0), 1)
    
    client.hincrby("llm_score_values", llm, score)
    client.hincrby("llm_score_counts", llm, 1)
    
    client.hincrby("retriever_score_values", retriever, score)
    client.hincrby("retriever_score_counts", retriever, 1)
    
    client.hincrby("memory_score_values", memory, score)
    client.hincrby("memory_score_counts", memory, 1)


def get_scores():
    """
    Retrieves and organizes scores from the langfuse client for different component types and names.
    The scores are categorized and aggregated in a nested dictionary format where the outer key represents
    the component type and the inner key represents the component name, with each score listed in an array.

    The function accesses the langfuse client's score endpoint to obtain scores.
    If the score name cannot be parsed into JSON, it is skipped.

    :return: A dictionary organized by component type and name, containing arrays of scores.

    Example:

        {
            'llm': {
                'chatopenai-3.5-turbo': [score1, score2],
                'chatopenai-4': [score3, score4]
            },
            'retriever': { 'pinecone_store': [score5, score6] },
            'memory': { 'persist_memory': [score7, score8] }
        }
    """

    pass
