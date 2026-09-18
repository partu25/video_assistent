import os
import time
from langchain_mistralai import ChatMistralAI


def get_llm(temperature: float = 0.2):
    model = os.getenv("MISTRAL_MODEL", "open-mistral-7b").strip()
    api_key = os.getenv("MISTRAL_API_KEY", "").strip()
    return ChatMistralAI(
        model=model,
        mistral_api_key=api_key,
        temperature=temperature,
        max_retries=5,
    )


def invoke_with_retry(target_chain, input_data, max_retries: int = 5, initial_delay: float = 2.0):
    """
    Invoke a LangChain runnable or LLM with exponential backoff retries 
    when encountering 429 Rate Limit Exceeded errors.
    """
    current_delay = initial_delay
    for attempt in range(1, max_retries + 1):
        try:
            return target_chain.invoke(input_data)
        except Exception as e:
            err_str = str(e).lower()
            if ("429" in err_str or "rate limit" in err_str) and attempt < max_retries:
                print(f"⚠️ Mistral Rate Limit hit (429). Retrying in {current_delay:.1f}s (Attempt {attempt}/{max_retries})...")
                time.sleep(current_delay)
                current_delay *= 2
            else:
                raise
