import random
import time

def game_a(invited, user_name):
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
          print(f"게임 종료! {current_player}가 패배했습니다.")
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
      
      time.sleep(1)  # 게임 진행 속도 조절

# 메인 함수에서 이 함수를 호출할 때는 다음과 같이 사용합니다:
# game_a(invited, user.name)