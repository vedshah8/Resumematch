import spacy
from spacy.tokens import DocBin
from tqdm import tqdm
import json

def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return (data)

train_data = load_data("train.json")
test_data = load_data("test.json")

nlp = spacy.blank("en")
def create_training(TRAIN_DATA):
    db = DocBin()
    for text, annot in tqdm(TRAIN_DATA):
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in annot["entities"]:
            span = doc.char_span(start, end, label=label, alignment_mode="contract")
            if span is None:
                print ("Skipping entity")
            else:
                ents.append(span)
        doc.ents = ents
        db.add(doc)
    return(db)

train_data = create_training(train_data)
test_data = create_training(test_data)
train_data.to_disk("train.spacy")
test_data.to_disk("test.spacy")
