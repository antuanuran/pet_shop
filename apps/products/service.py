# import csv
#
# from apps.products.models import Attribute, Catalog, Category, Item, ItemAttribute, Product


def import_data(data_stream, admin):
    print(data_stream)
    print(admin)

    # data = csv.DictReader(data_stream, delimiter=",")
    #
    # for entity in data:
    #     category, _ = Category.objects.get_or_create(name=entity["category"])
    #     product, _ = Product.objects.get_or_create(category_id=category.id, name=entity["product"])
    #     catalog, _ = Catalog.objects.get_or_create(product_id=product.id, name=entity["catalog"], admin_id=admin)
    #     attribute, _ = Attribute.objects.get_or_create(name=entity["attribute"], catalog_id=catalog.id)
    #     item, _ = Item.objects.get_or_create(
    #         catalog_id=catalog.id, price=entity["price"], count=entity["count"], upc=entity["upc"]
    #     )
    #     itemattribute, _ = ItemAttribute.objects.get_or_create(
    #         item_id=item.id, attribute_id=attribute.id, value=entity["value"]
    #     )
