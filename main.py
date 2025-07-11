from langchain_ollama import OllamaLLM 
import re


def clean_text(text):
    llm = OllamaLLM(model="llama2")
    prompt = ("Can you clean the following text? By cleanup we mean - when reading a formatted document, it is often found that a header/footer, " \
    "page numbering, etc. is present somewhere in the text. These elements interrupt the logic of the text and " \
    "disrupt the context/semantics. Give the cleaned text between quotation marks\n\n"f"{text}")
    response = llm.invoke(prompt)
    clean_resp = extract_quoted(response)[0]
    return clean_resp

def extract_quoted(texto):
    return re.findall(r'"(.*?)"', texto)

def pre_clean(text):
    return re.sub(r'\s*/\s*\d+\s*', ' ', text)

def divide_text():
    clean_str = ""
    with open("test_b2b.txt", "r", encoding="utf-8") as file:
        text = file.read()

    splitted = text.split(".")
    for item in splitted:
        pre_cleaned_item = pre_clean(item)
        if len(pre_cleaned_item) > 0:  
            try:
                resultado = clean_text(pre_cleaned_item)
                print("Item limpio:", resultado)
                clean_str += str(resultado)
            except Exception as e:
                print("Error al limpiar item:", pre_cleaned_item)
                print("Error:", e)
    with open("response_ex2.txt", "w", encoding="utf-8") as file:
        file.write(clean_str)

def divide_text_with_prompt():
    with open("test_b2b.txt", "r", encoding="utf-8") as file:
        text = file.read()
    llm = OllamaLLM(model="llama2")
    prompt = ("Can you divide the following text into parts of a similar size? You must not break sentences. If a part is too short, you can combine it with the next or the previous one. Make sure that you don't miss any text.\n\n"f"{text}")
    response = llm.invoke(prompt)
    print(response)
    prompt_to_clean = ("Here are some parts of\n\n"f"{text}")


divide_text_with_prompt()


