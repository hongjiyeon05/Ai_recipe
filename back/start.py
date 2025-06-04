import pandas as pd
from utils import normalize

recipes_df = pd.read_csv("data/recipes_cleaned.csv")
kurly_df = pd.read_csv("data/kurly_cleaned.csv")

def recommend_recipes(user_ingredients):
    user_ingredients = [normalize(i) for i in user_ingredients]

    results = []

    for _, row in recipes_df.iterrows():
        recipe_ings = eval(row['재료목록'])  # ['김치', '두부', ...]
        have = set(user_ingredients) & set(recipe_ings)
        missing = set(recipe_ings) - set(user_ingredients)

        if len(have) == 0:
            continue

        match_score = len(have) / len(recipe_ings)

        # 부족재료 상품 추천
        items = []
        for ing in missing:
            match = kurly_df[kurly_df['정규이름'].str.contains(ing, na=False)]
            for _, m in match.head(2).iterrows():
                items.append({
                    "재료명": ing,
                    "이름": m["이름"],
                    "가격": m["가격"],
                    "단위": m["단위"]
                })

        results.append({
            "메뉴": row['메뉴'],
            "매칭률": round(match_score, 2),
            "부족재료": list(missing),
            "레시피": row['레시피'],
            "추천상품": items
        })

    return sorted(results, key=lambda x: x['매칭률'], reverse=True)[:5]  # 상위 5개
