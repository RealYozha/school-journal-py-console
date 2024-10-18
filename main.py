import pandas as pd
from random import randint


def setup(t: pd.DataFrame) -> pd.DataFrame: # makes grades and adds parallels
    t = t.rename(columns={"variable": "letter", "value": "name"})
    t["math_grade"] = [randint(3, 5) for i in range(len(t["name"]))]
    t["russian_grade"] = [randint(3, 5) for i in range(len(t["name"]))]
    t["it_grade"] = [randint(3, 5) for i in range(len(t["name"]))]
    t["parallel"] = [9 if i % 2 == 1 else 10 for i in range(len(t["letter"]))]
    return t


def class_journal(learners_table: dict, sort_by: str, top_learners_amount: int): # sort_by: 'letter', 'parallel' or 'all'
    if sort_by == 'letter':
        print("Сортировка происходит по букве.")
    elif sort_by == 'parallel':
        print("Сортировка происходит по параллели.")
    elif sort_by == 'all':
        sort_by = ['parallel', 'letter']
        print("Сортировка происходит по параллели и букве.")
    else:
        sort_by = ['parallel', 'letter']
        print("[ВНИМАНИЕ] Способ сортировки указан неправильно.")
        print("Сортировка происходит по параллели и букве.")
    wide_learners = pd.DataFrame(learners_table)
    learners = wide_learners.melt()
    learners = setup(learners)
    learners["avg"] = round(((learners["math_grade"] + learners["russian_grade"] + learners["it_grade"]) / 3), 2)
    learners = learners[["parallel", "letter", "name", "avg", "math_grade", "russian_grade", "it_grade"]]
    learners = learners.sort_values(by="avg", ascending=False)
    top_learners = learners.head(top_learners_amount)
    avg_per_class = learners.groupby(by=sort_by).mean(numeric_only=True)
    math_count_per_class = learners.pivot_table(index=sort_by, columns='math_grade', values='name', fill_value=0, aggfunc='count')
    russian_count_per_class = learners.pivot_table(index=sort_by, columns='russian_grade', values='name', fill_value=0, aggfunc='count')
    it_count_per_class = learners.pivot_table(index=sort_by, columns='it_grade', values='name', fill_value=0, aggfunc='count')
    print(f"Лучшие {top_learners_amount} ученика (-ов):\n{top_learners}")
    print(f"Средняя оценка по классам:\n{avg_per_class}")
    print(f"Количество оценок 3, 4 и 5 по математике по классам:\n{math_count_per_class}")
    print(f"Количество оценок 3, 4 и 5 по русскому языку по классам:\n{russian_count_per_class}")
    print(f"Количество оценок 3, 4 и 5 по информатике по классам:\n{it_count_per_class}")


def main():
    raw_learners_table = {
        "А": [
            "Смирнов",
            "Кузнецов",
            "Соколов",
            "Козлов",
            "Морозов",
            "Сидоров",
            "Васильев",
            "Зайцев",
            "Павлов",
            "Богданов"
        ],
        "Б": [
            "Иванов",
            "Попов",
            "Лебедев",
            "Новиков",
            "Петров",
            "Волков",
            "Соловьёв",
            "Семёнов",
            "Голубев",
            "Фёдоров"
        ]
    }
    class_journal(raw_learners_table, 'all', 5)


if __name__ == '__main__':
    main()
