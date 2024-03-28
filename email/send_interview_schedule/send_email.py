import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# config
stmp_server = '여기에_이메일_서버_주소를_입력'
smtp_port = 0  # <-- 여기에 이메일 서버 포트를 입력 (숫자)
smtp_username = '여기에_계정_이름을_입력'
stmp_password = '여기에_계정_비밀번호를_입력'

list_csv = 'list.csv'
mail_subject = "{name}님의 면접 일정을 알려드립니다"
mail_body = """안녕하세요 {name}님,
{name}님의 면접 일정은 본 회사에서 4월 13일 {time}입니다. 
(10분 전까지 회사 로비도착 요망)

궁금하신 사항이 있다면 회신 바랍니다.
감사합니다.
"""
############################################

def send_email(subject, body, to):
    """ 이메일을 발송합니다.
    Args:
        subject (str): 이메일 제목
        body (str): 이메일 본문
        to (str): 수신자 이메일 주소
    """
    msg = MIMEMultipart()
    msg['Sender'] = smtp_username
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(stmp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, stmp_password)
        server.send_message(msg)

def read_csv(file):
    """ CSV 파일을 읽어서 리스트로 반환합니다.
    Args:
        file (str): CSV 파일 경로
    Returns:
        list: CSV 파일 내용
    """
    result = []
    with open(file, 'r') as f:
        for line in f:
            temp = line.split(',')
            # 모든 데이터의 양쪽 공백을 제거합니다.
            for i in range(len(temp)):
                temp[i] = temp[i].strip()
            result.append(temp)
    return result

# 명단 불러오기
interview_list = read_csv(list_csv)
# 명단에 있는 사람(데이터) 각각에게 이메일 발송
for data in interview_list:
    # 데이터가 잘못된 경우 건너뜁니다.
    if len(data) != 3:
        print(f'잘못된 데이터: {data}')
        continue  # (잘못된) 이번 데이터 건너뛰기
    # 이름, 이메일, 시간 순으로 저장되어 있음으로 
    # 이를 각각 변수에 저장합니다.
    name, email, time = data
    # 제목 틀에 이름을 넣어서 제목을 만듭니다.
    subject = mail_subject.format(name=name)
    # 본문 틀에 이름과 시간을 넣어서 본문(body)을 만듭니다.
    body = mail_body.format(name=name, time=time)
    # 이메일 발송
    send_email(subject, body, email)
    print(f'{name}님에게 이메일 발송 완료')

print('모든 이메일 발송 완료')
