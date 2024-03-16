
def get_proxy():

    if not is_need_proxy():
        return

    return input_proxy()


def is_need_proxy():
    is_proxy = input("you need proxy(y/n)? ").strip()
    return is_proxy in ["y", "yes"]


def input_proxy():
    print()
    print(10 * "=")
    proxy = input("your proxy: ")
    print(10 * "=")
    print()
    return proxy


