import logging
import json
import re
from datetime import datetime, timedelta

from src.stt.whisper import load_pipeline
from src.stt.open_ai import stt as open_ai_stt
from src.download.dlp import download_video
from src.metadata.google_api import get_video_statistics, get_channel_statistics, get_channel_details
from src.categorize.chatgpt import get_text_category, get_embedding_based_category

logger = logging.getLogger(__name__)

TRANSCRIPT = """핸드폰 요금 왜 이렇게 많이 나와 이거? 그래서 알뜰폰으로 바꿨다. 안녕하세요. 잇섭입니다. 오랜만에 정보성 컨텐츠 어쩌면 핸드폰을 저렴하게 쓰는 방법일 수도 있는 많은 분들 그리고 실제로 제 주변 지인분들도 저한테 엄청 많이 묻는 자급제, 통신사, 스마트폰 구입에 관한 정리를 한번 해보려고 합니다. 일반적으로 통신사 구입은 아주 오래전부터 구입을 해왔기 때문에 뭐 크게 어려움 없이 우리에게 익숙하지만 테크층이라면 자급제를 많이 알고 있는데 일반적으로 자급제라는 용어로 들으면 많이 생소하긴 하죠. 자 그럼 자급제라는 말을 많이 쓰고 있거든요? 이것도 갤럭시는 S9부터 유행하기 시작했고 아이폰은 비교적 자급제가 오래전부터 얼락이라는 이름으로 많이 판매되기 시작했습니다. 그럼 여기서 제가 몇 년간 많이 들었던 질문에 대한 답을 한번 하고 제 친구들도 자급제는 이제 그나마 조금 익숙해졌는데 그것을 구입해서 통신사에 가야 되냐고 많이 물어보더라고요. 전혀 아닙니다. 사실 우리가 핸드폰을 쓰기 위해서는 통신을 하기 위한 통신사가 가장 위에 있다고 보면 그 밑에 핸드폰 단말을 구입하는데 통신사, 자급제로 구입했기 때문에 아무런 조건이 없이 그냥 공기계인 상태입니다. 이럴 때 그냥 유심만 빼고 트레이에 넣은 다음에 그냥 이렇게 넣으면 아... 처음에는 이렇게 안테나가 왔다 갔다 하긴 하지만 정상적으로 개통이 되진 않습니다. 그럼 여기서 많은 판매자분들이 하는 말이 있어요. 핸드폰을 두세 번 껐다 켜라. 그러면 개통이 된다. 근데 여기서도 꿀팁! 굳이 핸드폰을 끌 필요 없이 비행기 모드로 한 번 했다가 다시 풀고 이제 아까와 다르게 검색 중이라고 나오면서 KT-LT라고 썼잖아요? 개통이 되을 볼 수 있습니다. 두 번째, 통신사에서 구입하면 이것저것 여러 가지 할인 혜택이 많은데 그럼 자급제로 사면 손해가 아닌가? 결론적으로 이야기하자면 크게 차이가 없다고 봐도 무방합니다. 요금을 25% 할 할인을 받을 수 있어요. 다만 통신사에서 구입할 때 공시지원금이라는 게 있긴 한데 경우에 따라 이것을 받으면 조금 더 저렴한 경우가 있기는 해요. 다음은 새폰이 아닌 중고로 아무 폰이나 사도 자급제가 가능한가요? 기본적으로 가능하지만 체크해야 할 부분이 몇 가지 있습니다. 이것은 뒤에서 좀 더 자 자세하게 이야기를 해드릴게요. 자급제폰이랑 통신사폰이랑 디자인이나 성능이나 여러 가지 통신 품질에 대한 차이가 있나? 크게 보자면 이것도 차이가 없다고 무방합니다. 그나마 차이가 있다면 처음에 핸드폰을 켰을 때 부팅 로고 아니면 기본적으로 먼저 탑재되어 있는 통신사 앱 이러한 정도만 차이가 있지 사실상 거의 차이가 없다고 봐도 무방해요. 알뜰폰 그냥 일반적으로 통신사에서 번호이동을 하는 것과 동일하다고 생각하면 됩니다. 그럼 자급제폰은 어디서 구입하나요? 이것은 온라인이나 오프라인 모두 구입 가능하고 최근에 LG 베스트샵도 아이폰을 판다고 하죠? 하지만 제가 물어보니까 베스트샵에서 아이폰을 팔긴 하지만 통신사 개통 전용으로만 팔고 자급제는 따로 판매하지 않는다고 해요. 그럼 장점은 무엇일까? 첫 번째 장점은 통신사의 제약이 전혀 없다는 점이에요. 통신사에서 구입한다면 SK, KT, LG U Plus형 단말기가 따로 있지만 자급제는 한 기기를 구입해서 내가 원하는 통신사를 마음대로 사용할 수 있습니다. 게다가 통신요금도 내 마음대로 쓸 수 있는 거죠. 두 번째는 약정이 없다는 점이에요. 이게 생각보다 굉장히 강력한 장점이죠 약정하게 된다면 24개월을 하게 되는데 그중에서 내가 중고로 팔고 돈을 조금 더 추가해서 새로운 스마트폰으로 바꾸고 싶을 때 그때 약정에 아무 상관없이 갈아탈 수 있다는 장점이 있습니다. 세 번째는 대리점에 가서 폰 판매자분과 크게 실랑이를 하지 않아도 된다는 장점이 있습니다. 왜냐면 그냥 기기 자체만 구입하면 되니까 처음에 켰을 때 SK 전용 여러 가지 앱들이 설치되어 있는데 자급제는 그런 거 하나도 없이 엄청 깔끔하죠? 그리고 출고가 기준으로 따지고 보자면 통신사에서 구입하는 것보다 조금 더 저렴하게 구입할 수 있습니다. 통신사에서 할부를 하게 되면 무조건 5.9%의 할부 이자가 붙게 됩니다 것이죠. 물론 통신사에 구입하면 24개월 할부를 할 수 있기는 하지만 요즘은 자급제도 카드를 사용하게 된다면 일정 금액 이상 조건에 따라 무이자가 가능하고 최대 24개월까지 가능하긴 하지만 물론 이거는 카드사마다 여러 가지 판매 페이지마다 다르기 때문에 한번 체크해보시는 것을 추천드릴게요. 그러니까 여기서부터 59,000원으로 먹고 들어가는 거죠. 아이폰 13의 경우 대략 한 8%에서 12% 정도 더 저렴하게 구입할 수 있습니다. 통신사는 단통법 때문에 출고가에서 할인을 해줄 수가 없어요. 그럼 저처럼 자급제로 구입하는 게 아니라 통신사에서 핸드폰을 구입했을 때의 장점은 무엇이 있을까? 뭐 귀찮은 걸 싫어하면 구입과 개통을 한 번에 할 수 있다는 장점이 있습니다. 근데 이것도 애 자급제를 구입해도 60만원 가량 끼우면 되기 때문에 오히려 자급제가 더 간편할지도? 그리고 가끔 선택약정이 아닌 공시지원금이 굉장히 많이 나온다면 자급제에 알트폰을 쓰는 것보다 훨씬 더 저렴하게 구입할 수 있는 경우가 종종 있습니다. 여기서도 핸드폰을 구입할 때 약정 할인받을 수 있는 게 크게 두 종류가 있거든요. 첫 번째는 요금 자체의 할인을 받는 공시지원금이 있습니다. 이거는 경우에 따라 다르지만 처음에 구입할 때 좀 고가의 기기와 고가의 요금제를 쓴다면 이 선택약정이 대부분 유리한 경우가 많죠. 그리고 흔히 말하는 성지, 불법 보존을 받는다면 자급제, 알드폰을 구입하는 것보다 훨씬 더 저�말기를 구입했을 때의 단점! 일단 대리점 직원과 싸우는 경우가 굉장히 많아요. 대부분 보면 제 주변에서 대리점에 가서 기분 좋게 구입했다는 후기를 크게 들을 수가 없더라고요. 얼마 전에 꽈뚜룹님이 저한테 전화와서 그... 거의 강매를 하려고 막 했다고 출국가 자체의 개통을 하더라도 뭐 할� 또 높은 요금제를 얼마나 써야 되고 이렇게 거의 강매를 하는 경우가 대부분 많습니다. 약장이나 이런 게 막 엄청 많기 때문에 핸드폰을 잘 모른다면 사실 이게 그냥 혜택인 줄 알고 그냥 하거든요. 그리고 앞서 말했다시피 비싼 할부이자 36개월 할부를 해놓고 2년 뒤에 오면 위약금 없이 새로운 핸드폰으로 교체해준다고 하지만 그때 되면 대리점이 없어지거나 나는 모르는데요? 경우도 굉장히 많습니다. 그리고 5G 강요! 이것은 엄청 많이 들어봐서 이제는 익숙할 거예요. 통신사에서 요즘 5G를 지원하는 기기를 산다면 무조건 5G 요금제로 개통하는 것으로 알고 있거든요? 이것도 사실 소비자에게 선택권을 줘야 되는 거 아니에요? 5G를 지원하는 단말기라고 하더라도 4G를 그대로 쓸 수 있는데 무조건 5G로만 강요한다니 5G가 요즘에는 그나마 속도 자체는 빠르지만 4G, LTE로 쓰더라도 크게 속도에 대한 답답함이 없습니다. 거기다가 더해지는 요금제를 4개월에서 6개월 동안 써야 한다는 단점! 사실 이게 공식은 아니거든요? 공식 판매 홈페이지에 들어가 보면 요금제를 자유롭게 쓸 수 있는데 대부분 대리점에서는 수익을 크게 남기기 위해 고가의 요금제를 4개월, 6개월 이렇게 오� 그리고 또 앞서 말했다시피 성지 성지 많은 이야기를 하는데 오히려 이것을 잘 모르고 갔다면 오히려 눈탱이 맞고 돌아오는 경우도 굉장히 많더라고요. 추가로 통신사의 정식 계약서가 아닌 위와 같은 계약서는 이명 계약서라고 하는데 이것은 법적 효력도 없고 통신사에서 지켜주지 않으니까 그곳에서는 절대 개통하지 않는 것을 추천드립니다. 이러한 부분들을 모두 정리해봤을 결국 요즘에 크게 뜨고 있는 것은 자급제의 알뜰폰 조합으로 쓰는 게 요즘 많은 젊은 층에서 토노되고 있습니다. 이게 왜 이럴까 제가 한번 생각을 해봤거든요? 사실상 통신사 예전에는 멤버십 혜택이나 여러 가지 많았지만 요즘에는 거의... 없어지다시피 하고 이제는 메이저 통신사를 썼을 때의 장점이라면 데이터 쉐어링이나 스마트 � SKT의 경우 요금제에 따라 멜론이나 웨이브 같은 혜택이 제공되곤 하는데 그나마 이것도 알뜰폰에서도 점점 지원하고 있는 상태이죠. 예전에는 알뜰폰 통신사가 많지는 않았는데 요즘 통신사가 굉장히 많아지면서 경쟁이 심해지다 보니까 오히려 소비자는 더 좋아졌다랄까요? 왜냐면 알뜰폰 특성상 여러 가지 이벤트를 많이 한다는 점이에요. 심지어 알� 약정이 하나도 없기 때문에 내가 원할 때마다 통신사나 핸드폰을 바꿀 수 있다는 장점까지 있는데 인터넷 결합 할인이 아니라면 굳이 쓸 이유가 크게 없더라고요. 그럼 이게 얼마나 저렴할지 한번 계산을 해봤습니다. 아 요즘 아이폰 13 프로 새로 나왔던데 이게 좀... 이게 요금이 비싸고 좀 저렴하게 쓸 수 있는 방법 없나? 모두 서비스가 다르고 4G 10대 1로 직접적으로 비교하기는 어렵지만 그냥 진짜 참고용으로 비교를 해보자면 제가 사용하고 있는 KT N모바일 모두 다 마음껏이라는 12GB의 데이터 요금제가 있습니다. 이 요금제를 24개월간 썼을 때 686,400원이 나오고 아이폰 13 프로, 쿠팡에서 8% 즉시 할인을 받았을 때 1242,000원입니다. 결국 2에서 개통했을 때의 금액은 어떨까? KT에서 가장 저렴한 5G 슬림을 썼을 때 2년간 사용하게 된다면 99만 원의 통신 요금을 지불하게 됩니다. 여기서 아이폰 13 프로 통신사에서 개통했을 때 할부이자 5.9%까지 포함을 하게 된다면 14 총 더한 금액은 241만 6천 8원 이 나오게 됩니다. 여기서부터 금액 차이가 어마어마하죠? 대충 계산해봐도 대략 50만 원 정도의 차이가 나요. 아마 요금제가 클수록 단말기가 더 비싸질수록 더 큰 차이가 나겠죠? 그나마 요즘 자급제랑 알뜰폰이 유행하다 보니까 이제 아이폰 사전 예약으로 통신사에서 에어팟 프로 같은 걸 주기도 하는데 써야 주더라고요. 뭐 이것을 받는다고 하더라도 자급제와 알뜰폰 조합을 이기기에는 굉장히 어렵습니다. 하지만! 자급제와 알뜰폰 조합으로 썼을 때 이 정도의 가격 차이가 나기는 하지만 알뜰폰의 단점이 있기도 해요. 가끔 사업자마다 교통카드 이슈가 있었습니다. 뭐 아이폰을 사용한다면 크게 이� 않고 만약 꼭 5G로 쓰셔야 하는 분들이라면 알뜰폰이나 메이저 통신사나 가격 차이가 그렇게 크게 나진 않았습니다. 뭐 대략 한 2, 3천 원 정도 차이? 근데 뭐니 뭐니 해도 알뜰폰의 가장 큰 단점은 고객센터의 연결이 매우x3 어렵다는 점이에요. 근데 이것도 제가 한번 생각을 해봤거든요. 과연 내가 핸드폰을 쓰면서 1년 동안 몇 번 전화할까? 진짜 한 5손가락 안에는 없더라고요? 전화할 때마다 짜증 나기는 하지만 개선되면 좀 더 좋다 할까? 그리고 추가로 이렇게 자급제를 많이 구입하게 된다면 핸드폰을 좀 자주 바꾸는 경우가 많고 이렇게 했을 때 중고를 많이 거래하시는 분들을 위해 조금의 팁을 드리자면 먼저 핸드폰을 판매할 때 가장 기본적이지만 데이터를 백업해놓고 초기화를 하는 것이 중요합니다. 물론 가끔 대리점에서 정리를 해준다고 하지만 초기화를 하지 않고 그냥 그것을 받았다가 그 데이터 갖고 그러한 사건이 있기 때문에 이것은 개인이 하는 게 가장 좋아요. 갤럭시 기준으로 이제 가장 쉬운 방법은 일반, 초기화 여기에 들어가서 디바이스 전체 초기화를 해주는 게 가장 중요합니다. 그렇게 되면 여기에 연결되어 있는 계정까지 모두 지워지게 되는 것이죠. 아이폰 같은 경우에는 설정 일반 전송 또는 아이폰 재설정 여기서 모든 컨텐츠 및 설정 지우기를 해주면 돼요. 여기서 더 딥하게 들어가자면 공장 초기화 DFU 보건 같은 여러 가지 더 깨끗하게 지울 수 있는 방법이 있긴 하지만 요즘은 이것까지만 진행해줘도 괜찮을 거예요. 게다가 만약 공시지원금을 받은 기기라면 약정 기간을 체크하고 판매를 해야 됩니다. 선택 약정으로 하게 된다면 기기 자체에 약정이 걸려있지 않기 때문에 내 마음대로 해도 되지만 공시지원금을 받은 경우에는 핸드폰에 약정이 걸려있기 때문에 이때는 그냥 마음대로 판매하면 이제 나중에 좀 골치 아픈 일이 있거든요? 그래서 이것 설정에 보면 휴대전화 정보에 들어갔을 때 IMEI 값이라는 정보가 있어요. 이것을 인터넷의 이동전화 단말기 작업지라는 사이트에서 조회를 해보면 이게 분실된 기기인지 도난 된 스마트폰인지 조회를 할 수 있고 또 요금 25% 할인을 받을 수 있는지 아닌지에 대한 것도 조회를 한 방에 할 수 있습니다. 추가로 확정기변이 가능하다는 뜻은 소유가 내 것으로 만들 수 있고 정상 해지된 핸드폰이라는 뜻이기도 합니다. 이 부분은 통신사를 통해 확인해야 되기 때문에 판매자에게 확실하게 물어보는 것이 중요해요. 만약 확장기변이 불가능하고 유심기변 상태이다? 그럼 나중에 이것을 구입했을 때 내 소유의 핸드폰이 아니기 때문에 원주인이 이것을 분실했다고 신고 이제 골치가 아파지는 거죠. 아무튼 많은 분들이 질문해주시는 자급제로 구입했을 때 통신사로 구입했을 때 어떠한 장단점이 있는지 많이 물어봐주셨는데 개인적으로 생각해봤을 때 내가 통신사에서 만약 혜택을 크게 받고 있지 않다. 그러면 저는 자급제의 알뜰폰 구입을 추천드릴게요. 처음에 알뜰폰이라고 한다면 이게이터 이러한 품질은 100% 동일하기 때문이죠. 아무튼 오늘은 여기까지이며 알뜰폰끼리도 지금 엄청나게 경쟁을 하고 있다 보니까 이것도 1년이나 2년 저렴한 요금제로 쓰고 또 다음에 이벤트를 하게 된다면 알뜰폰은 약정이 없기 때문에 이제 더 저렴한 요금제로 계속 저렴한 이렇게 경쟁을 해주면 소비자는 오히려 더 좋아. 왜냐면 통신사에서도 옛날에 아이폰을 사전 예약하면 여러 가지 혜택 크게 안 줬거든요? 줘야 에어팟 프로 이런 걸 선착순으로 줬는데 지금은 거의 작업제가 점점 더 유행하다 보니까 좀 더 풀고 있더라고요?
"""
VIDEO_ID = "c8OwVTBdE6s"


def parse_video_duration(text):
    # text format examples:
    # PT4H32M57S
    # PT12M56S
    # PT2M6S
    # PT9M
    # PT58S

    # Regex explanation:
    # (?:...) creates a group that isn't captured.
    # (?P<name>...) creates a named group.
    # This way, (?:(?P<h>\d+)H)? will capture the numbers before an 'H' if an 'H' exists and save them to 'h'
    rex = re.compile(r"PT(?:(?P<h>\d+)H)?(?:(?P<m>\d+)M)?(?:(?P<s>\d+)S)?")
    match = rex.match(text)
    logger.debug(f"{text=}, {match=}, {match.groups()=}, {match.groupdict()=}")
    match_dict = {k: int(v) if v is not None else 0 for k, v in match.groupdict().items()}

    delta = timedelta(hours=match_dict['h'], minutes=match_dict['m'], seconds=match_dict['s'])
    return delta


def video_basic_information(video_id):
    logger.info(f'Getting basic information for video with {video_id=}')
    result = get_video_statistics(video_id)
    delta = parse_video_duration(result['duration'])
    result['duration_parsed'] = str(delta)
    result['estimated_categorization_duration'] = result['duration_parsed']
    return result


def youtube_video_categorization(video_id, transcript=None, audio_file_path=None, use_openai=False, truncate=False):
    logger.info(f'Categorizing video with {video_id=}, {transcript=}, {audio_file_path=}')
    result = get_video_statistics(video_id)

    video_url = f"https://www.youtube.com/watch?v={video_id}"
    file_name = video_id

    if transcript is None:
        result['transcript'] = video_transcription(video_url, file_name, audio_file_path, use_openai)
    else:
        result['transcript'] = transcript

    result['AIReadyText'] = '\n\n'.join([result['channelTitle'],
                                         result['title'],
                                         result['description'],
                                         result['transcript']])  # TODO: Improve this...
    
    result['categories'] = text_categorization(result['AIReadyText'], truncate=truncate)
    result['categories']['youtubeCategory'] = result['category']

    logger.info('Done categorizing.')
    return result


def instagram_video_categorization(post_id, audio_file_path=None, use_openai=False, truncate=False):
    logger.info(f'Categorizing video with {post_id=}, {audio_file_path=}')
    result = {}

    video_url = f'https://www.instagram.com/p/{post_id}/'
    file_name = post_id

    result['transcript'] = video_transcription(video_url, file_name, audio_file_path, use_openai)

    result['AIReadyText'] = '\n\n'.join([
                                         result['transcript']])  # TODO: Improve this...
    
    result['categories'] = text_categorization(result['AIReadyText'], truncate=truncate)

    logger.info('Done categorizing.')
    return result


def video_transcription(video_url, file_name, audio_file_path, use_openai):
    logger.info(f'Transcribing video with {video_url=}, {audio_file_path=}')

    
    if audio_file_path is None:
        audio_file_path = download_video(video_url, file_name, False)

    if use_openai:
        transcript = open_ai_stt(audio_file_path)
    else:
        pipeline = load_pipeline()
        transcript = pipeline(audio_file_path, generate_kwargs={"language": "korean"})["text"]
    
    logger.info('Done transcribing')
    return transcript
    

def text_categorization(text, truncate=False):
    return {
        'FreeCategory': get_text_category(text, truncate, 0),
        'PremianCategory': get_embedding_based_category(text, truncate)
    }


def youtube_channel_statistics(channel_handle, channel_id):
    return get_channel_statistics(channel_handle, channel_id)


def youtube_channel_details(channel_handle, channel_id, n):
    return get_channel_details(channel_handle, channel_id, n)


def test():
    result = youtube_video_categorization(VIDEO_ID, transcript=TRANSCRIPT)
    logger.info(json.dumps(result, ensure_ascii=False))  # https://jsonviewer.stack.hu/


def test2():
    result = youtube_video_categorization("mgLeCd5zQ5E")
    logger.info(json.dumps(result, ensure_ascii=False))  # https://jsonviewer.stack.hu/


def test3():
    result = youtube_video_categorization("mgLeCd5zQ5E", use_openai=True)
    logger.info(json.dumps(result, ensure_ascii=False))  # https://jsonviewer.stack.hu/


if __name__ == "__main__":
    logger.info("Program started")
    now = datetime.now()
    test()
    logger.info(f"Program finished. Duration: {datetime.now() - now}")
