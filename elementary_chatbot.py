import random

#Dictionary of intents: keywords -> intent -> canned responses
INTENTS = {
    "greet": {
        "keywords": ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"],
        "responses": ["Hello! How can I help you today?", "Hi there, what can I do for you?"]
    },
    "goodbye": {
        "keywords": ["bye", "goodbye", "see you", "farewell"],
        "responses": ["Goodbye! Have a great day.", "See you, feel free to come back with more questions."]
    },
    "thanks": {
        "keywords": ["thanks", "thank you", "thx"],
        "responses": ["You're welcome!", "Happy to help!"]
    },
    "hours": {
        "keywords": ["hours", "open", "opening", "close", "closing"],
        "responses": ["We are open Mon-Fri 9am-5pm.", "Our business hours are Monday to Friday, 9:00–17:00."]
    },
    "pricing": {
        "keywords": ["price", "cost", "pricing", "how much", "plans"],
        "responses": ["Our basic plan starts at Rs.299/month. Would you like details on plans?", "We have several pricing tiers — do you want the summary or a comparison?"]
    },
    "order_status": {
        "keywords": ["order", "status", "tracking", "where is my"],
        "responses": ["Let me check that for you."] 
    },
    "return_policy": {
        "keywords": ["return", "refund", "exchange", "return policy"],
        "responses": ["Our return policy allows returns within 30 days with a receipt.", "You can return unopened items within 30 days for a refund."]
    }
}

#FAQ knowledge base (dictionary-based quick answers)
FAQ = {
    "shipping time": "Standard shipping takes 3-5 business days; express takes 1-2 business days.",
    "support email": "You can reach support@example.com for detailed help.",
    "cancel order": "You can cancel an order within 1 hour from placement via your account orders page."
}

FALLBACK_RESPONSES = [
    "Sorry, I didn't understand that. Can you rephrase?",
    "I'm not sure I follow. Try asking about orders, pricing, returns, or hours."
]


def normalize(text: str) -> str:
    return text.lower().strip()


def match_intent(text: str):
    text_norm = normalize(text)
    for key in FAQ:
        if key in text_norm:
            return "faq", key

    for intent, data in INTENTS.items():
        for kw in data["keywords"]:
            if kw in text_norm:
                return intent, None

    return None, None


def apply_rules(intent: str, extra):
    if intent == "faq":
        return FAQ.get(extra)
    if intent in INTENTS:
        return random.choice(INTENTS[intent]["responses"])
    return random.choice(FALLBACK_RESPONSES)


def get_response(user_input: str) -> str:
    intent, extra = match_intent(user_input)
    if intent is None:
        return random.choice(FALLBACK_RESPONSES)
    return apply_rules(intent, extra)


def repl():
    print("Welcome — simple rule/dictionary-based customer chatbot.")
    print("Type 'exit' or 'quit' to end the chat.\n")
    while True:
        try:
            user = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting chat.")
            break
        if not user:
            continue
        if user.lower() in ("exit", "quit"):
            print("Bot: Goodbye!")
            break
        response = get_response(user)
        print("Bot:", response)


if __name__ == "__main__":
    repl()
