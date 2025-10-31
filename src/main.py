from src.manager import Manager
from pprint import pprint



def main():
    mgr = Manager()
    while (exp := input("Введите свое выражение:")):
        if exp in ["end", "q"]:
            break
        if exp == "getall":
            pprint(mgr.get_all_tasks())
        else:
            mgr.add_task(exp)
    mgr.shutdown()

if __name__ == "__main__":
    main()
