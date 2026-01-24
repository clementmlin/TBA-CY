# TBA

Ce repo contient la première version (minimale) du jeu d’aventure TBA.

Les lieux sont au nombre de 6. Il n'y a pas encore d’objets ni de personnages autres que le joueur et très peu d’interactions. Cette première version sert de base à ce qui va suivre, et sera améliorée au fur et à mesure.


## Structuration

Il y a pour le moment 5 modules contenant chacun une classe.

- `game.py` / `Game` : description de l'environnement, interface avec le joueur ;
- `room.py` / `Room` : propriétés génériques d'un lieu  ;
- `player.py` / `Player` : le joueur ;
- `command.py` / `Command` : les consignes données par le joueur ;
- `actions.py` / `Action` : les interactions entre .





# 🕵️ TBA – Text Based Adventure : Enquête à la Bibliothèque

Un **jeu d'aventure textuel (Text-Based Adventure)** développé en **Python**, proposant une **enquête immersive** dans une bibliothèque mystérieuse.  
Le joueur doit explorer les salles, interroger les suspects, collecter des indices et résoudre un meurtre.


---
##  Diagramme Mermaid


```mermaid
classDiagram

Game --> Player
Game --> Room
Game --> Command
Game --> Actions

Player --> QuestManager
Player --> Item
Player --> Room

QuestManager --> Quest

Room --> Item
Room --> Character

Command --> Actions

class Game {
  +rooms
  +player
  +current_room
  +commands
  +play()
  +process_command()
}

class Player {
  +name
  +current_room
  +history
  +inventory
  +move()
  +back()
}

class Room {
  +name
  +description
  +exits
  +items
  +characters
}

class Character {
  +name
  +dialog
  +alibi
  +guilty
  +talk()
  +accuse()
}

class Item {
  +name
  +description
  +weight
}

class Quest {
  +title
  +objectives
  +reward
  +activate()
  +complete_objective()
}

class QuestManager {
  +quests
  +active_quests
  +activate_quest()
  +check_objectives()
}

class Command {
  +command_word
  +help_string
  +action
}
```

---



##  Perspectives de développement

Plusieurs axes d’amélioration ont été identifiés afin d’enrichir l’expérience de jeu et d’améliorer la qualité globale du projet :

###  Interface graphique
L’interface graphique a été partiellement développée. Cependant, en raison de nombreux problèmes techniques impactant le code de base, nous avons décidé de suspendre temporairement son développement afin de garantir la stabilité du jeu.

Dans une perspective future, nous souhaitons :
- résoudre ces problèmes structurels,
- optimiser l’architecture du projet,
- et proposer aux utilisateurs une véritable interface graphique complète, fluide et ergonomique, améliorant significativement l’immersion.

---

###  Carte du jeu et level design
Nous souhaitons proposer une carte plus élaborée et immersive, intégrant une verticalité (étages, sous-sols, escaliers, ascenseurs, etc.).  
Cette évolution permettrait :
- d’enrichir l’exploration,
- de complexifier les déplacements,
- et d’augmenter la profondeur du gameplay, améliorant ainsi le plaisir de jeu.

---

###  Quêtes secondaires et progression
Concernant les quêtes secondaires, nous aurions souhaité créer un véritable lien de dépendance entre elles, en mettant en place un système de récompenses influençant directement leur faisabilité.

Par exemple :
- certaines quêtes ne pourraient être accessibles qu’après l’obtention d’objets ou de compétences spécifiques,
- les récompenses pourraient débloquer de nouvelles zones, interactions ou dialogues.

Cela permettrait de renforcer la cohérence scénaristique, la progression du joueur et la dimension stratégique du jeu.

