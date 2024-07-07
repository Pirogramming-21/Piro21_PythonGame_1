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
    print("3. 369 게임")
    print("4. 게임 D")

def game_a(invited): #김민수 함수 구현
    selected_person = random.choice(invited)
    print(f"\n{selected_person.name}(이)가 게임 A에서 패배했습니다!")
    selected_person.drink(1)
    print(f"{selected_person.name}: 지금까지 {selected_person.current_drinks}잔 마셨습니다, 치사량까지 {selected_person.drinks_left()}잔 남았습니다.")

def game_b(invited): # 이민수 함수 구현
    selected_person = random.choice(invited)
    print(f"\n{selected_person.name}(이)가 게임 B에서 패배했습니다!")
    selected_person.drink(1)
    print(f"{selected_person.name}: 지금까지 {selected_person.current_drinks}잔 마셨습니다, 치사량까지 {selected_person.drinks_left()}잔 남았습니다.")

def game_c(invited): # 이수용 함수 구현

    #--------------------------------------------------

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

    #--------------------------------------------

def game_d(invited): # 주유민 함수 구현
    selected_person = random.choice(invited)
    print(f"\n{selected_person.name}(이)가 게임 D에서 패배했습니다!")
    selected_person.drink(1)
    print(f"{selected_person.name}: 지금까지 {selected_person.current_drinks}잔 마셨습니다, 치사량까지 {selected_person.drinks_left()}잔 남았습니다.")

def selectedMemberInfoPrinting(member):
    print(f"\n{member.name}(이)가 게임 C에서 패배했습니다!")
    member.drink(1)
    print(f"{member.name}: 지금까지 {member.current_drinks}잔 마셨습니다, 치사량까지 {member.drinks_left()}잔 남았습니다.")


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

    #아직 게임 선택 안한 사람들 모임
    chooser = list(invited)

    while not game_over:
        print_drink_status(invited)
        print_game_list()

        #모두 게임 선택했지만 아직 게임이 안 끝났다면 다시 리셋
        if len(chooser) == 0:
            chooser = list(invited)

        #선택하고 제거
        player = random.sample(chooser, 1).pop(0)
        chooser.remove(player)
        print(user.name, "이/가 게임을 선택합니다.")

        if player == user:                                  #선택된 사람이 user이면 입력받는다.
            print_game_list()
            while True:
                game_choice = input("게임을 선택하세요 (1, 2, 3, 4): ")
                if game_choice != '1' and game_choice != '2' and game_choice != '3' and game_choice != '4':
                    print("잘못된 선택입니다. 다시 선택해주세요.")
                    continue
        else:                                               #컴퓨터가 플레이 하는 사람이 선택되면 게임 렌덤 배정
            game_choice = str(random.randrange(1, 5))
            print(user.name, "이/가 ", game_choice, "번 게임을 선택했습니다.")

        if game_choice == '1':
            game_a(invited)
        elif game_choice == '2':
            game_b(invited)
        elif game_choice == '3':
            game_c(invited)
        elif game_choice == '4':
            game_d(invited)

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

