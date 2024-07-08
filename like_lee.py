import random

def like_game(players, user_name):
    rejected_counts = {player.name: 0 for player in players}
    host = random.choice(players)
    user = next(player for player in players if player.name == user_name)
    print(f"\n주최자는 {host.name}입니다!\n")

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
                        break
                print("유효하지 않은 입력입니다. 다시 시도해주세요.")
        else:
            target = random.choice(available_players)
            print(f"{host.name}: {target.name} 좋아!")
        
        if target == user:
            responses = ["나도 좋아", "얼만큼?", "나는 싫어", "칵, 퉤"]
            response = input(f"{target.name}: {', '.join(responses)} 중 하나를 입력하세요: ").strip()
        else:
            response = random.choice(["나도 좋아", "얼만큼?", "나는 싫어", "칵, 퉤"])
            print(f"{target.name}: {response}")
        
        if response == "나도 좋아":
            print("모두: 좋아 좋아~")
            host = target
            rejected_counts[host.name] = 0  # 카운트 초기화
        elif response == "얼만큼?":
            for i in range(3):
                print(f"{host.name}: 이만큼~")
                if target == user:
                    target_response = input(f"{target.name}, 반응을 선택하세요 ('나도 좋아' 또는 다른 반응): ").strip()
                else:
                    target_response = random.choice(["나도 좋아", "..."])
                print(f"{target.name}: {target_response}")
                
                if target_response == "나도 좋아":
                    print("모두: 좋아 좋아~")
                    host = target
                    rejected_counts[host.name] = 0  # 카운트 초기화
                    break
            else:  # 3번 모두 실패한 경우
                print(f"누가누가 술을 마셔 ~ {host.name}이(가) 술을 마셔~~!!")
                host.drink(1)
                return host
        elif response == "나는 싫어":
            print("모두: 그럼 누구?")
            rejected_counts[host.name] += 1
        elif response == "칵, 퉤":
            rejected_counts[host.name] += 1
        else:
            print("잘못된 입력입니다. 다음 차례로 넘어갑니다.")
        
        if rejected_counts[host.name] >= 3:
            print(f"누가누가 술을 마셔 ~ {host.name}이(가) 술을 마셔~~!!")
            host.drink(1)
            return host
        
        print(f"\n다음 주최자는 {host.name}입니다.\n")

    return host