import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd

# 1. 데이터 로드 및 전처리
df = pd.read_csv("student_health_3.csv", encoding="cp949")
df = df[['학년', '수축기', '이완기', '키', '몸무게']].dropna()
df.columns = ['Grade', 'Upper', 'Lower', 'Height', 'Weight']

# Class 1: Grade 1~3, Class 2: Grade 4~6
df['Class'] = df['Grade'].apply(lambda x: 1 if x <= 3 else 2)

# 2. 특성과 타깃 분리
X = df[['Lower', 'Upper', 'Height', 'Weight']]
y = df['Class']

# 3. 학습/검증 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)

# 4. 모델 학습
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# 5. 주어진 입력값 예측

test_input = pd.DataFrame([[80, 100, 140, 60]], columns=['Lower', 'Upper', 'Height', 'Weight'])
predicted_class = model.predict(test_input)[0]
print(f"입력 [80, 100, 140, 60] 에 대한 예측 클래스: Class {predicted_class}")
