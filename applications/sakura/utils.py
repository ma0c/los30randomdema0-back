from applications.sakura import models


def load_categories():
    all_cards = models.Question.objects.all()
    for card in all_cards:
        category, _ = models.Category.objects.get_or_create(
            name=card.theme,
            slug=card.theme.lower().replace(' ', '-')
        )
        card.category = category
        card.save()


if __name__ == "__main__":
    load_categories()