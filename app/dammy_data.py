import models.favorites
import models.restaurants
import random
tmp1 = models.favorites.FavoriteModel()
tmp2 = models.restaurants.RestaurantModel()

for i in range(100):
  tmp1.create_fav(random.randint(2362304748, 2362304750), random.randint(1,100))

for i in range(1000):
  tmp2.create_restaurant(i + 1, 38.253834 + 0.001*i, 140.874074 + 0.001*i,"居酒屋", "a", "adress", "bud", "open", "park","https://www.hotpepper.jp/strJ001001485/")