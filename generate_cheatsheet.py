# -*- coding: utf8 -*-
"""
THIS MODULE HAS BEEN MADE BY LUDUK AT ningawent@gmail.com
PLEASE CONTACT BEFORE DISTRIBUTING AND OR MODIFYING THIS ON YOUR OWN ACCORD.

I, LUDUK, TAKE NO RESPONSIBILITY FOR ANY MISUES OF THIS MODULE.

also if you don't credit me you're a big meanie

!!!DISCLAIMER!!!
ALL INFORMATION CONTAINED IN THIS FILE HAS NOTHING TO DO WITH REAL LIFE.
ALL CHARACTERS DESCRIBED HERE ARE FICTIONARY.
ANY AND ALL SIMILARITIES ARE COMPLETELY COINCIDENTAL.
"""

"""
NOTA BENE
!!! NB !!!
! ! ! F U N ! ! !

DON'T TOUCH ANY OF THIS CODE OR PYTHON WILL EAT YOUR FACE
Unless you're here to refactor it and make it better, then please, do touch the code.
"""
#  _______ _    _ ______   ____ _____ _____   _______ ____  _____   ____  
# |__   __| |  | |  ____| |  _ \_   _/ ____| |__   __/ __ \|  __ \ / __ \
#    | |  | |__| | |__    | |_) || || |  __     | | | |  | | |  | | |  | |
#    | |  |  __  |  __|   |  _ < | || | |_ |    | | | |  | | |  | | |  | |
#    | |  | |  | | |____  | |_) || || |__| |    | | | |__| | |__| | |__| |
#    |_|  |_|  |_|______| |____/_____\_____|    |_|  \____/|_____/ \____/
#                                                                         
# The TODO list:
# - Make this code more presentable(please use OOP).
# - Make all the options into a config.

import itertools
import textwrap

from sys import exc_info
from traceback import print_exception


def reindent(s, amount, character = ' '):
  s = s.split("\n")
  s = [(amount * character) + line for line in s]
  s = "\n".join(s)
  return s

def reindent_not_first(s, amount, character = ' '):
  s = s.split("\n")
  ret = [s[0]]
  ret += [(amount * character) + line for line in s[1::]]
  ret = "\n".join(ret)
  return ret


EXPLANATION = """
~~~
hatreds -> corpuses

"Lightness":
Drone(Only if has E) -> Autominiton -> Light Automaton -> Automaton -> Heavy Automaton -> Dreadnaught(Only if has U) -> Rogue(Only if has UGHED)

if 0 lightness -> autodrone + DISARM_TRAPS_SKILL
if can not autodrone while having 1 lightness too low -> autominiton          + SPEED
if can not dreadnaught or rogue while having > 6 lightness -> heavy automaton + DAM_BONUS(+DEF_BONUS too if 7)

resolve incompatibilities:
"Heavy Stone" -> Stone Automaton + DEF_BONUS
"Light Wood" -> Wood Automaton   + DISARM_TRAPS_SKILL
"Heavy Wood" -> Wood Automaton   + MELEE_RESISTANCE

Resources:
Wood -> Stone -> Iron

Undead: Flesh(Wood)
Greenskins: Stone
Humans: Wood
Elves: Wood
Dwarves: Iron

"Lightness tier" = number of letters + (+1 if undead) + (+1 if humans) + (-1 if elves)
~~~
"""

EFFECTS_WRAPPER = """Area 30 Filter AUTOMATON Filter ALLY FilterLasting SUMMONED FirstSuccessful {
    FilterLasting HATE_HUMANS Chain {
      Permanent UNSTABLE
      RemovePermanent UNSTABLE
    }
    FilterLasting HATE_ELVES Chain {
      Permanent UNSTABLE
      RemovePermanent UNSTABLE
    }
    FilterLasting HATE_DWARVES Chain {
      Permanent UNSTABLE
      RemovePermanent UNSTABLE
    }
    FilterLasting HATE_GREENSKINS Chain {
      Permanent UNSTABLE
      RemovePermanent UNSTABLE
    }
    FilterLasting HATE_UNDEAD Chain {
      Permanent UNSTABLE
      RemovePermanent UNSTABLE
    }

    Chain {
@EFFECT_STR_HERE@
    }
  }"""
AUTOMATON_WITH_EFFECTS_WRAPPER = """@FILTERS_STR_HERE@Chain {
  @SUMMON_STR_HERE@
  @EFFECTS_WRAPPER_HERE@
}"""

HATREDS = ["U", "G", "H", "E", "D"]

HATREDS_FULL = {
  "U": "HATE_UNDEAD",
  "G": "HATE_GREENSKINS",
  "H": "HATE_HUMANS",
  "E": "HATE_ELVES",
  "D": "HATE_DWARVES"
}

MATERIALS = ["WOOD", "STONE", "IRON"]

MATERIAL_TIERS = {
  "WOOD": 1,
  "STONE": 2,
  "IRON": 3
}

ADJUST_MATERIAL = {
  "U": "WOOD",
  "G": "STONE",
  "H": "WOOD",
  "E": "WOOD",
  "D": "IRON"
}

LIGHTNESS_TIERS = [
  "AUTODRONE_CORPUS", "AUTOMINITON_CORPUS", "LIGHT_AUTOMATON_CORPUS", "AUTOMATON_CORPUS",
  "HEAVY_AUTOMATON_CORPUS", "DREADNAUGHT_CORPUS", "ROGUE_DREADNAUGHT"
]

LIGHTNESS_HATRED_REQUIREMENT = {
  "AUTODRONE_CORPUS": "E",
  "DREADNAUGHT_CORPUS": "U",
  "ROGUE_DREADNAUGHT": "UGHED"
}

LIGHTNESS_GLOBAL_MIN = 0

LIGHTNESS_HATRED_MIN = {
  "U": 1,
  "G": 1,
  "H": 1,
  "E": 0,
  "D": 1
}

LIGHTNESS_HATRED_MAX = {
  "U": 5,
  "G": 5,
  "H": 5,
  "E": 5,
  "D": 7
}

LIGHTNESS_HATRED_REQUIREMENT_FAILED = {
  "AUTODRONE_CORPUS": "NO_HATRED_TOO_LIGHT",
  "DREADNAUGHT_CORPUS": "NO_HATRED_TOO_HEAVY",
  "ROGUE_DREADNAUGHT": "NO_HATRED_TOO_HEAVY"
}

ADJUST_LIGHTNESS = {
  "U": 1,
  "G": 0,
  "H": 1,
  "E": -1,
  "D": 0
}

# The lighter - the further in the list.
TOO_LIGHT_EFFECTS = ["DISARM_TRAPS_SKILL"]
TOO_LIGHT_CORPUS = "AUTODRONE_CORPUS"

NO_HATRED_TOO_LIGHT_EFFECTS = ["SPEED"]
NO_HATRED_TOO_LIGHT_CORPUS = "AUTOMINITON_CORPUS"

# The heavier - the further in the list.
NO_HATRED_TOO_HEAVY_EFFECTS = ["DEF_BONUS", "DAM_BONUS"]
NO_HATRED_TOO_HEAVY_CORPUS = "HEAVY_AUTOMATON_CORPUS"

MATERIAL_INCOMPATIBLE_CORPUSES = {
  "WOOD": ["LIGHT_AUTOMATON_CORPUS", "HEAVY_AUTOMATON_CORPUS"],
  "STONE": ["HEAVY_AUTOMATON_CORPUS"],
}

MATERIAL_INCOMPATIBLE_CORPUSES_RESOLVE = {
  "LIGHT_AUTOMATON_CORPUS_WOOD": "AUTOMINITON_CORPUS",
  "HEAVY_AUTOMATON_CORPUS_WOOD": "AUTOMATON_CORPUS",
  "HEAVY_AUTOMATON_CORPUS_STONE": "AUTOMATON_CORPUS"
}

MATERIAL_INCOMPATIBLE_CORPUSES_EFFECTS = {
  "LIGHT_AUTOMATON_CORPUS_WOOD": ["DISARM_TRAPS_SKILL"],
  "HEAVY_AUTOMATON_CORPUS_WOOD": ["MELEE_RESISTANCE"],
  "HEAVY_AUTOMATON_CORPUS_STONE": ["DEF_BONUS"]
}

TAGS_BY_HATRED = {
  "U": set(["Head", "Fire", "Sharp"]),
  "G": set(["Arms", "Acid", "Sharp", "Big"]),
  "H": set(["Head", "Humanoid"]),
  "E": set(["Legs", "Range", "Small", "Arcane"]),
  "D": set(["Arms", "Forge", "Mine"])
}

TAGS_BY_PART = {
  "HumanoidHead": set(["Head", "Humanoid"]),
  "ArcherHead": set(["Head", "Range"]),
  "AutomatonLegs": set(["Legs"]),
  "AutomatonArms": set(["Arms"]),
  "DrillAutomatonArms": set(["Arms", "Mine"]),

  "HumanoidHead": set(["Head", "Humanoid"]),
  "ArcherHead": set(["Head", "Range"]),
  "FireHead": set(["Head", "Fire", "Range"]),
  "AcidHead": set(["Head", "Acid", "Range"]),
  "AutomatonLegs": set(["Legs"]),
  "AutomatonArms": set(["Arms"]),
  "DrillAutomatonArms": set(["Arms", "Mine"]),

  "HumanoidHead": set(["Head", "Humanoid"]),
  "ArcherHead": set(["Head", "Range"]),
  "FireHead": set(["Head", "Fire", "Range"]),
  "AcidHead": set(["Head", "Acid", "Range"]),
  "AutomatonLegs": set(["Legs"]),
  "AutomatonArms": set(["Arms"]),
  "SharpAutomatonArms": set(["Arms", "Sharp"]),
  "RepairAutomatonArms": set(["Arms", "Forge"]),
  "CannonballAutomatonArms": set(["Arms", "Forge", "Range", "Big"]),
  "DrillAutomatonArms": set(["Arms", "Mine"])
}

MATERIAL_ALLOWED_PARTS = {
  "WOOD": [
    "HumanoidHead", "ArcherHead", "AutomatonLegs", "AutomatonArms", "DrillAutomatonArms"
  ],
  "STONE": [
    "HumanoidHead", "ArcherHead", "FireHead", "AcidHead", "AutomatonLegs", "AutomatonArms",
    "DrillAutomatonArms"
  ],
  "IRON": [
    "HumanoidHead", "ArcherHead", "FireHead", "AcidHead", "AutomatonLegs", "AutomatonArms",
    "SharpAutomatonArms", "RepairAutomatonArms", "CannonballAutomatonArms",
    "DrillAutomatonArms"
  ]
}

def generate_possible_words():
  ret = []
  for i in range(len(HATREDS), 0, -1):
    ret += [list(e) for e in itertools.combinations(HATREDS, i)]
  return ret


def lightness_formula(word):
  ret = len(word)
  for symbol in word:
    ret += ADJUST_LIGHTNESS[symbol]
  return ret


def get_material(word):
  ret = None
  cur_tier = 0
  for symbol in word:
    new_mat = ADJUST_MATERIAL[symbol]
    new_tier = MATERIAL_TIERS[new_mat]
    if new_tier > cur_tier:
      ret = new_mat
      cur_tier = new_tier
  return ret


def generate_automaton(word):
  ret = {"word": word, "corpus": "", "material": "", "effects": []}

  light = lightness_formula(word)
  sanitized_light = max([min([light, len(LIGHTNESS_TIERS)]), 0])

  corpus = LIGHTNESS_TIERS[sanitized_light]
  corpus_failure = None
  if corpus in LIGHTNESS_HATRED_REQUIREMENT.keys():
    if LIGHTNESS_HATRED_REQUIREMENT[corpus].find("".join(word)) == -1:
      corpus_failure = LIGHTNESS_HATRED_REQUIREMENT_FAILED[corpus]

      if corpus_failure == "NO_HATRED_TOO_LIGHT":
        failure = abs(light - min([LIGHTNESS_HATRED_MIN[h] for h in word]))
        failure = min([abs(light), len(NO_HATRED_TOO_LIGHT_EFFECTS) - 1])
        ret["effects"].append(NO_HATRED_TOO_LIGHT_EFFECTS[failure])
        corpus = NO_HATRED_TOO_LIGHT_CORPUS
      elif corpus_failure == "NO_HATRED_TOO_HEAVY":
        failure = abs(light - min([LIGHTNESS_HATRED_MAX[h] for h in word]))
        failure = min([abs(light), len(NO_HATRED_TOO_HEAVY_EFFECTS) - 1])
        ret["effects"].append(NO_HATRED_TOO_HEAVY_EFFECTS[failure])
        corpus = NO_HATRED_TOO_HEAVY_CORPUS

  if light <= LIGHTNESS_GLOBAL_MIN:
    too_light = min([abs(light), len(TOO_LIGHT_EFFECTS) - 1])
    ret["effects"].append(TOO_LIGHT_EFFECTS[too_light])
    corpus = TOO_LIGHT_CORPUS

  material = get_material(word)
  if material in MATERIAL_INCOMPATIBLE_CORPUSES.keys():
    if corpus in MATERIAL_INCOMPATIBLE_CORPUSES[material]:
      ret["effects"] += MATERIAL_INCOMPATIBLE_CORPUSES_EFFECTS[corpus + "_" + material]
      corpus = MATERIAL_INCOMPATIBLE_CORPUSES_RESOLVE[corpus + "_" + material]

  ret["corpus"] = corpus
  ret["material"] = material
  return ret


def generate_automatons(words):
  ret = []
  for word in words:
    ret.append(generate_automaton(word))
  return ret


def format(automaton):
  effect_str = ""
  first = True
  for effect in automaton["effects"]:
    if not first:
      effect_str += ", "
    effect_str += effect
    first = False
  return "(" + "".join(automaton["word"]) + ") " + automaton["corpus"] + "_" + automaton["material"] + " [" + effect_str + "]"


def format_summon_cmd(automaton):
  summon_command = ""
  filters = ""
  for symbol in automaton["word"]:
    filters += "FilterLasting " + HATREDS_FULL[symbol] + " "
  summon_command += "Summon \"" + automaton["corpus"] + "_" + automaton["material"] + "\" {1} 2000 # " + "".join(automaton["word"])

  if len(automaton["effects"]) > 0:
    effect_str = ""
    embed = ""
    first = True
    for effect in automaton["effects"]:
      if not first:
        embed += "\n"
      embed += "Permanent " + effect
      first = False
    effect_str = EFFECTS_WRAPPER.replace("@EFFECT_STR_HERE@", reindent(embed, 6))

    ret = AUTOMATON_WITH_EFFECTS_WRAPPER.replace("@FILTERS_STR_HERE@", filters)
    ret = ret.replace("@SUMMON_STR_HERE@", summon_command)
    ret = ret.replace("@EFFECTS_WRAPPER_HERE@", effect_str)
    return ret

  return filters + summon_command


def header(f):
  f.write(EXPLANATION + "\n")


def output_combos(f, automatons):
  for automaton in automatons:
    f.write(format(automaton) + "\n")

def output_summon_commands(f, automatons):
  for automaton in automatons:
    f.write(format_summon_cmd(automaton) + "\n")


CONSTRUCT_HATRED_ORDER = ["HATE_HUMANS", "HATE_ELVES", "HATE_DWARVES", "HATE_GREENSKINS", "HATE_UNDEAD"]

SPELL_WRAPPER = """\"construct automatons @NUMBER@\"
{@UPGRADE_STR@
  symbol = "🛠"
  cooldown = 5
  sound = TRAP_ARMING
  effect = Name "construct automatons(@NUMBER@)" Description "Depending on your hatreds construct up to @NUMBER@ automaton@NUMBER_S@. If trying to construct more - first constructed will dissapear." Chain {
    @PROMOTE_ROUTINE_HERE@
    FirstSuccessful {
@SUMMON_ROUTINE_HERE@
    }
    # Find the newly spawned one, he has no hatreds.
    Area 30 Filter AUTOMATON Filter ALLY FilterLasting SUMMONED FirstSuccessful {
      FilterLasting HATE_HUMANS Chain {
        Permanent UNSTABLE
        RemovePermanent UNSTABLE
      }
      FilterLasting HATE_ELVES Chain {
        Permanent UNSTABLE
        RemovePermanent UNSTABLE
      }
      FilterLasting HATE_DWARVES Chain {
        Permanent UNSTABLE
        RemovePermanent UNSTABLE
      }
      FilterLasting HATE_GREENSKINS Chain {
        Permanent UNSTABLE
        RemovePermanent UNSTABLE
      }
      FilterLasting HATE_UNDEAD Chain {
        Permanent UNSTABLE
        RemovePermanent UNSTABLE
      }

      # Make them the first in order automaton.
      Permanent HATE_HUMANS
    }
  }
}"""

PROMOTE_ROUTINE_STOPPER = "Area 30 Filter AUTOMATON Filter ALLY FilterLasting SUMMONED FilterLasting @HATE_CURRENT@ Suicide DIE"

PROMOTE_ROUTINE_START = "Area 30 Filter AUTOMATON Filter ALLY FilterLasting SUMMONED FilterLasting @HATE_CURRENT@ @RECURSION_STR@"
PROMOTE_ROUTINE_STOPPER = "Suicide DIE"

PROMOTE_ROUTINE_RECURSIVE = """Chain {
  Area 30 Filter AUTOMATON Filter ALLY FilterLasting SUMMONED FilterLasting @HATE_CURRENT@ @RECURSION_STR@
  Permanent @HATE_NEXT@
  RemovePermanent @HATE_CURRENT@
}"""

def output_construct_spells(f, automatons, N=5):
  class BreakLoop(Exception):
    pass

  for i in range(1, N + 1):
    number = i
    number_s = "" if N == 1 else "s"
    upgrade_str = ""
    if number < N:
      upgrade_str = "\n  upgrade = \"construct automatons "+ str(number + 1) + "\""


    promote_routine = PROMOTE_ROUTINE_START
    try:
      promote_identation = 0
      loop = 0
      for hatred in CONSTRUCT_HATRED_ORDER:
        hate_current = CONSTRUCT_HATRED_ORDER[loop]
        hate_next = CONSTRUCT_HATRED_ORDER[loop + 1]

        promote_routine = promote_routine.replace("@HATE_CURRENT@", hate_current)
        promote_routine = promote_routine.replace("@HATE_NEXT@", hate_next)

        if loop == number - 1 or loop == len(CONSTRUCT_HATRED_ORDER) - 2:
          promote_routine = promote_routine.replace("@RECURSION_STR@", PROMOTE_ROUTINE_STOPPER)
          promote_routine = promote_routine.replace("@HATE_CURRENT@", hate_next)
          raise BreakLoop
        loop += 1

        promote_identation += 2
        promote_routine = promote_routine.replace("@RECURSION_STR@", reindent_not_first(PROMOTE_ROUTINE_RECURSIVE, promote_identation))
    except BreakLoop:
      pass

    summon_routine = ""
    first = True
    for automaton in automatons:
      if not first:
        summon_routine += "\n"
      summon_routine += format_summon_cmd(automaton)
      first = False

    ret = SPELL_WRAPPER.replace("@NUMBER@", str(number))
    ret = ret.replace("@NUMBER_S@", number_s)
    ret = ret.replace("@UPGRADE_STR@", upgrade_str)
    ret = ret.replace("@SUMMON_ROUTINE_HERE@", reindent(summon_routine, 6))
    ret = ret.replace("@PROMOTE_ROUTINE_HERE@", promote_routine)

    f.write(ret + "\n")


def format_part(part):
  if part["part"] is None:
    return "(" + "".join(part["word"]) + ") !!! EMPTY !!!"
  return "(" + "".join(part["word"]) + ") " + part["part"] + part["material"].lower().capitalize()


def format_spawn_part_cmd(part):
  if part["part"] is None:
    return ""
  part_str = "AddAutomatonParts { { Simple \"" + part["part"] + part["material"].lower().capitalize() + "\" } } # " + "".join(part["word"]) + "\n"
  filters = ""
  for symbol in part["word"]:
    filters += "FilterLasting " + HATREDS_FULL[symbol] + " "
  return "Caster " + filters + "Area 1 Filter AUTOMATON Filter ALLY FilterLasting SUMMONED FilterLasting FAST_TRAINING " + part_str


def generate_automaton_part(word):
  part_tags = set()
  for h in word:
    part_tags.update(TAGS_BY_HATRED[h])

  chosen_part = {"word": word, "part": None, "material": None}

  material = get_material(word)
  if material in MATERIAL_ALLOWED_PARTS.keys():
    max_similarity = 0
    for part_name in MATERIAL_ALLOWED_PARTS[material]:
      allowed_tags = TAGS_BY_PART[part_name]
      if allowed_tags.issubset(part_tags):
        if len(allowed_tags) == len(part_tags):
          return {"word": word, "part": part_name, "material": material}

        if len(allowed_tags) > max_similarity:
          max_similarity = len(allowed_tags)
          chosen_part = {"word": word, "part": part_name, "material": material}

  return chosen_part


def generate_automaton_parts(words):
  ret = []
  for word in words:
    ret.append(generate_automaton_part(word))
  return ret 


def output_part_combos(f, parts):
  for part in parts:
    f.write(format_part(part) + "\n")

def output_spawn_parts(f, parts):
  for part in parts:
    if part is None:
      continue
    f.write(format_spawn_part_cmd(part))

SPELL_CONSTRUCT_PART = """\"construct part\"
{
  symbol = \"🔨\"
  cooldown = 0
  range = 1
  effect = Chain {
    # Mark the target with FAST_TRAINING so Caster knows whom to put the part on.
    Permanent FAST_TRAINING

    FirstSuccessful {
    @CONSTRUCT_STR_HERE@

      # Fallback, if no proper hatreds are found - install legs. Everybody needs them.
      # !!! NB !!! fallback removed:
      # 1) it would cast without needing for corpse beer
      # 2) it doesn't make much sense 
      # AddAutomatonParts { { Simple "AutomatonLegsIron" } }
    }

    RemovePermanent FAST_TRAINING
  }
}"""

def output_construct_part_spell(f, parts):
  construct_str_here = ""
  for part in parts:
    construct_str_here += reindent(format_spawn_part_cmd(part), 4)

  f.write(SPELL_CONSTRUCT_PART.replace("@CONSTRUCT_STR_HERE@", construct_str_here))


if __name__ == "__main__":
  try:
    words = generate_possible_words()
    automatons = generate_automatons(words)
    parts = generate_automaton_parts(words)
    with open("automaton_doc.txt", "w", encoding="utf-8") as f:
        # header(f)
        output_combos(f, automatons)
        # output_summon_commands(f, automatons)
        # output_construct_spells(f, automatons)
        output_part_combos(f, parts)
        # output_spawn_parts(f, parts)
        # output_construct_part_spell(f, parts)
  except Exception as err:
    try:
      exc_info = exc_info()
    finally:
      # Display the *original* exception
      print(err)
      print_exception(*exc_info)
      del exc_info
  i = input()
