import numpy as np

def user_based_recommendation(user_id, ratings, k):
    def pearson_correlation(user1, user2):    # 해당 사용자와 다른 사용자 간의 상관계수 계산
        # 공통으로 평가한 항목 찾기
        common_ratings = np.logical_and(user1 != 0, user2 != 0)
        if np.sum(common_ratings) == 0:
            return 0
        else:
            mean_user1 = np.mean(user1[common_ratings])
            mean_user2 = np.mean(user2[common_ratings])
            numerator = np.sum((user1[common_ratings] - mean_user1) * (user2[common_ratings] - mean_user2))
            denominator = np.sqrt(np.sum((user1[common_ratings] - mean_user1)**2)) * np.sqrt(np.sum((user2[common_ratings] - mean_user2)**2))
            if denominator == 0:
                return 0
            else:
                return numerator / denominator

    # 해당 사용자와 다른 사용자들 간의 상관계수 계산
    similar_users = []
    for i in range(len(ratings)):
        if i != user_id:
            similarity = pearson_correlation(ratings[user_id], ratings[i])
            similar_users.append((i, similarity))

    # 상관계수가 높은 상위 k명의 사용자 선택
    similar_users.sort(key=lambda x: x[1], reverse=True)
    similar_users = similar_users[:k]

    # 추천 음원 찾기
    recommendation = np.zeros(ratings.shape[1])
    for user, similarity in similar_users:
        recommendation += ratings[user] * similarity
 
    return recommendation

# 예제 데이터와 함수 호출
ratings = np.array([
    [5, 4, 0, 0, 4, 5],
    [4, 3, 4, 5, 4, 2],
    [2, 0, 1, 3, 0, 5],
    [5, 5, 0, 5, 4, 5],
    [5, 4, 4, 4, 5, 0]
])

user_id = 0  # 추천을 받고자 하는 사용자의 ID
k = 3  # 고려할 유사 사용자의 수

recommendation = user_based_recommendation(user_id, ratings, k)
recommendation = np.clip(recommendation, 0, 5)
recommendation = recommendation.round(1)
print(recommendation)  # 결과 출력
