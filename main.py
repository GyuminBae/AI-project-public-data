import os
import uuid
import random
from fastapi import FastAPI, UploadFile, Form
from public_data import get_food_data, calculate_kcal_per_serving
#from estimation import estimate_weight
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
    save_directory = "uploaded_images"
    os.makedirs(save_directory, exist_ok=True)  # 디렉토리가 없으면 생성

    # UUID로 파일 이름 생성
    file_extension = image.filename.split('.')[-1]  # 원본 파일 확장자 추출
    unique_filename = f"{uuid.uuid4()}.{file_extension}"  # UUID 기반 파일 이름 생성
    file_path = os.path.join(save_directory, unique_filename)

    # 파일 데이터를 읽고 저장
    with open(file_path, "wb") as file:
        file.write(await image.read())

    nutrients_data = get_food_data(food_name)
    if nutrients_data:
        estimated_weight = random.uniform(50, 500)
        kcal = calculate_kcal_per_serving(estimated_weight, nutrients_data)
        return {
            "kcal": round(kcal, 2)
        }
    else:
        return {"error": "음식 데이터를 찾을 수 없습니다."}