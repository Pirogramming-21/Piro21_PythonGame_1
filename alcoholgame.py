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
        "이민수": 5,
        "김민수": 4,
        "유민": 3,
        "수용": 6,
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
    print("\n오늘의 🍺 게임 리스트:")
    print("1. 사랑의 총알")
    print("2. 좋아 게임")
    print("3. 369 게임")
    print("4. 초성 게임")

def love_bullet_game(invited, user_name):
    print("\n사랑의 총알 게임을 시작합니다!")
    hands = {player.name: 2 for player in invited}  # 각 플레이어는 2개의 손으로 시작
    host = random.choice([p.name for p in invited])
    print(f"{host}가 게임의 주최자로 선정되었습니다.")
    
    # 각 플레이어가 지목할 사람 선택
    targets = {}
    for player in invited:
        if player.name == user_name:
            print(f"\n{user_name}, 누구를 지목하시겠습니까? (1-2명 선택)")
            available_targets = [p.name for p in invited if p.name != user_name]
            for i, target in enumerate(available_targets, 1):
                print(f"{i}. {target}")
            while True:
                choices = input("번호를 입력하세요 (여러 명 선택 시 공백으로 구분): ").split()
                if 1 <= len(choices) <= 2 and all(choice.isdigit() and 1 <= int(choice) <= len(available_targets) for choice in choices):
                    player_targets = [available_targets[int(choice)-1] for choice in choices]
                    break
                else:
                    print("잘못된 입력입니다. 다시 선택해주세요.")
        else:
            available_targets = [p.name for p in invited if p.name != player.name]
            num_targets = random.randint(1, 2)
            player_targets = random.choices(available_targets, k=num_targets)
        
        targets[player.name] = player_targets
        target_str = ' 와 '.join(set(player_targets))  # 중복 제거
        print(f"{player.name}이(가) {target_str}를 지목했습니다.")
    
    current_player = host
    
    while True:
        print(f"\n현재 플레이어: {current_player}")
        print("현재 상태:", hands)
        
        if hands[current_player] == 0:
            loser = next(p for p in invited if p.name == current_player)
            print(f"게임 종료! {current_player}(이)가 패배했습니다.")
            loser.drink(1)
            print(f"{loser.name}: 지금까지 {loser.current_drinks}잔 마셨습니다, 치사량까지 {loser.drinks_left()}잔 남았습니다.")
            break
        
        if current_player == user_name:
            print(f"\n{user_name}, 누구에게 '빵!'을 하시겠습니까?")
            for i, target in enumerate(targets[user_name], 1):
                print(f"{i}. {target}")
            while True:
                choice = input("번호를 입력하세요: ")
                if choice.isdigit() and 1 <= int(choice) <= len(targets[user_name]):
                    next_player = targets[user_name][int(choice)-1]
                    break
                else:
                    print("잘못된 입력입니다. 다시 선택해주세요.")
        else:
            next_player = random.choice(targets[current_player])
        
        hands[current_player] -= 1
        
        print(f"'빵!' {current_player}가 {next_player}를 선택했습니다.")
        print(f"{current_player}의 손가락이 하나 내려갔습니다.")
        
        if hands[current_player] == 0:
            print(f"{current_player}(이)가 모든 손가락을 잃었습니다!")
        
        current_player = next_player
        
        time.sleep(1.5)  # 게임 진행 속도 조절

def like_game(players):
    rejected_counts = {player.name: 0 for player in players}
    host = random.choice(players)               # 일단 이건 랜덤으로
    print(f"\n주최자는 {host.name}입니다!\n")
    print("\n현재 사람들 중 한명을 지목하여 '○○ 좋아!'를 입력해주세요 (본인 제외)! 🚨")

    while True:
        available_players = [player for player in players if player.name != host.name]
        target = random.choice(available_players)
        print(f"{host.name}: {target.name} 좋아!")
        
        responses = ["나도 좋아", "얼만큼?", "나는 싫어", "칵, 퉤"]
        
        response = random.choice(responses) # 이것도 랜덤으로
        print(f"{target.name}: {response}")
        
        if response == "나도 좋아":
            print("좋아 좋아!")
            host = target
            continue
        elif response == "얼만큼?":
            for i in range(3):
                print(f"{host.name}가 주접을 부립니다. '아주 많이 좋아해!'")
                if random.choice([True, False]):
                    print(f"{target.name}: 좋아 좋아!")
                    host = target
                    break
                else:
                    print(f"{target.name}: 쫌만 더~")

            else:
                print(f"누가누가 술을 마셔 ~ {host.name}이(가) 술을 마셔~~!!")
                host.drink(1)
                return host
            continue
                    
        elif response == "나는 싫어":
            print("모두가 그럼 누구?를 외친다!")
            continue
            
        elif response == "칵, 퉤":
            rejected_counts[host.name] += 1
            if rejected_counts[host.name] >= 3:
                print(f"누가누가 술을 마셔 ~ {host.name}이(가) 술을 마셔~~!!")
                host.drink(1)
                return host
            continue
    
    return host


def samyukgu(invited):

    print("369~ 369! 369~ 369!!")
    flag = True
    num = 0
    while flag:
        for member in invited:
            num += 1

            #성공할 확률, 실패할 확률
            answerPercentage = random.randrange(0, 10, 1)
            if answerPercentage <= 1:
                if ("3" in str(num)) or ("6" in str(num)) or ("9" in str(num)):
                    print(member.name, " : ", num)
                    flag = False
                    print("틀렸습니다!!")
                    selectedMemberInfoPrinting(member)
                    break
                else:
                    print(member.name, " : " + "짝")
                    flag = False
                    print("틀렸습니다!!")
                    selectedMemberInfoPrinting(member)
                    break
            else:
                if '3' in str(num) or '6' in str(num) or '9' in str(num):
                    print(member.name, " : " + "짝")
                else:
                    print(member.name, " : ", num)

def selectedMemberInfoPrinting(member):
    print(f"\n{member.name}(이)가 게임 C에서 패배했습니다!")
    member.drink(1)
    print(f"{member.name}: 지금까지 {member.current_drinks}잔 마셨습니다, 치사량까지 {member.drinks_left()}잔 남았습니다.")

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
        for selected_person in invited:
            if selected_person in passed_players:
                continue
            word = input(f"{selected_person.name} 차례! ").strip()

            if word in used_words:
                print(f"\n{selected_person.name}(이)가 단어 중복으로 초성 게임에서 패배했습니다!")
                selected_person.drink(1)  # selected_person 탈락 시 1잔만 마심
                return

            if word in valid_words:
                valid_words.remove(word)
                used_words.add(word)
                passed_players.add(selected_person)
                print(f"{selected_person.name}(이)는 통과 !")
            else:
                print(f"{selected_person.name}(이)는 '{word}'를 입력하지 못했습니다. 다음 기회에...")

            if len(passed_players) == len(invited) - 1:
                remaining_person = set(invited) - passed_players
                remaining_person = remaining_person.pop()  # 집합에서 요소 하나를 꺼냄
                print(f"마지막에 남은 {remaining_person.name}(이)가 초성 게임에서 패배했습니다! ")
                remaining_person.drink(1)  # remaining_person 탈락 시 1잔만 마심
                return

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
            love_bullet_game(invited, user.name)
        elif game_choice == '2':
            like_game(invited)
        elif game_choice == '3':
            samyukgu(invited)
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
        time.sleep(1)  # 예시로 1초 대기

    print("\nGAME OVER!")
    print(f"\n🍺 다음에 술 마시면 또 불러주세요~ 안녕! 🍺")

if __name__ == "__main__":
    main()