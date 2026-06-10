"""Tkinter desktop application for the distributed-key project workflow."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

from dkglab.gui.services import (
    DEFAULT_MESSAGE,
    DEFAULT_SIGNERS,
    TextResult,
    parse_participant_ids,
    workflow_attack_summary,
    workflow_dkg_summary,
    workflow_signature_summary,
)


class DistributedKeyLabApp(tk.Tk):
    """Desktop UI for the distributed key generation and threshold signature flow."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Distributed Key Lab")
        self.geometry("1080x680")
        self.minsize(940, 600)

        self._configure_theme()
        self._build_layout()
        self._show_result(self._welcome_text())

    def _configure_theme(self) -> None:
        self.configure(bg="#eef2f6")
        self.option_add("*Font", ("Segoe UI", 10))

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#eef2f6")
        style.configure("Panel.TFrame", background="#ffffff", relief="flat")
        style.configure("Header.TFrame", background="#172033")
        style.configure(
            "HeaderTitle.TLabel",
            background="#172033",
            foreground="#ffffff",
            font=("Segoe UI", 20, "bold"),
        )
        style.configure(
            "HeaderSub.TLabel",
            background="#172033",
            foreground="#b9c4d5",
            font=("Segoe UI", 10),
        )
        style.configure("TLabel", background="#ffffff", foreground="#1f2937")
        style.configure("Muted.TLabel", background="#ffffff", foreground="#64748b")
        style.configure(
            "CardTitle.TLabel",
            background="#ffffff",
            foreground="#111827",
            font=("Segoe UI", 12, "bold"),
        )
        style.configure(
            "TButton",
            background="#2563eb",
            foreground="#ffffff",
            padding=(12, 8),
            borderwidth=0,
        )
        style.map("TButton", background=[("active", "#1d4ed8"), ("disabled", "#94a3b8")])
        style.configure("Secondary.TButton", background="#e2e8f0", foreground="#0f172a")
        style.map("Secondary.TButton", background=[("active", "#cbd5e1")])
        style.configure("TEntry", padding=7)
        style.configure("Status.TLabel", background="#e2e8f0", foreground="#334155", padding=(10, 5))

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        header = ttk.Frame(self, style="Header.TFrame", padding=(24, 18))
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)
        ttk.Label(header, text="Distributed Key Lab", style="HeaderTitle.TLabel").grid(
            row=0,
            column=0,
            sticky="w",
        )
        ttk.Label(
            header,
            text="Glowny przeplyw projektu: rozproszona generacja klucza -> podpis progowy -> kontrola progu",
            style="HeaderSub.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

        main = ttk.Frame(self, padding=16)
        main.grid(row=1, column=0, sticky="nsew")
        main.columnconfigure(0, weight=0)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(0, weight=1)

        controls = ttk.Frame(main, style="Panel.TFrame", padding=16)
        controls.grid(row=0, column=0, sticky="ns", padx=(0, 14))
        controls.columnconfigure(0, weight=1)
        controls.columnconfigure(1, weight=1)

        ttk.Label(controls, text="Scenariusz 3 z 5", style="CardTitle.TLabel").grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(0, 12),
        )

        self.signers_var = tk.StringVar(value=",".join(str(value) for value in DEFAULT_SIGNERS))
        self.message_var = tk.StringVar(value=DEFAULT_MESSAGE)

        self._entry(controls, "Podpisujacy", self.signers_var, 1)
        self._entry(controls, "Wiadomosc", self.message_var, 2)

        ttk.Button(
            controls,
            text="1. Wygeneruj wspolny klucz publiczny",
            style="Secondary.TButton",
            command=lambda: self._run_action(workflow_dkg_summary),
        ).grid(row=3, column=0, columnspan=2, sticky="ew", pady=(14, 8))
        ttk.Button(
            controls,
            text="2. Podpis progowy",
            style="Secondary.TButton",
            command=self._run_signature_demo,
        ).grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        ttk.Button(
            controls,
            text="3. Test zbyt malej liczby uczestnikow",
            style="Secondary.TButton",
            command=lambda: self._run_action(workflow_attack_summary),
        ).grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 14))

        ttk.Label(
            controls,
            text="Co pokazuje aplikacja",
            style="CardTitle.TLabel",
        ).grid(row=6, column=0, columnspan=2, sticky="w", pady=(8, 8))
        ttk.Label(
            controls,
            text=(
                "Najpierw uruchom rozproszona generacje klucza, aby pokazac wspolny klucz publiczny i "
                "zweryfikowane udzialy uczestnikow. Nastepnie wykonaj podpis progowy "
                "dla wybranej wiadomosci. Na koncu sprawdz scenariusz z dwoma uczestnikami, ktory "
                "potwierdza, ze dwoch uczestnikow nie moze podpisac w modelu 3 z 5."
            ),
            style="Muted.TLabel",
            wraplength=290,
        ).grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0, 12))

        ttk.Label(
            controls,
            text=(
                "Wynik po prawej pokazuje pelne wartosci: wspolny klucz publiczny, "
                "wspolny punkt losowy podpisu oraz skalar podpisu. "
                "Dlugie ciagi heksadecymalne sa zawijane w panelu tekstowym."
            ),
            style="Muted.TLabel",
            wraplength=290,
        ).grid(row=8, column=0, columnspan=2, sticky="ew")

        output_frame = ttk.Frame(main)
        output_frame.grid(row=0, column=1, sticky="nsew")
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)

        self.output = tk.Text(
            output_frame,
            bg="#0f172a",
            fg="#e5e7eb",
            insertbackground="#e5e7eb",
            relief="flat",
            wrap="char",
            padx=18,
            pady=18,
            font=("Cascadia Mono", 10),
            height=24,
        )
        self.output.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=self.output.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.output.configure(yscrollcommand=scrollbar.set)

        self.status = ttk.Label(self, text="Ready", style="Status.TLabel")
        self.status.grid(row=2, column=0, sticky="ew")

    def _run_signature_demo(self) -> None:
        def action() -> TextResult:
            return workflow_signature_summary(
                selected_ids=parse_participant_ids(self.signers_var.get()),
                message=self.message_var.get(),
            )

        self._run_action(action)

    def _run_action(self, action: Callable[[], TextResult]) -> None:
        try:
            result = action()
        except Exception as exc:
            self._show_result(TextResult(title="Blad", body=str(exc)))
            self.status.configure(text=f"Error: {exc}")
            return

        self._show_result(result)
        self.status.configure(text=f"Done: {result.title}")

    def _show_result(self, result: TextResult) -> None:
        self.output.configure(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, f"{result.title}\n")
        self.output.insert(tk.END, "=" * len(result.title) + "\n\n")
        self.output.insert(tk.END, result.body)
        self.output.configure(state="disabled")

    @staticmethod
    def _entry(parent: ttk.Frame, label: str, variable: tk.StringVar, row: int) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=(0, 8), padx=(0, 8))
        ttk.Entry(parent, textvariable=variable).grid(row=row, column=1, sticky="ew", pady=(0, 8))

    @staticmethod
    def _welcome_text() -> TextResult:
        return TextResult(
            title="Distributed Key Lab",
            body=(
                "Aplikacja uruchamia glowny przeplyw rozproszonej generacji klucza i podpisu progowego.\n\n"
                "1. Uczestnicy generuja wspolny klucz publiczny.\n"
                "2. Trzech wybranych uczestnikow tworzy podpis progowy Schnorra.\n"
                "3. Proba podpisu przez mniej niz wymagany prog jest odrzucana.\n\n"
                "Uruchom kroki po kolei przyciskami po lewej stronie."
            ),
        )


def main() -> None:
    """Launch the Tkinter desktop app."""
    app = DistributedKeyLabApp()
    app.mainloop()


if __name__ == "__main__":
    main()
