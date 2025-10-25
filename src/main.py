from src.manager import Manager



def main():
    mgr = Manager()
    while (exp := input("Введите свое выражение:")) and exp not in ["end", "q"]:
        if exp == "getall":
            mgr.get_all_tasks()
        else:
            mgr.add_task(exp)
    mgr.shutdown()

if __name__ == "__main__":
    main()
