import random
import numpy as np

# a = np.random.rand(3,4)
# b = np.random.rand(1,4)
# a = np.array([[2,1],[1,3]])
# # c= a+b
# print(np.dot(a,a))
# # print(c)

# import numpy as np

vector1 = np.array([[1,2,3],[4,5,6]])
vector2 = np.array([4,5,6])

result = np.dot(vector1, vector2) + 8

# print(vector1.shape)
print(result)  # Kết quả: 32

# import numpy as np

# # Đặc trưng của mẫu dữ liệu
# # Ví dụ: hai đặc trưng, thêm một đặc trưng bias
# X = np.array([[1, 2, 1], [2, 3, 1], [3, 4, 1], [4, 5, 1]])

# # Trọng số của mô hình logistic regression
# # Ví dụ: ba trọng số tương ứng với ba đặc trưng và một trọng số cho đặc trưng bias
# weights = np.array([0.1, 0.2, 0.3])

# # Tính tổng trọng số cho mỗi mẫu dữ liệu
# # Sử dụng numpy.dot() để tính toán
# logit_scores = np.dot(X, weights)

# print(logit_scores)