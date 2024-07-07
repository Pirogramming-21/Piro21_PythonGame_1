import random
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver


class Person:
    def __init__(self, name, max_drinks):
        self.name = name
        self.max_drinks = max_drinks
        self.current_drinks = 0

    def drink(self, amount):
        self.current_drinks += amount

    def drinks_left(self):
        return self.max_drinks - self.current_drinks
    

def invite_opponents():
    opponents = {
        "은서": 5,
        "하연": 4,
        "연서": 3,
        "예진": 6,
        "헌도": 2
    }

    while True:
        try:
            num_of_opponents = int(input("초대할 사람의 수를 입력하세요 (최대 3명): "))
            if num_of_opponents > 3:
                print("최대 3명까지 초대할 수 있습니다. 다시 입력해주세요.")
            else:
                break
        except ValueError:
            print("숫자를 입력해주세요.")

    invited_names = random.sample(list(opponents.keys()), num_of_opponents)
    invited = [Person(name, opponents[name]) for name in invited_names]
    return invited


def print_invited(invited):
    print("\n초대된 사람들:")
    for person in invited:
        print(f"{person.name} (주량: {person.max_drinks}잔)")


def print_drink_status(invited):
    print("\n현재 마신 잔 수와 남은 치사량:")
    for person in invited:
        print(f"{person.name}: 지금까지 {person.current_drinks}잔 마셨습니다, 치사량까지 {person.drinks_left()}잔 남았습니다.")


def print_game_list():
    print("\n게임 리스트:")
    print("1. 게임 A")
    print("2. 게임 B")
    print("3. 게임 C")
    print("4. 초성 게임")


def game_a(invited):
    selected_person = random.choice(invited)
    print(f"\n{selected_person.name}(이)가 게임 A에서 패배했습니다!")
    selected_person.drink(1)
    print(f"{selected_person.name}: 지금까지 {selected_person.current_drinks}잔 마셨습니다, 치사량까지 {selected_person.drinks_left()}잔 남았습니다.")


def game_b(invited):
    selected_person = random.choice(invited)
    print(f"\n{selected_person.name}(이)가 게임 B에서 패배했습니다!")
    selected_person.drink(1)
    print(f"{selected_person.name}: 지금까지 {selected_person.current_drinks}잔 마셨습니다, 치사량까지 {selected_person.drinks_left()}잔 남았습니다.")


def game_c(invited):
    selected_person = random.choice(invited)
    print(f"\n{selected_person.name}(이)가 게임 C에서 패배했습니다!")
    selected_person.drink(1)
    print(f"{selected_person.name}: 지금까지 {selected_person.current_drinks}잔 마셨습니다, 치사량까지 {selected_person.drinks_left()}잔 남았습니다.")

# 초성 게임(주유민)------------------------------------------------------------------------------------------------------------
def get_words(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-logging')
    options.add_argument('--log-level=3')
    # 로그 짧게 출력

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    words = []
    try:
        #print(f"크롤링할 URL: {url}")
        driver.get(url)
        time.sleep(3)

        rows = driver.find_elements(By.CLASS_NAME, 'origin')
        for row in rows:
            links = row.find_elements(By.TAG_NAME, 'a')
            for link in links:
                word = link.text.strip().replace(" ", "")  # 공백, 숫자 제거
                clean_word = re.sub(r'\d+\s*$', '', word)
                words.append(clean_word)

        #print(f"추출된 단어: {words}")
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        driver.quit()

    return words


def generate_initials():
    consonants = ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    return random.choice(consonants) + random.choice(consonants)



def initial_game(invited):
    initials = generate_initials()
    print(f"초성은 '{initials}'")
    print("-------------------Are You Ready ?------------------------")

    url = f"https://ko.dict.naver.com/#/search?range=word&query={initials}&autoConvert=&shouldSearchOpen=false&autoConvert="
    valid_words = get_words(url)
    if not valid_words:
        print("해당하는 초성에 맞는 단어를 찾을 수 없습니다. 게임을 다시 시작합니다.")
        return initial_game(invited)

    print(f"크롤링된 단어들: {valid_words}")

    used_words = set()
    passed_players = set()

    while valid_words and len(passed_players) < len(invited) - 1:
        print("\n현재 플레이어 목록:")
        for i, person in enumerate(invited, 1):
            print(f"{i}. {person.name}")

        word_entered = False
        while not word_entered:
            try:
                player_number = int(input("플레이어 번호를 입력하세요: ")) - 1
                if player_number < 0 or player_number >= len(invited):
                    print("유효한 번호를 입력해주세요.")
                    continue
            except ValueError:
                print("숫자를 입력해주세요.")
                continue

            selected_person = invited[player_number]
            if selected_person in passed_players:
                print(f"{selected_person.name}(이)는 이미 통과했습니다.")
                continue

            word = input("단어를 입력하세요: ").strip()

            if word in used_words:
                print(f"\n{selected_person.name}(이)가 중복된 단어로 초성 게임에서 패배했습니다!")
                selected_person.drink(1)  # selected_person 탈락 시 1잔만 마심
                return

            if word in valid_words:
                valid_words.remove(word)
                used_words.add(word)
                passed_players.add(selected_person)
                print(f"{selected_person.name} 통과!")
                word_entered = True
            else:
                print(f"{selected_person.name}(이)는 '{word}'를 입력하지 못했습니다. 다음 기회에...")

            if len(passed_players) == len(invited) - 1:
                remaining_person = set(invited) - passed_players
                remaining_person = remaining_person.pop()  # 집합에서 요소 하나를 꺼냄
                print(f"마지막에 남은 {remaining_person.name}(이)가 초성 게임에서 패배했습니다!")
                remaining_person.drink(1)  # remaining_person 탈락 시 1잔만 마심
                return

# 초성 게임--------------------------------------------------------------------------------------------




def get_user_info():
    user_name = input("오늘 거하게 취해볼 당신의 이름은?: ")
    print("\n소주 기준 당신의 주량은? 🍺~~~~~~~~~~~~~~~~~~~~~~~~")
    print("1. 소주 반병 (2잔)")
    print("2. 소주 반병에서 한병 (4잔)")
    print("3. 소주 한병에서 한병 반 (6잔)")
    print("4. 소주 한병 반에서 두병 (8잔)")
    print("5. 소주 두병 이상 (10잔)")

    while True:
        try:
            choice = int(input("당신의 치사량(주량)은 얼마만큼인가요?(1~5을 선택해주세요): "))
            if 1 <= choice <= 5:
                max_drinks = choice * 2
                break
            else:
                print("1에서 5 사이의 숫자를 선택해주세요.")
        except ValueError:
            print("숫자를 입력해주세요.")

    user = Person(user_name, max_drinks)
    return user


def main():
    user = get_user_info()
    invited = invite_opponents()
    print_invited(invited)
    invited.append(user)
    game_over = False

    while not game_over:
        print_drink_status(invited)
        print_game_list()
        game_choice = input("게임을 선택하세요 (1, 2, 3, 4): ")
        if game_choice == '1':
            game_a(invited)
        elif game_choice == '2':
            game_b(invited)
        elif game_choice == '3':
            game_c(invited)
        elif game_choice == '4':
            initial_game(invited)
        else:
            print("잘못된 선택입니다. 다시 선택해주세요.")
            continue

        for person in invited:
            if person.drinks_left() <= 0:
                print_drink_status(invited)
                print(f"\n{person.name}(이)가 전사했습니다... 꿈나라에서는 편히 쉬시길...zzz")
                game_over = True
                break
        time.sleep(1)

    print("\nGAME OVER!")
    print(f"\n🍺 다음에 술 마시면 또 불러주세요~ 안녕! 🍺")


if __name__ == "__main__":
    main()
