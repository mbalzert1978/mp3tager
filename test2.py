dict_ = {"title": {"Art": "one"}}


def main():
    test = dict_.get("title").get("two")
    for item in (test,):
        if not item:
            continue
        print(item)
    print()


if __name__ == "__main__":
    main()
