from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd

load_dotenv()


SYSTEM_MESSAGES = (
    "You are a machine that categorizes the text you are given with one word.",
)
CLIENT = OpenAI()


TEST_STRING = "'기초공사가 중요하듯 피부도 기초가 중요하니 꽃추출물이 함유되어  내 거친 피부를 푸석해진 피부를 촉촉하게 수분충전해줄  아미니의 세컨 브랜드 롤리오  페이셜 토너&에멀전 여름에도 수분 보충은 필수라지요  #롤리오 #보타니컬믹스 #촉촉한에멀전 #촉촉한스킨토너  #기초화장품 #기초스킨케어 #토너추천 #에멀전추천 #수분충전  #뷰티스타그램 #뷰티맘스타그램'"


def get_text_category(user_message, system_message=SYSTEM_MESSAGES[0]):
    completion = CLIENT.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": system_message},
            {"role": "user",
             "content": user_message}
        ]
    )

    return completion.choices[0].message.content


