import random


def game_c(invited):
    print("369~ 369! 369~ 369!!")
    flag = True
    num = 0
    while flag:
        for member in invited:
            num += 1

            answerPercentage = random.randrange(0, 10, 1)
            if answerPercentage <= 1:
                if '3' in str(num):
                    print(member, " : ", num)
                else:
                    print(member, " : " + "짝")
                flag = False
                print("틀렸습니다!!")
                break
            else:
                if '3' in str(num):
                    print(member, " : " + "짝")
                else:
                    print(member, " : ", num)

invited = {
    "은서": 5,
    "하연": 4,
    "연서": 3,
    "예진": 6,
    "헌도": 2
}

game_c(invited)