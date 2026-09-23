import customtkinter as ctk

from ui.components.kpi_card import KPICard


class SmartKPIPanel(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.cards = []

    def update_cards(self, kpis):

        for card in self.cards:

            card.destroy()

        self.cards.clear()

        for title, value in kpis[:4]:

            card = KPICard(
                self,
                title=title,
                icon="📈",
                accent="#14B8A6"
            )

            card.update_value(value)

            card.pack(
                side="left",
                padx=10,
                pady=5
            )

            self.cards.append(card)