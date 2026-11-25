import os
import time


def get_llm(temperature: float = 0.2):
    groq_api_key = os.getenv("GROQ_API_KEY", "").strip()
    if groq_api_key:
        from langchain_groq import ChatGroq
        model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile").strip()
        return ChatGroq(
            model=model,
            api_key=groq_api_key,
            temperature=temperature,
            max_retries=5,
        )

    # Fallback to Mistral AI if GROQ_API_KEY is not configured
    from langchain_mistralai import ChatMistralAI
    model = os.getenv("MISTRAL_MODEL", "open-mistral-7b").strip()
    api_key = os.getenv("MISTRAL_API_KEY", "").strip()
    return ChatMistralAI(
        model=model,
        mistral_api_key=api_key,
        temperature=temperature,
        max_retries=2,
    )


def invoke_with_retry(target_chain, input_data, max_retries: int = 4, initial_delay: float = 5.0):
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
            if ("429" in err_str or "rate limit" in err_str or "rate_limited" in err_str) and attempt < max_retries:
                print(f"⚠️ Rate Limit hit (429). Waiting {current_delay:.1f}s before retry (Attempt {attempt}/{max_retries})...")
                time.sleep(current_delay)
                current_delay *= 2
            else:
                raise
