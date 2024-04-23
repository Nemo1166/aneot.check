from nerpy import NERModel
import 

ner = NERModel("bert", "shibing624/bert4ner-base-chinese")

ents = {
    "PER": [],
    "LOC": [],
    "ORG": [],
}

if __name__ == "__main__":
    with open('./test.txt', 'r') as f:
        paras = f.read().split('\n\n')
    predictions, raw_outputs, entities = ner.predict(paras)
    for item in entities:
        if len(item)>0:
            for ent in item:
                match ent[1]:
                    case 'PER':
                        ents['PER'].append(ent[0])
                    case 'LOC':
                        ents['LOC'].append(ent[0])
                    case 'ORG':
                        ents['ORG'].append(ent[0])
                    case _:
                        continue
    for k in ents.keys():
        ents[k] = list(set(ents[k]))
    print(ents)

