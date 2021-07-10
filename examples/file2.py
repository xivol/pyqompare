n_products = int(input())
products = set()

for _ in range(n_products):
    product = input()
    products.add(product)

nrecipe = int(input())
for _ in range(nrecipe):
    namerecipe = input()

    print(namerecipe, end=' ')