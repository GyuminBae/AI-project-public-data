import requests

def get_food_data(food_name: str):
    api_key = 'N3GAbEpG5hh7TOgjrr3SO7acjCz%2BAIgGdmNcz2eiqApIPE7Yh33D00a0PQfWcD6g2YV1gy7LyWzUC7v4SQlpPA%3D%3D'
    base_url = 'apis.data.go.kr/1471000/FoodNtrCpntDbInfo02'
    query_params = {
        'serviceKey': api_key,
        'FOOD_NM_KR': food_name,
        'numOfRows': 100,
        'pageNo': 1,
        'type': 'json'
    }
    url = f'http://{base_url}/getFoodNtrCpntDbInq02'
    url += '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()])
    response = requests.get(url)

    if response.status_code == 200:
        food_data = list(
            filter(
                lambda x: x['FOOD_NM_KR'] == food_name and x['SERVING_SIZE'].__contains__('g'),
                response.json()['body']['items']
            )
        )[0]
        nutrients = {
            'code': food_data['FOOD_CD'],
            'name': food_data['FOOD_NM_KR'],
            'reference_name': food_data['FOOD_REF_NM'],
            'serving_size': float(food_data['SERVING_SIZE'].replace('g', '')),
            'kcal': float(food_data['AMT_NUM1']),
            'carbohydrates': food_data['AMT_NUM6'],
            'protein': food_data['AMT_NUM3'],
            'fat': food_data['AMT_NUM4']
        }
        return nutrients
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def calculate_kcal_per_serving(weight, nutrients_data):
    return (weight / nutrients_data['serving_size']) * nutrients_data['kcal']

# Example usage
def example_usage():
    search_keyword = "찜닭"
    first = get_food_data(search_keyword)
    print(f"[{first['name']} 식품 영양 성분]")
    for key, value in first.items():
        print(f"{key}: {value}")
    print()
    print(f"[주어진 무게에 대한 칼로리 계산 예시 ({first['name']})]")
    weight = 174  # Example weight in grams
    kcal_per_serving = calculate_kcal_per_serving(weight, first)
    print(f"Weight: {weight}g, kcal: {kcal_per_serving:.2f} kcal")
    # print()
    # print("---[Search Results]---")
    # index = 0
    # for food in search_result:
    #     index += 1
    #     nutrients = extract_nutrient_data(food)
    #     print(f"({index}) {nutrients['name']} <{nutrients['reference_name']}> ({nutrients['code']}) - {nutrients['kcal']} kcal ({nutrients['serving_size']})")
