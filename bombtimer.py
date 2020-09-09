start_time = time.time()
seconds = 0.1

while True:
    current_time = time.time()
    elapsed_time = current_time - start_time

    if elapsed_time > seconds:
        for bomb in bombs:
            bomb["time"] -= 1
            if sqrt(bomb["current_time"]) - sqrt(bomb["time"]) > 1:
                bomb["current_time"] = bomb["time"]
                bomb["flicker"] = not bomb["flicker"]

            if bomb["time"] <= 0:
                
        break
