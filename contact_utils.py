import json
import uuid

def extract_name(text, spacy_model):
    doc = spacy_model(text) # przetwarzamy tekst jeszcze raz, korzystając z innego modelu
    names = [e for e in doc.ents if e.label_ == "persName"] # wybieramy nazwy osób
    try:
        the_name = names[0] # zakładamy że liczy się pierwsza wymieniona nazwa
    except IndexError:
        return None
    full_name = []
    for tok in the_name:
        full_name.append(tok.lemma_) # lematyzujemy nazwę
    full_name = " ".join(full_name)
    return full_name

def add_contact(name):
    new_id = str(uuid.uuid4())
    with open("contacts.json") as f: # zapisujemy nazwiska do pliku
        contact_data = json.load(f)
    new_contact = {"id": new_id, "name": name}
    contact_data.append(new_contact)
    with open("contacts.json", "w") as f:
        json.dump(contact_data, f)
