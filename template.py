import random
import time

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
    print("2. 게임 B")
    print("3. 게임 C")
    print("4. 게임 D")

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

def game_b(invited): # 이민수 함수 구현 
    selected_person = random.choice(invited)
    print(f"\n{selected_person.name}(이)가 게임 B에서 패배했습니다!")
    selected_person.drink(1)
    print(f"{selected_person.name}: 지금까지 {selected_person.current_drinks}잔 마셨습니다, 치사량까지 {selected_person.drinks_left()}잔 남았습니다.")

def game_c(invited): # 이수용 함수 구현
    selected_person = random.choice(invited)
    print(f"\n{selected_person.name}(이)가 게임 C에서 패배했습니다!")
    selected_person.drink(1)
    print(f"{selected_person.name}: 지금까지 {selected_person.current_drinks}잔 마셨습니다, 치사량까지 {selected_person.drinks_left()}잔 남았습니다.")

def game_d(invited): # 주유민 함수 구현 
    selected_person = random.choice(invited)
    print(f"\n{selected_person.name}(이)가 게임 D에서 패배했습니다!")
    selected_person.drink(1)
    print(f"{selected_person.name}: 지금까지 {selected_person.current_drinks}잔 마셨습니다, 치사량까지 {selected_person.drinks_left()}잔 남았습니다.")

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
            game_b(invited)
        elif game_choice == '3':
            game_c(invited)
        elif game_choice == '4':
            game_d(invited)
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