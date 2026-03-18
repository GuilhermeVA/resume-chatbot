from openai import OpenAI
from dotenv import load_dotenv
import os
from pypdf import PdfReader






# Configurando chave API
load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key:
    print(f'A chave API está configurada e pronta. A chave começa com {openai_api_key[:5]}')
else:
    print(f'A chave API não está configurada')


openai = OpenAI()


#Lendo meu curriculo
meu_curriculo = 'documentos/meu_curriculo.pdf'

reader = PdfReader(meu_curriculo)
texto_curriculo = ""

for page in reader.pages:
    text = page.extract_text()
    if text:
        texto_curriculo += text


#Lendo meu resumo pessoal
meu_resumo = "documentos/meu_resumo.txt"
with open(meu_resumo, 'r') as arquivo:
    texto_resumo = arquivo.read()



#Criando o System Prompt
meu_nome = "Guilherme Vallim Araujo"
system_prompt = f"Você está agindo como {meu_nome} em seu site pessoal. Seu principal objetivo é responder perguntas relacionadas ao\
 {meu_nome}, em especial sobre sua carreira profissional, habilidades e experiências. Sua responsabilidade é representar {meu_nome}\
 em seu site da forma mais fiel possível. Você tem acesso à um breve resumo pessoal e o currículo de {meu_nome} que você deve usar\
 para responder as perguntas. Seja profissional e empolgado, imaginando que está falando com um possível cliente ou recrutador.\
 Se você não souber a resposta para alguma pergunta, diga que não sabe. \n"

#Adicionando o currículo e o resumo ao prompt
system_prompt += f"\n\n# Resumo Pessoal: {texto_resumo}"
system_prompt += f"\n\n# Currículo: {texto_curriculo}"



#User Prompt
user_prompt = input(f"Pergunte algo sobre {meu_nome}")


#Agrupando os prompts para a IA
message = [{"role" :"system", "content":system_prompt}] + [{"role":"user", "content":user_prompt}]


#Chamando a IA
resposta_completa = openai.chat.completions.create(model="gpt-5-nano",messages=message)
resposta = resposta_completa.choices[0].message.content

print(resposta)
