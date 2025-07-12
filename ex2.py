import re
from langchain_ollama import OllamaLLM 
import time

def clean_text(text, title):
    llm = OllamaLLM(model="llama2")
    prompt = (
        "You are a helpful assistant tasked with cleaning up a scanned or extracted text.\n\n"
        "Please perform the following cleanup operations:\n"
        "1. Remove headers and footers that may repeat across pages.\n"
        "2. Remove any instance of the title below, especially when it appears together with a number or symbol (such as page numbers).\n"
        f"   Title to remove: \"{title}\"\n"
        f"   Example: \"{title} / 23\" or \"{title} - 5\"\n"
        "3. Fix word breaks and unnecessary spaces. For example: 'Con   tent'.\n"
        "4. Preserve the content and flow of the original text. Do not add, invent, or rephrase the meaning.\n\n"
        "**Return ONLY the cleaned text. Do not include any explanations, headings, or formatting.**\n\n"
        "Just return the cleaned text itself in the following format: Clean text: <clean text\n\n> \n\n"
        "This is the text to clean:\n\n"
        f"{text}"
    )

    response = llm.invoke(prompt)
    return response


def dividir_en_frases(texto):
    patron = r'(?<=[.!?])(?:"?)(?=\s|$)'
    frases = re.split(patron, texto)
    frase_comb = ""
    frases_combinadas = []
    for frase in frases:
        if len(frase_comb) > 1000:
            frases_combinadas.append(frase_comb)
            frase_comb = ""
        frase_comb += frase
    for i, f in enumerate(frases_combinadas, 1):
        print(f"Frase combinada {i}: {len(f)}")
    return frases, frases_combinadas

def main():
    start = time.time()
    with open("test_b2b.txt", mode="r", encoding="utf-8") as file:
        texto = file.read()

    frases_limpias = []
    frases, frases_combinadas = dividir_en_frases(texto)
    title = "The B2B Sales Process Handbook"
    print(len(frases), len(frases_combinadas))

    with open("response_ex2.txt", "w", encoding="utf-8") as file:
        for i, f in enumerate(frases_combinadas, 1):
            start_f = time.time()
            cleaned_text = clean_text(f, title).replace("Clean text:","")
            file.write(cleaned_text + "\n")
            print(f"Frase {i}: {cleaned_text}")
            print("Time taken for cleaning:", time.time() - start_f)

    end = time.time()
    print("Total time taken:", end - start)