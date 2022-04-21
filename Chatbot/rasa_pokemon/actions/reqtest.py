from asyncore import dispatcher
from matplotlib.pyplot import title
import requests
import json
import asyncio

from rasa_sdk.executor import CollectingDispatcher


class getFromWiki:
    def getPokemon(self, name: str, dispatcher: CollectingDispatcher):
        print(dispatcher)
        pname_DE = json.loads(requests.get('https://raw.githubusercontent.com/sindresorhus/pokemon/main/data/de.json').text)
        pname_EN = json.loads(requests.get('https://raw.githubusercontent.com/sindresorhus/pokemon/main/data/en.json').text)
        for x in range(len(pname_DE)):
            if pname_DE[x] == name:
                pname_USE = pname_EN[x]
                name_given = pname_DE[x]
                break

        r = requests.get('https://pokeapi.co/api/v2/pokemon/' + pname_USE.lower())
        self.j = json.loads(r.text)
        dispatcher.utter_message("Name des Pokemon: " + name_given )
        dispatcher.utter_message("\n")
        self.getBasicInformation(dispatcher)
        self.getAbilities(dispatcher)
        self.getForms(dispatcher)

    def getAbilities(self, dispatcher):
        j = self.j
        abilities = j["abilities"]
        dispatcher.utter_message("\nAnzahl Fähigkeiten: " + str(len(abilities)) + "\n")
        if len(abilities) >= 1:
            a1 = abilities[0]
            a1_name = a1["ability"]["name"]
            a1_isHidden = a1["is_hidden"]
            a1_slot = a1["slot"]
            dispatcher.utter_message(text="Name: " + a1_name.title())
            a1_URL = a1["ability"]["url"]
            r_a1 = requests.get(a1_URL)
            j_a1 = json.loads(r_a1.text)
            for x in range(len(j_a1["effect_entries"])):
                a1_lang = j_a1["effect_entries"][x]["language"]["name"]
                if a1_lang == "en":
                    a1_lang_fallback = x
                if a1_lang == "de":
                    dispatcher.utter_message(text = "Effekt (Kurzform): " + j_a1["effect_entries"][x]["short_effect"])
                    dispatcher.utter_message(text = "Effekt: " + j_a1["effect_entries"][x]["effect"])
                if x >= len(j_a1):
                    dispatcher.utter_message(text = "Efffekt (Kurzform): " + j_a1["effect_entries"][a1_lang_fallback]["short_effect"])
                    dispatcher.utter_message(text = "Effekt: " + j_a1["effect_entries"][a1_lang_fallback]["effect"])
            if  a1_isHidden == False:
                a1_isHidden = "Nein"
            elif a1_isHidden == True:
                a1_isHidden = "Ja"
            dispatcher.utter_message(text = "Ist versteckt: " + str(a1_isHidden).title())
            dispatcher.utter_message( text = "Slot: " + str(a1_slot))
            dispatcher.utter_message(text = "\n")
        if len(abilities) >= 2:
            a2 = abilities[1]
            a2_name = a2["ability"]["name"]
            a2_isHidden = a2["is_hidden"]
            a2_slot = a2["slot"]
            if a2_isHidden == False:
                a2_isHidden = "Nein"
            elif a2_isHidden == True:
                a2_isHidden = "Ja"
            dispatcher.utter_message(text = "Name: " + a2_name.title())
            a2_URL = a2["ability"]["url"]
            r_a2 = requests.get(a2_URL)
            j_a2 = json.loads(r_a2.text)
            for x in range(len(j_a2["effect_entries"])):
                a2_lang = j_a2["effect_entries"][x]["language"]["name"]
                if a2_lang == "en":
                    a2_lang_fallback = x
                if a2_lang == "de":
                    dispatcher.utter_message(text= "Effekt (Kurzform): " + j_a2["effect_entries"][x]["short_effect"])
                    dispatcher.utter_message(text = "Effekt: " + j_a2["effect_entries"][x]["effect"])
                    break
                if x >= len(j_a2):
                    dispatcher.utter_message(text = "Efffekt (Kurzform): " + j_a2["effect_entries"][a2_lang_fallback]["short_effect"])
                    dispatcher.utter_message(text = "Effekt: " + j_a2["effect_entries"][a2_lang_fallback]["effect"])
            dispatcher.utter_message(text = "Ist versteckt: " + str(a2_isHidden).title())
            dispatcher.utter_message(text = "Slot: " + str(a2_slot))
            dispatcher.utter_message("")
        if len(abilities) >= 3:
            a3 = abilities[2]
            a3_name = a3["ability"]["name"]
            a3_isHidden = a3["is_hidden"]
            a3_slot = a3["slot"]
            dispatcher.utter_message(text = "Name: " + a3_name.title())
            a3_URL = a3["ability"]["url"]
            r_a3 = requests.get(a3_URL)
            j_a3 = json.loads(r_a3.text)
            for x in range(len(j_a3["effect_entries"])):
                a3_lang = j_a3["effect_entries"][x]["language"]["name"]
                if a3_lang == "en":
                    a3_lang_fallback = x
                if a3_lang == "de":
                    dispatcher.utter_message(text = "Effekt (Kurzform): " + j_a3["effect_entries"][x]["short_effect"])
                    dispatcher.utter_message(text = "Effekt: " + j_a3["effect_entries"][x]["effect"])
                    break
                if x >= len(j_a3):
                    dispatcher.utter_message(text = "Efffekt (Kurzform): " + j_a3["effect_entries"][a3_lang_fallback]["short_effect"])
                    dispatcher.utter_message(text = "Effekt: " + j_a3["effect_entries"][a3_lang_fallback]["effect"])
            if a3_isHidden == False:
                a3_isHidden  = "Nein"
            elif a3_isHidden == True:
                a3_isHidden = "Ja"
            dispatcher.utter_message(text = "Ist versteckt: " + str(a3_isHidden).title())
            dispatcher.utter_message(text = "Slot: " + str(a3_slot))

    def getBasicInformation(self, dispatcher):
        j = self.j
        base_exp = j["base_experience"]
        height = j["height"]
        id = j["id"]
        is_default = j["is_default"]
        en_name = j["name"]
        weight = j["weight"]
        dispatcher.utter_message(text = "Base EXP: " + str(base_exp))
        dispatcher.utter_message(text = "Höhe: " + str(height))
        dispatcher.utter_message(text = "ID: " + str(id))
        if is_default == True:
            is_default = "Ja"
        elif is_default == False:
            is_default = "Nein"
        dispatcher.utter_message(text = "Ist default-Pokemon für seine/ihre Spezies: " + str(is_default))
        dispatcher.utter_message(text = "Englischer Name: " + en_name)
        dispatcher.utter_message(text = "Gewicht: " + str(weight))

    def getForms(self, dispatcher):
        j = self.j
        forms = j["forms"]
        dispatcher.utter_message(text = "\n")
        dispatcher.utter_message(text = "Anzahl Formen: " + str(len(forms)))
        for x in range(len(forms)):
            dispatcher.utter_message(text = "\n")
            dispatcher.utter_message(text = "Form " + str(x+1) + ": " + forms[x]["name"].title())
            f_URL = forms[x]["url"]
            r_f = requests.get(f_URL)
            j_f = json.loads(r_f.text)
            f_id = j_f["id"]
            f_order = j_f["form_order"]
            f_is_default = j_f["is_default"]
            if f_is_default == True:
                f_is_default = "Ja"
            elif f_is_default == False:
                f_is_default = "Nein"
            f_is_battle_only = j_f["is_battle_only"]
            if f_is_battle_only == True:
                f_is_battle_only = "Ja"
            elif f_is_battle_only == False:
                f_is_battle_only = "Nein"
            f_is_mega = j_f["is_mega"]
            if f_is_mega == True:
                f_is_mega = "Ja"
            elif f_is_mega == False:
                f_is_mega = "Nein"
            dispatcher.utter_message(text = "ID: " + str(f_id))
            dispatcher.utter_message(text = "Reihenfolge in der Entwicklung eines Pokemon: " + str(f_order))
            dispatcher.utter_message(text = "Default-Form für Pokemon: " + str(f_is_default))
            dispatcher.utter_message(text = "Battle-only: " + str(f_is_battle_only))
            dispatcher.utter_message(text = "Mega-only: " + str(f_is_mega))
