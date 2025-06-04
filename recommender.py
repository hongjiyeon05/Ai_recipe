import pandas as pd
import os
from utils import normalize

# 현재 파일 기준 상대경로로 CSV 경로 설정
base_dir = os.path.dirname(__file__)
recipes_path = os.path.join(base_dir, "data", "recipes.csv")
kurly_path = os.path.join(base_dir, "data", "kurly_cleaned.csv")

recipes = pd.read_csv(recipes_path)
kurly = pd.read_csv(kurly_path)

def recommend_recipes(user_ingredients):
    user_ingredients = [normalize(i) for i in user_ingredients]
    results = []

    for _, row in recipes.iterrows():
        recipe_ings = [normalize(i) for i in row["재료"].split(",")]
        have = set(user_ingredients) & set(recipe_ings)
        need = set(recipe_ings) - set(user_ingredients)

        if not have:
            continue

        match_score = len(have) / len(recipe_ings)

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
