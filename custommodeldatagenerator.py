import json
import shutil
import os
from pathlib import Path
import questionary

PACKMCMETA = """
{
  "pack": {
    "pack_format": 22,
    "description": "Generated by DrgnFireYellow's Custom Model Data Generator"
  }
}
"""


packname = questionary.text("Enter pack name").ask()
baseitem = questionary.text("Enter the item to base the custom model data on (for example diamond_sword)").ask()
modeltype = questionary.confirm("Is this item a tool?", False)
custommodeldatanumber = int(questionary.text("Enter the custom model data number for your custom model", "1").ask())
custommodel = questionary.path("Select model file", "./").ask()
customtexture = questionary.path("Select texture file for the model to use", "./").ask()
modelname = Path(custommodel).stem

if modeltype:
    modeltype = "handheld"
else:
    modeltype = "generated"


os.makedirs(os.path.join(packname, "assets", "minecraft", "models", "custom"))
os.mkdir(os.path.join(packname, "assets", "minecraft", "models", "item"))
os.mkdir(os.path.join(packname, "assets", "minecraft", "textures"))
os.mkdir(os.path.join(packname, "assets", "minecraft", "textures", "item"))

custommodeldata = {
  "parent": f"minecraft:item/{modeltype}",
  "textures": {
    "layer0": f"minecraft:item/{baseitem}"
  },
  "overrides": [
    {
      "predicate": {
        "custom_model_data": custommodeldatanumber
      },
      "model": f"minecraft:custom/{modelname}"
    }
  ]
}

with open(os.path.join(packname, "assets", "minecraft", "models", "item", f"{baseitem}.json"), "w") as custommodeldatafile:
    json.dump(custommodeldata, custommodeldatafile)

with open(custommodel) as modelfile:
    modeldata = json.load(modelfile)

modeldata["textures"]["0"] = f"item/{modelname}"
modeldata["textures"]["particle"] = f"item/{modelname}"


with open(os.path.join(packname, "assets", "minecraft", "models", "custom", f"{modelname}.json"), "w") as modeldatafile:
    json.dump(modeldata, modeldatafile)

shutil.copyfile(customtexture, os.path.join(packname, "assets", "minecraft", "textures", "item", f"{modelname}.png"))

with open(os.path.join(packname, "pack.mcmeta"), "w") as packmcmetafile:
    packmcmetafile.write(PACKMCMETA)

print("Done")
