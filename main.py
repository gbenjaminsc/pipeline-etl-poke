import pandas as pd

import requests
import json

import openai

sdw2023_api_url = "https://pokeapi.co/"

openai_api_key = "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"
openai.api_key = openai_api_key

# EXTRACT
df = pd.read_csv("SDW2023.csv")
pokemon_ids = df["UserID"].tolist()
# print(pokemon_ids)

def get_pokemon(id):
    response = requests.get(f"{sdw2023_api_url}/api/v2/pokemon/{id}")
    return response.json() if response.status_code == 200 else None

pokemons = [pokemon for id in pokemon_ids if (pokemon := get_pokemon(id)) is not None]
# print(json.dumps(pokemons, indent=2))

# TRANSFORM
def generate_ai_info(pokemon):
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Voce entende tudo sobre pokemons"},
            {
                "role": "user",
                "content": f"Me passe algumas informações sobre o {pokemon['name']}",
            },
        ],
    )
    return completion.choices[0].message.content.strip('"')


for pokemon in pokemons:
    info = generate_ai_info(pokemon)
    print(info)
    pokemon["info"].append({"description": info})
# conta já estava com saldo usado não obtive resultado.

#LOAD
def update_pokemon(pokemon):
  response = requests.put(f"{sdw2023_api_url}/pokemon/{pokemon['id']}", json=pokemon)
  return True if response.status_code == 200 else False

for pokemon in pokemons:
  success = update_pokemon(pokemon)
  print(f"User {pokemon['name']} updated? {success}!")
# por se tratar de uma api pública  esse trecho de código não irá funcionar.

