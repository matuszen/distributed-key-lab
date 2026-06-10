"""Tkinter desktop application for Distributed Key Lab."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

from dkglab.gui.services import (
    DEFAULT_MESSAGE,
    TextResult,
    attack_t_minus_one_demo,
    benchmark_dkg,
    curve_summary,
    dkg_demo,
    parse_participant_ids,
    shamir_demo,
    threshold_wallet_demo,
)


class DistributedKeyLabApp(tk.Tk):
    """Small desktop UI for running the project's academic crypto demos."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Distributed Key Lab")
        self.geometry("1120x720")
        self.minsize(980, 640)

        self._configure_theme()
        self._build_layout()
        self._show_result(curve_summary())

    def _configure_theme(self) -> None:
        self.configure(bg="#eef2f6")
        self.option_add("*Font", ("Segoe UI", 10))

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#eef2f6")
        style.configure("Panel.TFrame", background="#ffffff", relief="flat")
        style.configure("Header.TFrame", background="#172033")
        style.configure("HeaderTitle.TLabel", background="#172033", foreground="#ffffff", font=("Segoe UI", 20, "bold"))
        style.configure("HeaderSub.TLabel", background="#172033", foreground="#b9c4d5", font=("Segoe UI", 10))
        style.configure("TLabel", background="#ffffff", foreground="#1f2937")
        style.configure("Muted.TLabel", background="#ffffff", foreground="#64748b")
        style.configure("CardTitle.TLabel", background="#ffffff", foreground="#111827", font=("Segoe UI", 12, "bold"))
        style.configure("TButton", background="#2563eb", foreground="#ffffff", padding=(12, 7), borderwidth=0)
        style.map("TButton", background=[("active", "#1d4ed8"), ("disabled", "#94a3b8")])
        style.configure("Secondary.TButton", background="#e2e8f0", foreground="#0f172a")
        style.map("Secondary.TButton", background=[("active", "#cbd5e1")])
        style.configure("TNotebook", background="#eef2f6", borderwidth=0)
        style.configure("TNotebook.Tab", padding=(16, 8), background="#dbe3ef", foreground="#334155")
        style.map("TNotebook.Tab", background=[("selected", "#ffffff")], foreground=[("selected", "#111827")])
        style.configure("TEntry", padding=6)
        style.configure("Status.TLabel", background="#e2e8f0", foreground="#334155", padding=(10, 5))

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        header = ttk.Frame(self, style="Header.TFrame", padding=(24, 18))
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)
        ttk.Label(header, text="Distributed Key Lab", style="HeaderTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text="SSS, Feldman VSS, DKG i progowy podpis Schnorra",
            style="HeaderSub.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

        main = ttk.Frame(self, padding=16)
        main.grid(row=1, column=0, sticky="nsew")
        main.columnconfigure(0, weight=0)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(0, weight=1)

        left_panel = ttk.Frame(main, style="Panel.TFrame", padding=14)
        left_panel.grid(row=0, column=0, sticky="ns", padx=(0, 14))
        left_panel.rowconfigure(0, weight=1)

        self.output = tk.Text(
            main,
            bg="#0f172a",
            fg="#e5e7eb",
            insertbackground="#e5e7eb",
            relief="flat",
            wrap="word",
            padx=18,
            pady=18,
            font=("Cascadia Mono", 10),
            height=24,
        )
        self.output.grid(row=0, column=1, sticky="nsew")

        notebook = ttk.Notebook(left_panel)
        notebook.grid(row=0, column=0, sticky="nsew")
        notebook.add(self._build_start_tab(notebook), text="Start")
        notebook.add(self._build_sss_tab(notebook), text="SSS")
        notebook.add(self._build_protocol_tab(notebook), text="DKG / TSS")

        self.status = ttk.Label(self, text="Ready", style="Status.TLabel")
        self.status.grid(row=2, column=0, sticky="ew")

    def _build_start_tab(self, parent: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(parent, style="Panel.TFrame", padding=14)
        frame.columnconfigure(0, weight=1)
        self._section_title(frame, "Szybkie akcje", 0)
        self._button(frame, "Parametry krzywej", lambda: self._run_action(curve_summary), 1)
        self._button(frame, "Demo DKG 3 z 5", lambda: self._run_action(lambda: dkg_demo(5, 3)), 2)
        self._button(
            frame,
            "Podpis portfela 3 z 5",
            lambda: self._run_action(lambda: threshold_wallet_demo([1, 3, 5], DEFAULT_MESSAGE)),
            3,
        )
        self._button(frame, "Atak t-1", lambda: self._run_action(attack_t_minus_one_demo), 4, secondary=True)
        self._button(frame, "Benchmark DKG", lambda: self._run_action(benchmark_dkg), 5, secondary=True)
        ttk.Label(
            frame,
            text=(
                "Wyniki pojawiają się po prawej. Przykłady używają "
                "deterministycznych danych, żeby demonstracja była powtarzalna."
            ),
            style="Muted.TLabel",
            wraplength=280,
        ).grid(row=6, column=0, sticky="ew", pady=(18, 0))
        return frame

    def _build_sss_tab(self, parent: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(parent, style="Panel.TFrame", padding=14)
        frame.columnconfigure(1, weight=1)
        self._section_title(frame, "Shamir Secret Sharing", 0, columnspan=2)

        self.secret_var = tk.StringVar(value="123456789")
        self.sss_threshold_var = tk.StringVar(value="3")
        self.sss_participants_var = tk.StringVar(value="5")

        self._entry(frame, "Sekret", self.secret_var, 1)
        self._entry(frame, "Próg t", self.sss_threshold_var, 2)
        self._entry(frame, "Liczba n", self.sss_participants_var, 3)
        ttk.Button(frame, text="Podziel i odzyskaj", command=self._run_shamir).grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(14, 0),
        )
        ttk.Label(
            frame,
            text="Pokazuje udziały, rekonstrukcję z t elementów oraz blokadę t-1.",
            style="Muted.TLabel",
            wraplength=280,
        ).grid(row=5, column=0, columnspan=2, sticky="ew", pady=(14, 0))
        return frame

    def _build_protocol_tab(self, parent: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(parent, style="Panel.TFrame", padding=14)
        frame.columnconfigure(1, weight=1)
        self._section_title(frame, "DKG i podpis progowy", 0, columnspan=2)

        self.signers_var = tk.StringVar(value="1,3,5")
        self.message_var = tk.StringVar(value=DEFAULT_MESSAGE)

        self._entry(frame, "Uczestnicy", self.signers_var, 1)
        self._entry(frame, "Wiadomość", self.message_var, 2)

        ttk.Button(frame, text="Uruchom DKG", command=lambda: self._run_action(lambda: dkg_demo(5, 3))).grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(14, 0),
        )
        ttk.Button(frame, text="Podpisz wiadomość", command=self._run_threshold_wallet).grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(8, 0),
        )
        ttk.Button(
            frame,
            text="Symuluj atak t-1",
            style="Secondary.TButton",
            command=lambda: self._run_action(attack_t_minus_one_demo),
        ).grid(row=5, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        ttk.Button(
            frame,
            text="Benchmark DKG",
            style="Secondary.TButton",
            command=lambda: self._run_action(benchmark_dkg),
        ).grid(row=6, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        ttk.Label(
            frame,
            text="Domyślny scenariusz to portfel 3 z 5. Zmień listę uczestników, np. 2,4,5.",
            style="Muted.TLabel",
            wraplength=280,
        ).grid(row=7, column=0, columnspan=2, sticky="ew", pady=(14, 0))
        return frame

    def _run_shamir(self) -> None:
        def action() -> TextResult:
            return shamir_demo(
                secret=int(self.secret_var.get()),
                threshold=int(self.sss_threshold_var.get()),
                num_participants=int(self.sss_participants_var.get()),
            )

        self._run_action(action)

    def _run_threshold_wallet(self) -> None:
        def action() -> TextResult:
            selected_ids = parse_participant_ids(self.signers_var.get())
            return threshold_wallet_demo(selected_ids=selected_ids, message=self.message_var.get())

        self._run_action(action)

    def _run_action(self, action: Callable[[], TextResult]) -> None:
        try:
            result = action()
        except Exception as exc:
            self._show_result(TextResult(title="Błąd", body=str(exc)))
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
    def _section_title(parent: ttk.Frame, text: str, row: int, columnspan: int = 1) -> None:
        ttk.Label(parent, text=text, style="CardTitle.TLabel").grid(
            row=row,
            column=0,
            columnspan=columnspan,
            sticky="w",
            pady=(0, 12),
        )

    @staticmethod
    def _button(
        parent: ttk.Frame,
        text: str,
        command: Callable[[], None],
        row: int,
        secondary: bool = False,
    ) -> None:
        style = "Secondary.TButton" if secondary else "TButton"
        ttk.Button(parent, text=text, command=command, style=style).grid(row=row, column=0, sticky="ew", pady=(0, 8))

    @staticmethod
    def _entry(parent: ttk.Frame, label: str, variable: tk.StringVar, row: int) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=(0, 8), padx=(0, 8))
        ttk.Entry(parent, textvariable=variable).grid(row=row, column=1, sticky="ew", pady=(0, 8))


def main() -> None:
    """Launch the Tkinter desktop app."""
    app = DistributedKeyLabApp()
    app.mainloop()


if __name__ == "__main__":
    main()
