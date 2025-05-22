import random
import string

def generate_code(length=10):
    """
    지정한 길이만큼의 랜덤 영문자+숫자 조합 코드를 생성합니다.
    예: '8FJ2KD9LQX'
    """
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))
