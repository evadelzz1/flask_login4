import bcrypt, time

def test(_rounds):
    # 사용자로부터 입력받은 비밀번호
    password = "mysecretpassword"

    # 비밀번호를 바이트 문자열로 인코딩
    password_bytes = password.encode('utf-8')

    # 솔트 생성 시 사용할 라운드 수 지정 (default=12)
    salt = bcrypt.gensalt(rounds=_rounds)

    # 지정된 라운드 수로 해시 생성
    hashed_password = bcrypt.hashpw(
        password=password_bytes,
        salt=salt
    )

    print(f"Actual Password: {password_bytes.decode('utf-8')}")
    print(f"Hashed Password: {hashed_password.decode('utf-8')}")

    # 저장된 해시와 비밀번호 시도 비교
    if bcrypt.checkpw(password_bytes, hashed_password):
        print("Password is correct!")
    else:
        print("Password is incorrect!")

for i in range(10,17):
    start_time = time.time()
    test(i)
    end_time = time.time()
    print(f"### Cost Rounds : {i} --> {end_time - start_time} sec")

