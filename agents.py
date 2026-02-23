#agentların promptları burada girili 
from ollama_client import ask_llm
import time 
import datetime 

# --- LOGLAMA MEKANİZMASI ---
def logger_decorator(func):
    def wrapper(*args, **kwargs):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{'='*20}")
        print(f"[BAŞLADI] Agent: {func.__name__}")
        print(f"[ZAMAN]   {current_time}")
        print(f"{'='*20}")
        
        start_perf = time.perf_counter()
        result = func(*args, **kwargs) # Fonksiyonun kendisi çalışıyor
        end_perf = time.perf_counter()
        
        finished_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{'-'*20}")
        print(f"[BİTTİ]   Agent: {func.__name__}")
        print(f"[TAMAMLANDI] {finished_time}")
        print(f"[SÜRE]    {end_perf - start_perf:.2f} saniye")
        print(f"{'-'*20}\n")
        
        return result
    return wrapper


@logger_decorator
#reader agent #1
def reader_agent(email_text):
    prompt = f"""
You are an email preprocessor.

The input email is ALWAYS in English.
Do NOT detect language.
Do NOT translate anything.

Extract the core message of the email.
Remove signatures and repeated text.

Return result in this format:

CLEANED: <cleaned email>

Email:
{email_text}

Return only the cleaned message.
"""
    return ask_llm(prompt)

@logger_decorator
#classification agent #2
def classifier_agent(cleaned_email):
    prompt = f"""
You are an email classification system.

The email is guaranteed to be in English.

Classify the email into ONLY ONE of:
Complaint
Inquiry
Sales
Support
Spam

Return only the category name.

Email:
{cleaned_email}
"""
    return ask_llm(prompt)

@logger_decorator
#response agent #3
def response_agent(category, email_text, metadata):
    customer_name = metadata.get("username", "Dear Customer")
    order_id = metadata.get("order_no", "Unknown_Order_No")
    
    prompt = f"""
You are a professional customer support assistant.

IMPORTANT RULES:
- The email is ALWAYS in English.
- You MUST respond ONLY in English.
- Never use any other language.

Customer Name: {customer_name}
Order Number: {order_id}
Category: {category}

Email Content:
{email_text}

Write a professional reply.
- Address the customer as {customer_name}.
- Mention the order number {order_id}.
- Keep the tone professional.
"""
    return ask_llm(prompt)

@logger_decorator
#control agent #4
def critic_agent(response_text):
    prompt = f"""
You are a quality control assistant.
Evaluate this email response. 

You are a quality control assistant.

The response MUST be in English.

If it is professional and correct, start with:
APPROVED

If it needs changes, start with:
REVISE

Response:

{response_text}
"""
    return ask_llm(prompt)
