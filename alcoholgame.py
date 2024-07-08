import random
from inputimeout import inputimeout
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
            num_of_opponents = int(input("함께 취할 친구들은 얼마나 필요하신가요? (최대 3명): "))
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
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    for person in invited:
        print(f"오늘 함께 취할 친구는 {person.name}입니다! (주량: {person.max_drinks}잔)")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

def print_drink_status(invited):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("현재 마신 잔 수와 남은 치사량:")
    for person in invited:
        print(f"{person.name}: 지금까지 {person.current_drinks}잔 마셨습니다, 치사량까지 {person.drinks_left()}잔 남았습니다.")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

def print_game_list():
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("오늘의 🍺 게임 리스트:")
    print("1. 사랑의 총알")
    print("2. 좋아 게임")
    print("3. 369 게임")
    print("4. 초성 게임")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    
# 게임 이름을 매핑하는 딕셔너리 추가
game_names = {
    '1': "사랑의 총알",
    '2': "좋아 게임",
    '3': "369 게임",
    '4': "초성 게임"
}


def love_bullet_game(invited, user_name, last_drinker=None):
    print("사랑의~ (빵) 총알을~ (빵) 누구에게 쏠까요~ 빵빵!")
    hands = {player.name: 2 for player in invited}  # 각 플레이어는 2개의 손으로 시작
    
    if last_drinker and last_drinker.name in [p.name for p in invited]:
        host = last_drinker.name
        print(f"{host}(이)가 게임의 주최자로 선정되었습니다.")
    else:
        host = random.choice([p.name for p in invited])
        print(f"{host}(이)가 게임의 주최자로 랜덤 선정되었습니다.")
    
    # 각 플레이어가 지목할 사람 선택
    targets = {}
    for player in invited:
        if player.name == user_name: # 유저가 플레이어인 경우 지목할 사람을 정할 수 있도록
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
        target_str = ' 와(과) '.join(set(player_targets))  # 중복 제거
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
            return loser
        
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
        
        print(f"'빵!' {current_player}(이)가 {next_player}를 선택했습니다.")
        print(f"{current_player}의 손이 하나 내려갔습니다.")
        
        if hands[current_player] == 0:
            print(f"{current_player}(이)가 모든 손을 잃었습니다!")
        
        current_player = next_player
        
        time.sleep(1.5)  # 게임 진행 속도 조절

import time
import random

def like_game(players, user_name):
    rejected_counts = {player.name: 0 for player in players}
    host = random.choice(players)
    user = next(player for player in players if player.name == user_name)
    print("아 술도 마셨는데~ 좋아 게임할까~ 좋아, 좋아, 좋아좋아좋아!!")
    print(f"\n주최자는 {host.name}입니다!\n")
    time.sleep(1)

    while True:
        available_players = [player for player in players if player.name != host.name]
        
        if host == user:
            while True:
                target_input = input(f"{host.name}: 누구를 지목하시겠습니까? (예: '유민 좋아') ").strip()
                if " 좋아" in target_input:
                    target_name = target_input.replace(" 좋아", "").strip()
                    target = next((player for player in available_players if player.name == target_name), None)
                    if target:
                        print(f"{host.name}: {target.name} 좋아!")
                        time.sleep(1)
                        break
                print("유효하지 않은 입력입니다. 다시 시도해주세요.")
                time.sleep(1)
        else:
            target = random.choice(available_players)
            print(f"{host.name}: {target.name} 좋아!")
            time.sleep(1)
        
        if target == user:
            print("\n선택 가능한 반응:")
            print("1. 나도 좋아 (바로 좋아 좋아~)")
            print("2. 얼만큼? (상대방이 최대 3번까지 '이만큼~'을 외칩니다)")
            print("3. 나는 싫어 (모두가 '그럼 누구?'를 외칩니다)")
            print("4. 칵, 퉤 (거절합니다)")
            response = input(f"{target.name}, 반응을 선택하세요 (1-4): ").strip()
            responses = ["나도 좋아", "얼만큼?", "나는 싫어", "칵, 퉤"]
            response = responses[int(response)-1] if response.isdigit() and 1 <= int(response) <= 4 else "잘못된 입력"
        else:
            response = random.choice(["나도 좋아", "얼만큼?", "나는 싫어", "칵, 퉤"])
        print(f"{target.name}: {response}")
        time.sleep(1)
        
        if response == "나도 좋아":
            print("모두: 좋아 좋아~")
            time.sleep(1)
            host = target
            rejected_counts[host.name] = 0  # 카운트 초기화
        elif response == "얼만큼?":
            for i in range(3):
                print(f"{host.name}: 이만큼~")
                time.sleep(1)
                if target == user:
                    print("\n선택 가능한 반응:")
                    print("1. 나도 좋아 (게임 계속)")
                    print("2. 부족해~ (다음 '이만큼~'으로)")
                    target_response = input(f"{target.name}, 반응을 선택하세요 (1-2): ").strip()
                    target_response = "나도 좋아" if target_response == "1" else "부족해~"
                else:
                    target_response = random.choice(["나도 좋아", "부족해~"])
                print(f"{target.name}: {target_response}")
                time.sleep(1)
                
                if target_response == "나도 좋아":
                    print("모두: 좋아 좋아~")
                    time.sleep(1)
                    host = target
                    rejected_counts[host.name] = 0  # 카운트 초기화
                    break
            else:  # 3번 모두 실패한 경우
                print(f"누가누가 술을 마셔 ~ {host.name}이(가) 술을 마셔~~!!")
                time.sleep(1)
                host.drink(1)
                return host
        elif response == "나는 싫어":
            print("모두: 그럼 누구?")
            time.sleep(1)
            rejected_counts[host.name] += 1
        elif response == "칵, 퉤":
            rejected_counts[host.name] += 1
        else:
            print("잘못된 입력입니다. 다음 차례로 넘어갑니다.")
            time.sleep(1)
        
        if rejected_counts[host.name] >= 3:
            print(f"누가누가 술을 마셔 ~ {host.name}이(가) 술을 마셔~~!!")
            time.sleep(1)
            host.drink(1)
            return host
        
        print(f"\n다음 주최자는 {host.name}입니다.\n")
        time.sleep(1)

    return host

def samyukgu(invited, user): 

    print("369~ 369! 369~ 369!!")
    flag = True
    num = 0
    while flag:
        for member in invited:
            num += 1

            if member == user:      #순서가 사용자인 경우 입력받는다.
                userInput = userInputTimeout()
            else:                   #순서가 사용자가 아니라면 랜덤으로 수를 배정받는다.
                answerPercentage = random.randrange(0, 10, 1)
                if answerPercentage <= 1:
                    userInput = random.choice([num-1, num+1, num, "짝"])
                else:
                    if ("3" in str(num)) or ("6" in str(num)) or ("9" in str(num)): userInput = '짝'
                    else: userInput = num

            #타임 아웃이 난 경우
            if (userInput == 'timeout'):
                flag = False
                selectedMemberInfoPrinting(member)
                return member

            elif userInput == '짝':
                print(member.name, " : ", userInput)
                time.sleep(1)
                if ("3" in str(num)) or ("6" in str(num)) or ("9" in str(num)):
                    continue
                else:
                    flag = False
                    print("틀렸습니다!!")
                    selectedMemberInfoPrinting(member)
                    return member
            else:
                print(member.name, " : ", userInput)
                time.sleep(1)
                ans = str(num)
                if ("3" in str(num)) or ("6" in str(num)) or ("9" in str(num)):
                    ans = "짝"

                if str(userInput) == ans:
                    continue;
                else:
                    flag = False
                    print("틀렸습니다!!")
                    selectedMemberInfoPrinting(member)
                    return member


def selectedMemberInfoPrinting(member):
    print(f"\n{member.name}(이)가 369 게임에서 패배했습니다!")
    time.sleep(3)
    member.drink(1)
    print(f"{member.name}: 지금까지 {member.current_drinks}잔 마셨습니다, 치사량까지 {member.drinks_left()}잔 남았습니다.")

def userInputTimeout():
    try:
        c = inputimeout('당신 차례!!:\n', 3)
    except Exception:
        c = 'timeout'
        print('타임 오버! 패배입니다!')
    return c

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
    pages = [1, 2, 3]

    try:
        for page in pages:
            current_url = f"{url}&page={page}"
            driver.get(current_url)
            time.sleep(3)

            rows = driver.find_elements(By.CLASS_NAME, 'origin')
            if not rows:  # 더 이상 단어가 없으면 루프를 종료합니다.
                break

            for row in rows:
                links = row.find_elements(By.TAG_NAME, 'a')
                for link in links:
                    word = link.text.strip().replace(" ", "")  # 공백, 숫자 제거
                    clean_word = re.sub(r'\d+\s*$', '', word)
                    words.append(clean_word)

            page += 1  # 다음 페이지로 이동

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
    print("-------------------------Are You Ready ?------------------------------")

    url = f"https://ko.dict.naver.com/#/search?range=entry&query={initials}&shouldSearchOpen=false&autoConvert="
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
                return selected_person

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
                return remaining_person

def get_user_info():
    print(r'''
     _       _        ____    _   _       U  ___  u  _   _       U  ___  u   _           ____       _      __  __  U  _____  u 
 U  /"\  u  |"|    U /"___|  |'| |'|       \/"_ \/  |'| |'|       \/"_ \/   |"|       U /"___| uU  /"\  uU|' \/ '|u \| ___"|/ 
  \/ _ \/ U | | u  \| | u   /| |_| |\      | | | | /| |_| |\      | | | | U | | u      \| |  _ / \/ _ \/ \| |\/| |/  |  _|"   
  / ___ \  \| |/__  | |/__ U |  _  | u .-,_| |_| |U |  _  | u .-,_| |_| |  \| |/__      | |_| |  / ___ \  | |  | |   | |___   
 /_/   \_\  |_____|  \____|  |_| |_|    \_)-\___/   |_| |_|    \_)-\___/    |_____|      \____| /_/   \_\ |_|  |_|   |_____|  
 \\     >>  //  \\  _// \\   //   \\          \\    //   \\          \\     //  \\       _)(|_   \\    >> <<,-,,-.   <<   >>  
(__)   (__)(_")("_)(__) (__)(_") ("_)        (__)  (_") ("_)        (__)   (_")("_)     (__)__) (__)  (__)(./  \.)  (__) (__)
''')
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("(〃´𓎟`〃)(〃´𓎟`〃)(〃´𓎟`〃)(〃´𓎟`〃)    안주 먹을🍗 시간⏱️이 없어요🙅 마시면서 배우는 술게임🍺🍻   (〃´𓎟`〃)(〃´𓎟`〃)(〃´𓎟`〃)(〃´𓎟`〃)")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print()
    user_name = input("오늘 거하게 취해볼 당신의 이름은?: ")
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~🍺 소주 기준 당신의 주량은? 🍺~~~~~~~~~~~~~~~~~~~~~~~~")
    print("🍺 1. 소주 반병 (2잔)")
    print("🍺 2. 소주 반병에서 한병 (4잔)")
    print("🍺 3. 소주 한병에서 한병 반 (6잔)")
    print("🍺 4. 소주 한병 반에서 두병 (8잔)")
    print("🍺 5. 소주 두병 이상 (10잔)")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    
    while True:
        try:
            choice = int(input("당신의 치사량(주량)은 얼마인가요?(1 ~ 5를 선택해주세요): "))
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
    last_drinker = None

    while not game_over:
        print_drink_status(invited)
        print_game_list()
        
        if last_drinker is None or last_drinker == user:
            game_choice = input("게임을 선택하세요 (1, 2, 3, 4): ")
        else:
            game_choice = str(random.randint(1, 4))
            print(f"아 {last_drinker.name}이(가)~ 좋아하는~ 랜덤~ 게임~ 무슨~ 게임~")
            print(f"{last_drinker.name}이(가) {game_names[game_choice]}을(를) 선택했습니다.")
            time.sleep(3)
        
        if game_choice in game_names:
            print(r'''
_   _  _            _____                      
| \ | (_)          |  __ \                     
|  \| |_  ___ ___  | |  \/ __ _ _ __ ___   ___ 
| . ` | |/ __/ _ \ | | __ / _` | '_ ` _ \ / _ \
| |\  | | (_|  __/ | |_\ \ (_| | | | | | |  __/
\_| \_/_|\___\___|  \____/\__,_|_| |_| |_|\___|
''')
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(f"{game_names[game_choice]}을(를) 시작합니다!")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
            if game_choice == '1':
                last_drinker = love_bullet_game(invited, user.name, last_drinker)
            elif game_choice == '2':
                last_drinker = like_game(invited, user.name)
            elif game_choice == '3':
                last_drinker = samyukgu(invited, user)
            elif game_choice == '4':
                last_drinker = initial_game(invited)
        else:
            print("잘못된 선택입니다. 다시 선택해주세요.")
            continue

        for person in invited:
            if person.drinks_left() <= 0:
                print_drink_status(invited)
                print(r''' 
 ██████   █████  ███    ███ ███████      ██████  ██    ██ ███████ ██████  
██       ██   ██ ████  ████ ██          ██    ██ ██    ██ ██      ██   ██ 
██   ███ ███████ ██ ████ ██ █████       ██    ██ ██    ██ █████   ██████  
██    ██ ██   ██ ██  ██  ██ ██          ██    ██  ██  ██  ██      ██   ██ 
 ██████  ██   ██ ██      ██ ███████      ██████    ████   ███████ ██   ██ 
''')
                print(f"\n{person.name}(이)가 전사했습니다... 꿈나라에서는 편히 쉬시길...zzz")
                game_over = True
                break
        time.sleep(1)

    print(f"\n🍺 다음에 술 마시면 또 불러주세요~ 안녕! 🍺")

if __name__ == "__main__":
    main()