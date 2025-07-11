from langchain_ollama import OllamaLLM
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

# 1. Instancia del modelo local
llm = OllamaLLM(model="mistral")

# 2. Prompt personalizado: la IA actúa como cliente escéptico
prompt = PromptTemplate.from_template("""
You are acting as a skeptical customer who is considering buying a product.
You should:
- Ask specific questions about the product.
- Express doubts and hesitation.
- Only buy if you are fully convinced.
- If you are not convinced, say clearly why.

Previous conversation:
{history}
Seller: {input}
Customer:
""")

# 3. Memoria de conversación
memory = ConversationBufferMemory(return_messages=True)

# 4. Cadena de conversación con memoria y prompt personalizado
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=prompt,
    verbose=False
)

# 5. Función principal
def iniciar_conversacion():
    introduccion = (
        "You are a customer who is considering buying a product. "
        "I am the seller and I will try to convince you. You must ask me questions, "
        "and you should only buy if I give you good enough reasons."
    )
    conversation.invoke(introduccion)
    while True:
        pregunta = input("\nSeller: ")
        if pregunta.lower() == "bye":
            print("\nCustomer: Goodbye!")
            break
        respuesta = conversation.run(pregunta)
        print("\nCustomer:", respuesta)

        

iniciar_conversacion()

