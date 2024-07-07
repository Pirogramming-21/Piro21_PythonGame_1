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
