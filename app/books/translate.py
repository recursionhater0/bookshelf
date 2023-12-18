from django_ftl.bundles import Bundle

bundle = Bundle(("books/main.ftl",))

ftl = bundle.format
ftl_lazy = bundle.format_lazy
