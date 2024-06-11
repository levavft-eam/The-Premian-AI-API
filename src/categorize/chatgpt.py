from openai import OpenAI
from dotenv import load_dotenv
import os
# import pandas as pd
import logging
import json
import tiktoken
from pathlib import Path
from scipy import spatial

load_dotenv()
CLIENT = OpenAI()

logger = logging.getLogger(__name__)

MODEL_ENCODER_MAP = {
    "gpt-4": "cl100k_base",
    "gpt-3.5-turbo": "cl100k_base",
    "text-embedding-ada-002": "cl100k_base",
    "text-embedding-3-small": "cl100k_base",
    "text-embedding-3-large": "cl100k_base",
    "text-davinci-002": "p50k_base",
    "text-davinci-003": "p50k_base",
}

CATEGORIES = (
    ('엔터테인먼트·예술', 'Entertainment & Arts'),
    ('문학·책', 'Literature & Books'),
    ('영화', 'Movies'),
    ('미술·디자인', 'Fine Arts & Design'),
    ('공연·전시', 'Performing Arts & Exhibitions'),
    ('음악', 'Music'),
    ('드라마', 'Drama'),
    ('스타·연예인', 'Stars & Celebrities'),
    ('만화·애니', 'Comics & Animation'),
    ('방송', 'Broadcasting'),
    ('생활·노하우·쇼핑', 'Lifestyle, Tips & Shopping'),
    ('일상·생각', 'Daily Life & Thoughts'),
    ('육아·결혼', 'Parenting & Marriage'),
    ('반려동물', 'Pets'),
    ('좋은글·이미지', 'Inspirational Writing & Images'),
    ('패션·미용', 'Fashion & Beauty'),
    ('인테리어·DIY', 'Interior Design & DIY'),
    ('요리·레시피', 'Cooking & Recipes'),
    ('상품리뷰', 'Product Reviews'),
    ('원예·재배', 'Gardening & Cultivation'),
    ('취미·여가·여행', 'Hobbies, Leisure & Travel'),
    ('게임', 'Games'),
    ('스포츠', 'Sports'),
    ('사진', 'Photography'),
    ('자동차', 'Automobiles'),
    ('취미', 'Hobbies'),
    ('국내여행', 'Domestic Travel'),
    ('세계여행', 'International Travel'),
    ('맛집', 'Good Eateries/Restaurants'),
    ('지식·동향', 'Knowledge & Trends'),
    ('IT·컴퓨터', 'IT & Computers'),
    ('사회·정치', 'Society & Politics'),
    ('건강·의학', 'Health & Medicine'),
    ('비즈니스·경제', 'Business & Economy'),
    ('어학·외국어', 'Language & Foreign Languages'),
    ('교육·학문', 'Education & Academics')
)

CATEGORIES_KOREAN = "\n".join([c[0] for c in CATEGORIES])

THIS_FOLDER = Path(__file__).parent.resolve()
CATEGORY_EMBEDDINGS_FILE = THIS_FOLDER / '..' / '..' / 'data' / 'embeddings' / 'embeddings.json'


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def truncate_text(text, tokenizer_name="cl100k_base", maximal_token_count=8192):
    token_count = num_tokens_from_string(text, tokenizer_name)

    maximal_tries = 10
    while token_count >= maximal_token_count and maximal_tries > 0:
        rate = token_count / maximal_token_count
        goal_length = max(0, int(len(text) / rate) - 100)
        logger.warn(f"{goal_length=}")
        text = text[:goal_length]
        token_count = num_tokens_from_string(text, tokenizer_name)
        maximal_tries -= 1
    return text


def get_embedding(text, truncate=False):
    model = "text-embedding-3-small"
    tokenizer_name = MODEL_ENCODER_MAP[model]
    maximal_token_count = 8192

    if truncate:
        text = truncate_text(text, tokenizer_name, maximal_token_count)

    client = OpenAI()
    response = client.embeddings.create(
        input=text,
        model=model
    )

    return response.data[0].embedding


def save_category_embeddings():
    embeddings = {category[0]: get_embedding(category[0]) for category in CATEGORIES}
    with open(CATEGORY_EMBEDDINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(embeddings, f, ensure_ascii=False, indent=4)
    return embeddings


def load_category_embeddings():
    if not os.path.isfile(CATEGORY_EMBEDDINGS_FILE):
        return save_category_embeddings()
    with open(CATEGORY_EMBEDDINGS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


CATEGORY_EMBEDDINGS = load_category_embeddings()
CATEGORY_EMBEDDINGS_LOOKUP = tuple((category, embedding) for category, embedding in CATEGORY_EMBEDDINGS.items())
CATEGORY_EMBEDDINGS_KDTREE = spatial.KDTree([pair[1] for pair in CATEGORY_EMBEDDINGS_LOOKUP])


SYSTEM_MESSAGES = (
    "You are a machine that categorizes the text you are given with one word in Korean.",
    "You are a machine that categorizes the text you are given with one word.",
    f"You are a machine that chooses the most fitting category for the text you are given. You choose from this list: "
    f"```{CATEGORIES_KOREAN}```"
    f"and return precisely one element of the list."
)


TEST_STRING = "'기초공사가 중요하듯 피부도 기초가 중요하니 꽃추출물이 함유되어  내 거친 피부를 푸석해진 피부를 촉촉하게 수분충전해줄  아미니의 세컨 브랜드 롤리오  페이셜 토너&에멀전 여름에도 수분 보충은 필수라지요  #롤리오 #보타니컬믹스 #촉촉한에멀전 #촉촉한스킨토너  #기초화장품 #기초스킨케어 #토너추천 #에멀전추천 #수분충전  #뷰티스타그램 #뷰티맘스타그램'"


def get_text_category(user_message, truncate, system_message_index=0):
    model = "gpt-3.5-turbo"
    tokenizer_name = MODEL_ENCODER_MAP[model]
    maximal_token_count = 16385

    if truncate:
        user_message = truncate_text(user_message, tokenizer_name, maximal_token_count)

    system_message = SYSTEM_MESSAGES[system_message_index]
    completion = CLIENT.chat.completions.create(
        model=model,
        messages=[
            {"role": "system",
             "content": system_message},
            {"role": "user",
             "content": user_message}
        ]
    )

    return completion.choices[0].message.content


def get_embedding_based_category(user_message, truncate):
    message_embedding = get_embedding(user_message, truncate)
    closest = CATEGORY_EMBEDDINGS_KDTREE.query(message_embedding)
    logger.info(f"When calculating embeddings, got: {closest=}")
    return CATEGORY_EMBEDDINGS_LOOKUP[closest[1]][0]
