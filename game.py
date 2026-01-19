from pathlib import Path
import sys

# Tkinter imports for GUI
import tkinter as tk
from tkinter import ttk, simpledialog



from room import Room
from player import Player
from command import Command
from actions import Actions
from character import Character
from item import Item
from quest import Quest

class Game:

    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.current_room = None
        

    def setup(self):


        # ---------- COMMANDES ----------
        self.commands["help"] = Command("help", ": afficher cette aide", Actions.help, 0)
        self.commands["quit"] = Command("quit", ": quitter le jeu", Actions.quit, 0)
        self.commands["go"] = Command("go", "<direction> : se déplacer (N,E,S,O)", Actions.go, 1)
        self.commands["look"] = Command("look", ": observer la salle", Actions.look, 0)
        self.commands["history"] = Command("history", ": afficher l’historique", Actions.history, 0)
        self.commands["back"] = Command("back", ": revenir à la salle précédente", Actions.back, 0)

        self.commands["talk"] = Command("talk", "<nom> : parler à une personne", Actions.talk, 1)
        self.commands["alibi"] = Command("alibi", "<nom> : demander l’alibi", Actions.alibi, 1)
        self.commands["accuse"] = Command("accuse", "<nom> : accuser le suspect", Actions.accuse, 1)
        #self.commands["inventory"] = Command("inventory", ": afficher l’inventaire", Actions.inventory, 0)
        # ---------- QUÊTES ----------
        self.commands["quests"]= Command("quests", ": afficher les quêtes en cours", Actions.quests, 0)
        self.commands["quest"]= Command("quest", "<numéro> : afficher les détails d’une quête", Actions.quest, 1)
        self.commands["activate"]= Command("activate", ": afficher les objectifs activés", Actions.activate, 1)
        self.commands["rewards"]= Command("rewards", ": afficher les récompenses obtenues", Actions.rewards, 0)
        # ---------- OBJETS ----------
        #self.commands["inventory"] = Command("inventory", ": afficher l’inventaire", Actions.inventory, 0)
        #self.commands["use"] = Command("use", "<nom> : utiliser un objet", Actions.use, 1)
        #self.commands["take"] = Command("take", "<nom> : prendre un objet", Actions.take, 1)
        # ---------- SALLES ----------
        BU = Room("Bibliothèque", "dans le hall principal de la BU.")
        histoire = Room("Salle Histoire", "dans la salle d’histoire.")
        hist_cont = Room("Histoire contemporaine", "dans la salle d'histoire contemporaine.")
        politique = Room("Politique", "dans la salle politique.")
        préhist = Room("Préhistoire", "dans la salle de préhistoire.")
        société = Room("Société", "dans la salle société.")
        environnement = Room("Environnement", "dans la salle environnement.")
        philosophie = Room("Philosophie", "dans la salle philosophie.")
        psycho = Room("Psychologie", "dans la salle psychologie.")
        techno = Room("Technologie", "dans la salle technologie.")
        math = Room("Mathématiques", "dans la salle mathématiques.")

        # ---------- SORTIES ----------
        BU.exits = {"N": histoire, "E": philosophie, "S": société, "O": techno}

        histoire.exits = {"N": hist_cont, "S": BU, "O": politique}
        hist_cont.exits = {"S": histoire}
        politique.exits = {"S": techno}
        techno.exits = {"E": BU, "O": math}
        société.exits = {"N": BU, "S": environnement}
        environnement.exits = {"N": société}

        philosophie.exits = {"O": BU}
        psycho.exits = {}
        préhist.exits = {}
        math.exits = {"E": techno}

        self.rooms = [
            BU, histoire, hist_cont, politique, préhist,
            société, environnement, philosophie, psycho, techno, math
        ]

        # ---------- OBJETS ----------
        arme_crime = Item(
            "Arme du crime",
            "Une lourde sculpture en métal, ensanglantée. Indice majeur.",
            5
        )

        livre_enigme = Item(
            "Livre ancien",
            "Un livre poussiéreux dont certaines pages semblent annotées à la main.",
            2
        )

        cle_usb = Item(
            "Clé USB",
            "Une clé USB contenant des fichiers suspects.",
            0.05
        )

        ordinateur = Item(
            "Ordinateur",
            "Un ordinateur allumé sur lequel tu peux tenter de lire la clé USB.",
            3
        )
        psycho.add_item(arme_crime)
        histoire.add_item(livre_enigme)
        techno.add_item(cle_usb)
        techno.add_item(ordinateur)

        # ---------- PNJ ----------
        suspect1 = Character(
            "bibliothécaire",
            "Une femme calme, concentrée sur son travail.",
            dialog="Avez-vous besoin d'aide ?",
            alibi="Je rangeais les livres d'histoire.",
            guilty=False
        )

        suspect2 = Character(
            "étudiant",
            "Un étudiant stressé, regard fuyant.",
            dialog="Hein ? Non, je… je faisais rien !",
            alibi="Je révisais en philosophie.",
            guilty=True
        )

        suspect3 = Character(
            "professeur",
            "Un professeur passionné de politique.",
            dialog="On ne respecte plus rien de nos jours…",
            alibi="Je débattais en salle de politique.",
            guilty=False
        )

        suspect4 = Character(
            "chercheuse",
            "Une scientifique en quête d’un ouvrage rare.",
            dialog="Je cherchais un manuel en technologie.",
            alibi="J’étais dans la salle techno.",
            guilty=False
        )

        suspect5 = Character(
            "agent",
            "Le gardien de la bibliothèque.",
            dialog="Tout me semblait calme…",
            alibi="Je surveillais la zone sud.",
            guilty=False
        )

        BU.add_character(suspect1)
        philosophie.add_character(suspect2)
        politique.add_character(suspect3)
        techno.add_character(suspect4)
        société.add_character(suspect5)

        # ---------- JOUEUR ----------
        self.player = Player(input("\nEntrez votre nom : "))
        self.player.current_room = BU
        self.current_room = BU
        self._setup_quests()
    def _setup_quests(self):
        # Quête 1 : Visiter toutes les salles liées à l'humain
        salles_visited_quest = Quest(
            title="Explorer les salles liées à l'humain",
            description="Visitez toutes les salles liées à l'étude de l'humain.",
            target_rooms=[
                room for room in self.rooms
                if room.name in [
                    "Salle Histoire",
                    "Histoire contemporaine",
                    "Politique",
                    "Société",
                    "Philosophie",
                    "Psychologie"
                    ]
            ],
            reward="Badge d'explorateur humain"
        )

        # Quête 2 : Questionner les suspects dans la bibliothèque
        questionner_suspects_quest = Quest(
            title="Questionner les suspects",
            description="Parlez à tous les suspects présents dans la bibliothèque.",
            target_characters=[
                char
                for room in self.rooms
                if room.name == "Bibliothèque"
                for char in room.characters
                if char.is_suspect
            ],
            reward="Badge d'enquêteur"
        )

        self.quests.append(salles_visited_quest)
        self.quests.append(questionner_suspects_quest)
        self.player.quest_manager.add_quest(salles_visited_quest)

        
    def print_welcome(self):
        print(
            "Cette nuit-là, au cœur d’un hiver glacial de 1999, "
            "la bibliothèque Hogward s’apprêtait à fermer ses portes.\n"
            "Mais un meurtre vint briser le silence…\n"
        )
        print(f"Bienvenue {self.player.name} dans cette enquête !")
        print("Tape 'help' pour voir les commandes.\n")
        Actions.look(self)

    def play(self):
        self.setup()
        self.print_welcome()

        while not self.finished:
            self.process_command(input("> "))

    def process_command(self, command_string):
        command_string = command_string.strip()
        if not command_string:
            return

        words = command_string.split()
        cmd = words[0]

        if cmd not in self.commands:
            print("Commande inconnue.")
            return

        command = self.commands[cmd]
        command.action(self, words, command.number_of_parameters)

class _StdoutRedirector:
    """Redirect sys.stdout writes into a Tkinter Text widget."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, msg):
        """Write message to the Text widget."""
        if msg:
            self.text_widget.configure(state="normal")
            self.text_widget.insert("end", msg)
            self.text_widget.see("end")
            self.text_widget.configure(state="disabled")

    def flush(self):
        """Flush method required by sys.stdout interface (no-op for Text widget)."""




class GameGUI(tk.Tk):
    """Tkinter GUI for the text-based adventure game.

    Layout layers:
    L3 (top): Split into left image area (600x400) and right buttons.
    L2 (middle): Scrolling terminal output.
    L1 (bottom): Command entry field.
    """

    IMAGE_WIDTH = 600
    IMAGE_HEIGHT = 400

    def __init__(self):
        super().__init__()
        self.title("TBA")
        self.geometry("900x700")  # Provide enough space
        self.minsize(900, 650)

        # Underlying game logic instance
        self.game = Game()

        # Ask player name via dialog (fallback to 'Joueur')
        name = simpledialog.askstring("Nom", "Entrez votre nom:", parent=self)
        if not name:
            name = "Joueur"
        self.game.setup(player_name=name)  # Pass name to avoid double prompt

        # Build UI layers
        self._build_layout()

        # Redirect stdout so game prints appear in terminal output area
        self.original_stdout = sys.stdout
        sys.stdout = _StdoutRedirector(self.text_output)

        # Print welcome text in GUI
        self.game.print_welcome()

        # Load initial room image
        self._update_room_image()

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_close)


    # -------- Layout construction --------
    def _build_layout(self):
        # Configure root grid: 3 rows (L3, L2, L1)
        self.grid_rowconfigure(0, weight=0)  # Image/buttons fixed height
        self.grid_rowconfigure(1, weight=1)  # Terminal output expands
        self.grid_rowconfigure(2, weight=0)  # Entry fixed
        self.grid_columnconfigure(0, weight=1)

        # L3 Top frame
        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, sticky="nsew", padx=6, pady=(6,3))
        top_frame.grid_columnconfigure(0, weight=0)
        top_frame.grid_columnconfigure(1, weight=1)

        # L3L Image area (left)
        image_frame = ttk.Frame(top_frame, width=self.IMAGE_WIDTH, height=self.IMAGE_HEIGHT)
        image_frame.grid(row=0, column=0, sticky="nw", padx=(0,6))
        image_frame.grid_propagate(False)  # Keep requested size
        self.canvas = tk.Canvas(image_frame,
                                width=self.IMAGE_WIDTH,
                                height=self.IMAGE_HEIGHT,
                                bg="#222")
        self.canvas.pack(fill="both", expand=True)

        # Initialize image reference (will be loaded by _update_room_image)
        self._image_ref = None  # Keep reference to prevent garbage collection
        # Initial image will be loaded after welcome message

        # L3R Buttons area (right)
        buttons_frame = ttk.Frame(top_frame)
        buttons_frame.grid(row=0, column=1, sticky="ne")
        for i in range(10):
            buttons_frame.grid_rowconfigure(i, weight=0)
        buttons_frame.grid_columnconfigure(0, weight=1)

        # Load button images (keep references to prevent garbage collection)
        assets_dir = Path(__file__).parent / 'assets'
        # Load pre-resized 50x50 PNG images for better quality
        self._btn_help = tk.PhotoImage(file=assets_dir / 'help-50.png')
        self._btn_up = tk.PhotoImage(file=assets_dir / 'up-arrow-50.png')
        self._btn_down = tk.PhotoImage(file=assets_dir / 'down-arrow-50.png')
        self._btn_left = tk.PhotoImage(file=assets_dir / 'left-arrow-50.png')
        self._btn_right = tk.PhotoImage(file=assets_dir / 'right-arrow-50.png')
        self._btn_quit = tk.PhotoImage(file=assets_dir / 'quit-50.png')

        # Command buttons
        tk.Button(buttons_frame,
                  image=self._btn_help,
                  command=lambda: self._send_command("help"),
                  bd=0).grid(row=0, column=0, sticky="ew", pady=2)
        # Movement buttons (N,E,S,O)
        move_frame = ttk.LabelFrame(buttons_frame, text="Déplacements")
        move_frame.grid(row=1, column=0, sticky="ew", pady=4)
        tk.Button(move_frame,
                  image=self._btn_up,
                  command=lambda: self._send_command("go N"),
                  bd=0).grid(row=0, column=0, columnspan=2)
        tk.Button(move_frame,
                  image=self._btn_left,
                  command=lambda: self._send_command("go O"),
                  bd=0).grid(row=1, column=0)
        tk.Button(move_frame,
                  image=self._btn_right,
                  command=lambda: self._send_command("go E"),
                  bd=0).grid(row=1, column=1)
        tk.Button(move_frame,
                  image=self._btn_down,
                  command=lambda: self._send_command("go S"),
                  bd=0).grid(row=2, column=0, columnspan=2)

        # Quit button
        tk.Button(buttons_frame,
                  image=self._btn_quit,
                  command=lambda: self._send_command("quit"),
                  bd=0).grid(row=2, column=0, sticky="ew", pady=(8,2))

        # L2 Terminal output area (Text + Scrollbar)
        output_frame = ttk.Frame(self)
        output_frame.grid(row=1, column=0, sticky="nsew", padx=6, pady=3)
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(output_frame, orient="vertical")
        self.text_output = tk.Text(output_frame,
                                   wrap="word",
                                   yscrollcommand=scrollbar.set,
                                   state="disabled",
                                   bg="#111", fg="#eee")
        scrollbar.config(command=self.text_output.yview)
        self.text_output.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # L1 Entry area
        entry_frame = ttk.Frame(self)
        entry_frame.grid(row=2, column=0, sticky="ew", padx=6, pady=(3,6))
        entry_frame.grid_columnconfigure(0, weight=1)

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(entry_frame, textvariable=self.entry_var)
        self.entry.grid(row=0, column=0, sticky="ew")
        self.entry.bind("<Return>", self._on_enter)
        self.entry.focus_set()


    # -------- Image update --------
    def _update_room_image(self):
        """Update the canvas image based on the current room."""
        if not self.game.player or not self.game.player.current_room:
            return

        room = self.game.player.current_room
        assets_dir = Path(__file__).parent / 'assets'

        # Use room-specific image if available, otherwise fallback
        if room.image:
            image_path = assets_dir / room.image
        else:
            image_path = assets_dir / 'scene.png'

        try:
            # Load new image
            self._image_ref = tk.PhotoImage(file=image_path)
            # Clear canvas and redraw image
            self.canvas.delete("all")
            self.canvas.create_image(
                self.IMAGE_WIDTH/2,
                self.IMAGE_HEIGHT/2,
                image=self._image_ref
            )
        except FileNotFoundError:
            # Fallback to text if image not found or cannot be loaded
            self.canvas.delete("all")
            self.canvas.create_text(
                self.IMAGE_WIDTH/2,
                self.IMAGE_HEIGHT/2,
                text=f"Image: {room.name}",
                fill="white",
                font=("Helvetica", 18)
            )


    # -------- Event handlers --------
    def _on_enter(self, _event=None):
        """Handle Enter key press in the entry field."""
        value = self.entry_var.get().strip()
        if value:
            self._send_command(value)
        self.entry_var.set("")


    def _send_command(self, command):
        if self.game.finished:
            return
        # Echo the command in output area
        print(f"> {command}\n")
        self.game.process_command(command)
        # Update room image after command (in case player moved)
        self._update_room_image()
        if self.game.finished:
            # Disable further input and schedule close (brief delay to show farewell)
            self.entry.configure(state="disabled")
            self.after(600, self._on_close)


    def _on_close(self):
        # Restore stdout and destroy window
        sys.stdout = self.original_stdout
        self.destroy()



def main():
    """Entry point.

    If '--cli' is passed as an argument, start the classic console version.
    Otherwise launch the Tkinter GUI.
    Fallback to CLI if GUI cannot be initialized (e.g., headless environment).
    """
    args = sys.argv[1:]
    if '--cli' in args:
        Game().play()
        return
    try:
        app = GameGUI()
        app.mainloop()
    except tk.TclError as e:
        # Fallback to CLI if GUI fails (e.g., no DISPLAY, Tkinter not available)
        print(f"GUI indisponible ({e}). Passage en mode console.")
        game = Game()
        game.play()


if __name__ == "__main__":
    main()
