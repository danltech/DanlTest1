#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import json
import subprocess
import os
import sys
from PIL import Image, ImageTk

class RecoveryLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("DanlTest Tool Launcher")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')

        # Pfade
        self.config_path = "/root/DanlTest/Launcher/config.json"
        self.icon_path = "/root/DanlTest/Launcher/icon.png"

        # Laden der Konfiguration
        self.tools = self.load_config()

        # GUI erstellen
        self.create_gui()

    def load_config(self):
        """Lädt die Tool-Konfiguration aus der JSON-Datei"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Fehler beim Laden der Konfiguration: {e}")
            return []

    def create_gui(self):
        """Erstellt die Benutzeroberfläche"""
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="DanlTest Tool Launcher",
            font=('Arial', 20, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(expand=True)

        # Suchleiste
        search_frame = tk.Frame(self.root, bg='#f0f0f0')
        search_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            search_frame,
            text="Suchen:",
            font=('Arial', 10),
            bg='#f0f0f0'
        ).pack(side=tk.LEFT)

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Arial', 10),
            width=30
        )
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind('<KeyRelease>', self.filter_tools)

        # Tool-Liste
        list_frame = tk.Frame(self.root, bg='#f0f0f0')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Treeview für Tools
        columns = ('name', 'description', 'category')
        self.tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show='headings',
            height=15
        )

        # Spalten definieren
        self.tree.heading('name', text='Tool Name')
        self.tree.heading('description', text='Beschreibung')
        self.tree.heading('category', text='Kategorie')

        self.tree.column('name', width=200)
        self.tree.column('description', width=400)
        self.tree.column('category', width=150)

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            list_frame,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Double-Click Binding
        self.tree.bind('<Double-1>', self.launch_tool)

        # Button Frame
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, padx=20, pady=10)

        launch_btn = tk.Button(
            button_frame,
            text="Tool starten",
            command=self.launch_selected_tool,
            font=('Arial', 12),
            bg='#27ae60',
            fg='white',
            padx=20
        )
        launch_btn.pack(side=tk.LEFT, padx=5)

        exit_btn = tk.Button(
            button_frame,
            text="Beenden",
            command=self.root.quit,
            font=('Arial', 12),
            bg='#e74c3c',
            fg='white',
            padx=20
        )
        exit_btn.pack(side=tk.RIGHT, padx=5)

        # Tools in Liste anzeigen
        self.populate_tool_list()

    def populate_tool_list(self, tools=None):
        """Füllt die Tool-Liste"""
        if tools is None:
            tools = self.tools

        # Liste leeren
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Tools hinzufügen
        for tool in tools:
            self.tree.insert(
                '',
                tk.END,
                values=(
                    tool.get('name', 'Unbekannt'),
                    tool.get('description', 'Keine Beschreibung'),
                    tool.get('category', 'Allgemein')
                ),
                tags=(tool.get('command', ''),)
            )

    def filter_tools(self, event=None):
        """Filtert die Tool-Liste basierend auf der Sucheingabe"""
        search_term = self.search_var.get().lower()

        if not search_term:
            self.populate_tool_list(self.tools)
            return

        filtered_tools = [
            tool for tool in self.tools
            if (search_term in tool.get('name', '').lower() or
                search_term in tool.get('description', '').lower() or
                search_term in tool.get('category', '').lower())
        ]

        self.populate_tool_list(filtered_tools)

    def get_selected_tool(self):
        """Gibt das aktuell ausgewählte Tool zurück"""
        selection = self.tree.selection()
        if not selection:
            return None

        item = selection[0]
        command = self.tree.item(item, 'tags')[0]

        # Finde das Tool in der Konfiguration
        for tool in self.tools:
            if tool.get('command') == command:
                return tool

        return None

    def launch_selected_tool(self):
        """Startet das ausgewählte Tool"""
        tool = self.get_selected_tool()
        if tool:
            self.execute_tool(tool)
        else:
            messagebox.showwarning(
                "Kein Tool ausgewählt",
                "Bitte wählen Sie zunächst ein Tool aus der Liste aus."
            )

    def launch_tool(self, event):
        """Startet Tool bei Double-Click"""
        self.launch_selected_tool()

    def execute_tool(self, tool):
        """Führt das Tool-Kommando aus"""
        command = tool.get('command')
        if not command:
            messagebox.showerror(
                "Fehler",
                "Kein Befehl für dieses Tool konfiguriert."
            )
            return

        try:
            # Führe den Befehl im Hintergrund aus
            if tool.get('terminal', False):
                # Starte in Terminal wenn benötigt
                subprocess.Popen(['x-terminal-emulator', '-e', command])
            else:
                subprocess.Popen(command, shell=True)

            messagebox.showinfo(
                "Tool gestartet",
                f"{tool.get('name')} wird gestartet..."
            )

        except Exception as e:
            messagebox.showerror(
                "Fehler",
                f"Konnte Tool nicht starten: {str(e)}"
            )

def main():
    root = tk.Tk()
    app = RecoveryLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main()

