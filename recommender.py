import pandas as pd
from utils import normalize

recipes = pd.read_csv("C:/Users/hongy/OneDrive/Desktop/20241283 홍지연/ai융합개론/data/recipes.csv")
kurly = pd.read_csv("C:/Users/hongy/OneDrive/Desktop/20241283 홍지연/ai융합개론/data/kurly_cleaned.csv")

def recommend_recipes(user_ingredients):
    user_ingredients = [normalize(i) for i in user_ingredients]
    results = []

    for _, row in recipes.iterrows():
        recipe_ings = [normalize(i) for i in row["재료"
                                                 ].split(",")] # 리스트로 저장돼 있음
        have = set(user_ingredients) & set(recipe_ings)
        need = set(recipe_ings) - set(user_ingredients)

        if not have:
            continue

        match_score = len(have) / len(recipe_ings)

        # 부족재료 → 마켓컬리 추천상품 찾기
        items = []
        for ing in need:
            match = kurly[kurly['정규이름'].str.contains(ing, na=False)]
            for _, r in match.head(2).iterrows():
                items.append({
                    "재료명": ing,
                    "이름": r["이름"],
                    "가격": r["가격"],
                    "단위": r["단위"]
                })

        results.append({
            "메뉴": row['메뉴'],
            "매칭률": round(match_score, 2),
            "부족재료": list(need),
            "레시피": row['레시피'],
            "추천상품": items
        })

    return sorted(results, key=lambda x: x['매칭률'], reverse=True)[:5]
