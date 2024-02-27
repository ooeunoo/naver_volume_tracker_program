from openai import OpenAI

class ChatGptHandler:
    def __init__(self, api_key):
        self.client = OpenAI(
            api_key=api_key,
        )

    def ask_keyword_question(self, forms):
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=forms
        )
        return completion.choices[0].message.content

    def generate_train_form(self, train_question, train_answer, real_question):
        return  [   {"role": "system","content": "You are a helpful assistant."},
                    {"role": "user","content": "나는 온라인 쇼핑몰의 상품을 소싱하고 있어. 키워드를 변환시키는 작업이 필요해. 세부적이지않은 키워드로 변경하는거야, 답변은 json포맷으로 줘"},
                    {"role": "user","content": '["휴대용 태양광 발전기 시스템","웨어러블 헬스 모니터링 밴드","생체 인식 보안 지문 잠금 장치","자동차용 블루투스 디스플레이 시스템","무선 충전 기능을 갖춘 스마트폰 케이스"]'},
                    {"role": "assistant","content": '[{"original": "휴대용 태양광 발전기 시스템", "main": "태양광 발전기 시스템"},{"original": "웨어러블 헬스 모니터링 밴드", "main": "헬스 밴드"},{"original": "생체 인식 보안 지문 잠금 장치", "main": "생체 인식 지문 잠금 장치"},{"original": "자동차용 블루투스 디스플레이 시스템","main": "자동차용 블루투스 디스플레이"},{"original": "무선 충전 기능을 갖춘 스마트폰 케이스","main": "무선 충전 케이스"}]'},
                    {"role": "user","content": '["스마트폰용 가상 현실 VR (가상현실) 헤드셋","무선 이어폰과 호환되는 블루투스 헤드폰","스마트홈 IoT 기반 가전 제어 시스템","안드로이드 및 iOS 스마트폰 호환 가능한 스마트 워치","생체 인식 안전 도어 잠금 장치","태블릿 컴퓨터와 호환되는 무선 키보드"]'},
                    {"role": "assistant", "content": '[{"original": "스마트폰용 가상 현실 VR (가상현실) 헤드셋","main": "VR 헤드셋"},{"original": "무선 이어폰과 호환되는 블루투스 헤드폰",  "main": "블루투스 헤드폰"},{"original": "스마트홈 IoT 기반 가전 제어 시스템", "main": "가전 제어 시스템"},{"original": "안드로이드 및 iOS 스마트폰 호환 가능한 스마트 워치", "main": "스마트 워치"},{"original": "생체 인식 안전 도어 잠금 장치", "main": "생체 인식 도어 잠금 장치"},{"original": "태블릿 컴퓨터와 호환되는 무선 키보드", "main": "무선 키보드"}]'},
                    {"role": "user", "content": f"'{train_question}'"},
                    {"role": "assistant", "content": f"'{train_answer}'"},
                    {"role": "user", "content": f"'{real_question}'"},
                ]
                


# 예제 사용
if __name__ == "__main__":
    pass