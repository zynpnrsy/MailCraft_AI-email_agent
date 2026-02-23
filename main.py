# en başta temeli test etmek için oluşturuldu 
from agents import classifier_agent, reader_agent, response_agent, critic_agent

def run_email_agent(email_text):
    print("\n--- Reader Agent ---")
    cleaned = reader_agent(email_text)
    print(cleaned)

    print("\n--- Classifier Agent ---")
    category = classifier_agent(cleaned)
    print(category)

    print("\n--- Response Agent ---")
    response = response_agent(category, cleaned)
    print(response)

    print("\n--- Critic Agent ---")
    review = critic_agent(response)
    print(review)

    return {
        "cleaned": cleaned,
        "category": category,
        "response": response,
        "review": review
    }


if __name__ == "__main__":
    email_input = input("Paste the email:\n")
    run_email_agent(email_input)
        