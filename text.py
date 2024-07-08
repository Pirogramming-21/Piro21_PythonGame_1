import random
import time
from inputimeout import inputimeout

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
    print("3. 369게임")
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

def userInputTimeout():
    try:
        while True:
            c = inputimeout('당신 차례!!:\n', 3)
            if c == '짝' or c.isdigit(): break
            else: print("잘못된 입력입니다.")
    except Exception:
        c = 'timeout'
        print('타임 오버! 패배입니다!')
    return c

def selectedMemberInfoPrinting(member):
    print(f"\n{member.name}(이)가 게임 C에서 패배했습니다!")
    member.drink(1)
    print(f"{member.name}: 지금까지 {member.current_drinks}잔 마셨습니다, 치사량까지 {member.drinks_left()}잔 남았습니다.")

def game_c(invited, user): # 이수용 함수 구현

    #--------------------------------------------------

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
                    userInput = num

            #타임 아웃이 난 경우
            if (userInput == 'timeout'):
                flag = False
                selectedMemberInfoPrinting(member)
                break

            elif userInput == '짝':
                print(member.name, " : ", userInput)
                if ("3" in str(num)) or ("6" in str(num)) or ("9" in str(num)):
                    continue
                else:
                    flag = False
                    print("틀렸습니다!!")
                    selectedMemberInfoPrinting(member)
                    break
            else:
                print(member.name, " : ", userInput)

                if str(userInput) == str(num):
                    continue;
                else:
                    flag = False
                    print("틀렸습니다!!")
                    selectedMemberInfoPrinting(member)
                    break



    #--------------------------------------------




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
            game_a(invited)
        elif game_choice == '2':
            game_b(invited)
        elif game_choice == '3':
            game_c(invited, user)
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