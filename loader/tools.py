import os
import csv

import pandas as pd


def load_foreign_essays():
    with open(os.path.join("..", "essays-foreign.csv")) as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader]
    result = []
    current_essay = None
    for row in rows:
        if row["id эссе"] == "":
            current_essay = None
            continue
        if current_essay == None:
            current_essay = {
                "ix": None,
                "n_chars": 0,
                "orpho": 0,
                "punct": 0,
                "morph": 0,
                "lexic": 0,
                "syntax": 0,
                "complexity": None,
                "theme_matching": None,
                "coherence": None,
                "sentiment": None,
                "sentiment_reasoned": None,
                "total": None,
                "text": []
            }
            result.append(current_essay)
        if row["абзацы эссе"] == "<ОБЩАЯ ОЦЕНКА>":
            current_essay["ix"] = int(row["id эссе"])
            current_essay["complexity"] = int(row["сложность текста"])
            current_essay["theme_matching"] = int(row["соответствие теме"])
            current_essay["coherence"] = int(row["связность текста"])
            current_essay["sentiment"] = int(row["тип тональности"])
            current_essay["sentiment_reasoned"] = int(row["уместность тональности"])
            current_essay["total"] = int(row["оценка"])
            current_essay["orpho"] /= current_essay["n_chars"] / 100
            current_essay["punct"] /= current_essay["n_chars"] / 100
            current_essay["morph"] /= current_essay["n_chars"] / 100
            current_essay["lexic"] /= current_essay["n_chars"] / 100
            current_essay["syntax"] /= current_essay["n_chars"] / 100
            current_essay["text"] = "\n".join(current_essay["text"])
            continue
        current_essay["n_chars"] += len(row["абзацы эссе"].strip())
        current_essay["orpho"] += int(row["орфография"]) if row["орфография"] else 0
        current_essay["punct"] += int(row["пунктуация"]) if row["пунктуация"] else 0
        current_essay["morph"] += int(row["морфология"]) if row["морфология"] else 0
        current_essay["lexic"] += int(row["лексика и стилистика"]) if row["лексика и стилистика"] else 0
        current_essay["syntax"] += int(row["синтаксис"]) if row["синтаксис"] else 0
        current_essay["text"].append(row["абзацы эссе"].strip())
    return pd.DataFrame.from_records(result, index="ix")


def load_native_essays():
    df = pd.read_csv(os.path.join("..", "essays-native.csv"), index_col="id эссе")
    df = df.rename(columns={
        "тема": "topic",
        "текст": "text",
        "сложность текста": "complexity",
        "соответствие теме": "theme_matching",
        "связность текста": "coherence",
        "уместность тональности": "sentiment_reasoned",
        "оценка": "total",
        "грамотность": "spelling",
    })
    df.index.names = ["ix"]
    df["n_chars"] = df.text.map(lambda x: len(x.strip()))
    return df
