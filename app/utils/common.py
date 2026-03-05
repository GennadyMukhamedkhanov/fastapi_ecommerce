def _correct_page(total, page, page_size):
    # Корректируем page, если он слишком большой
    max_page = max(1, (total + page_size - 1) // page_size)
    if page > max_page and total > 0:
        page = max_page
    return page
