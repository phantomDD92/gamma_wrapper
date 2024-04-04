def print_progress_bar(current: int, total: int, description: str = ""):
    percent = (current + 1) / total * 100
    print(
        "\r[{}{}] {:,.0%} -> {}".format(
            "#" * (current + 1), " " * (total - current - 1), percent, description
        ),
        end="",
    )
    if current + 1 == total:
        print()
