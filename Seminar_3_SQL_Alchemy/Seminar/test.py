import random
faculties = {
        1: 'Факультет биологии', 2: 'Факультет истории',
        4: 'Факультет экономики'}
keys = []
for key, faculty in faculties.items():
    keys.append(key)

print(random.choice(keys))
