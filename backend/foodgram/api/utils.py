def create_ingredients(model, data, recipe):
    """Creating ingredients for given recipe."""
    creation_list = []
    for ingredient in data:
        ingredient_id = ingredient.get('id')
        amount = ingredient.get('amount')
        creation_list.append(model(
            ingredient_id=ingredient_id,
            recipe_id=recipe,
            amount=amount
        ))
    model.objects.bulk_create(creation_list)


def create_tags(model, data, recipe):
    """Creating tags for given recipe."""
    creation_list = []
    for tag in data:
        creation_list.append(model(
            tag=tag,
            recipe_id=recipe
        ))
    model.objects.bulk_create(creation_list)
