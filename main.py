from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel
from typing import Literal
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("API_KEY")

#different languages to test on
test_esp = "¡Hola! La aplicación se cierra sola cada vez que intento exportar mi archivo PDF en Android. Esto me está costando clientes."
test_fra = "Votre service client est incroyable. Mon problème de facturation a été résolu en 5 minutes. Merci à toute l'équipe"
test_dut = "Ik kan niet inloggen op mijn account. Telkens als ik mijn wachtwoord invul, krijg ik een 404-foutmelding. Help alstublieft, ik heb dit vandaag nodig voor mijn werk!"
test_jap = "昨日サブスクリプションをキャンセルしたのに、今日また50ドル課金されています。すぐに返金してください。"
test_ger = "Die App ist toll, aber es wäre super, wenn es einen Dark Mode gäbe. Meine Augen tun abends weh, wenn ich am Bildschirm arbeite"
test_por = "O aplicativo mudou minha vida! É muito fácil de usar e o design é lindo. Parabéns aos desenvolvedores."

# structure of data the llm will recieve
class FeedbackAnalysis(BaseModel):
    language:str
    sentiment: Literal["Positive","Negative","Neutral"] = "Neutral"
    requires_followup:bool
    english_summary:str

# how the llm will act and how the user data is recieved
prompt = ChatPromptTemplate([
    ("system","Analyze the user feedback and retrieve the answer/summary of the feedback the language and the sentiment"),
    ("user","the feedback {og_feedback}")
    ])

# Gemini LLM that we send our prompt to
llm = ChatGoogleGenerativeAI(
    temperature=0.4,
    google_api_key=API_KEY,
    model="gemini-3.5-flash-lite"
)

#The Outpt formatting of the response email
parser = StrOutputParser()


#This for reading and classifying emails/different messages
structured_llm= llm.with_structured_output(FeedbackAnalysis)

chain = prompt | structured_llm

result =chain.invoke({"og_feedback":{test_por}})


def summary_analysis(result):

    #  Format of text

    print("\n")
    print("Summary:")
    print("email_summary: "+result.english_summary+"\n"+"Language: "+result.language+"\n"+"Sentiment: "+result.sentiment)
    print("Followup ?: ",result.requires_followup)


    # response message logic

    if result.requires_followup == True:
        response_prompt = ChatPromptTemplate([
            ("system","Generate a polite apology about the user feedback in their native language {language}"),
            ("user","User feedback {og_feedback}")
        ])

        respond_chain = response_prompt|llm|parser
        respond_text = respond_chain.invoke({"og_feedback":{test_por},
                                            "language": result.language})
        print(respond_text)
    else:
        print("No action needed")
        
try:
    summary_analysis(result)
except Exception as e:
    print(f"{e}")