from django.utils.timezone import now


def get_book_cover_upload_path(instance, filename):
    date = now()
    book_name = instance.title.replace(" ", "_")
    path = "book_covers/{year}/{month}/{day}/{book_name}/{filename}".format(
        year=date.year,
        month=date.month,
        day=date.day,
        book_name=book_name,
        filename=filename,
    )
    return path
