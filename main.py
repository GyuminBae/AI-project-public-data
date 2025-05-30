import random
from fastapi import FastAPI, UploadFile, Form
from public_data import get_food_data, calculate_kcal_per_serving
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8000",
    ],  # 모든 출처 허용 (필요에 따라 특정 도메인으로 변경 가능)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)


@app.post("/calculate_kcal")
async def calculate_kcal_with_image(
    food_name: str = Form(..., description="음식 이름"),
    image: UploadFile = Form(..., description="음식 이미지")
):
    # 음식 데이터를 가져옴
    nutrients_data = get_food_data(food_name)
    if nutrients_data:
        # 음식 무게를 랜덤값으로 추정 (50g ~ 500g 사이)
        estimated_weight = random.uniform(50, 500)
        kcal = calculate_kcal_per_serving(estimated_weight, nutrients_data)
        return {
            "kcal": round(kcal, 2)
        }
    else:
        return {"error": "음식 데이터를 찾을 수 없습니다."}