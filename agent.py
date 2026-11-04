from weather_tool import weather
from google import genai
from google.genai import types
from dotenv import load_dotenv
from google.genai import errors

load_dotenv()
import logging
import time

logging.basicConfig(
     filename="agent.log",
     level=logging.INFO,
     format="%(asctime)s - %(levelname)s - %(message)s"          
)

client = genai.Client(
    #http_options=types.HttpOptions(timeout=40000)
)

def calculator(a:float, b:float) -> float:
    """Add two numbers and return the result"""
    print("Calculator tool was called")
    return (a + b)



chat = client.chats.create(
    model="gemini-3.5-flash",
    config=types.GenerateContentConfig(
        tools=[weather, calculator]
    )
)

def run_agent():

    question_count = 0

    while True:
        if question_count >=10:
            print("Question limit reached. Goodbye!")    
            break

        user_question = input("Ask your agent: ")
    
        if user_question.strip() == "" :
            print ("Enter a valid question ")
            continue

        if user_question.lower() == "exit":
                    print("Goodbye!")
                    break

        question_count +=1    

        logging.info("Question number %s received", question_count)

        
        for attempt in range(3):
            try:
                response = chat.send_message(user_question)
                print(response.text)
                break
            
            except errors.APIError as e:
                logging.exception("Gemini request failed")
                  
                #print("Error occured, please try again: ", e) 
            
                if e.code not in (429, 500, 502, 503, 504):
                    print(f"Non-retryable API error ({e.code}): {e}")
                    break

                if attempt==2:
                    print("Request failed after 3 attempts. Please try again later.")
                else:
                    print(f"Temporary API error ({e.code}). Retrying in 2 seconds...")
                    time.sleep(2)
                 

if __name__=="__main__":
    run_agent()    

    



