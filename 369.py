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
                break

            elif userInput == '짝':
                print(member.name, " : ", userInput)
                if ("3" in str(num)) or ("6" in str(num)) or ("9" in str(num)):
                    continue
                else:
                    flag = False
                    print("틀렸습니다!!")
                    selectedMemberInfoPrinting(member)
                    return member
            else:
                print(member.name, " : ", userInput)
                ans = str(num)
                if ("3" in str(num)) or ("6" in str(num)) or ("9" in str(num)):
                    ans = "짝"

                if str(userInput) == ans:
                    continue;
                else:
                    flag = False
                    print("틀렸습니다!!")
                    selectedMemberInfoPrinting(member)
                    break


def selectedMemberInfoPrinting(member):
    print(f"\n{member.name}(이)가 369 게임에서 패배했습니다!")
    member.drink(1)
    print(f"{member.name}: 지금까지 {member.current_drinks}잔 마셨습니다, 치사량까지 {member.drinks_left()}잔 남았습니다.")

def userInputTimeout():
    try:
        c = inputimeout('당신 차례!!:\n', 3)
    except Exception:
        c = 'timeout'
        print('타임 오버! 패배입니다!')
    return c