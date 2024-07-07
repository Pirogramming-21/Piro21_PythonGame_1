import random

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