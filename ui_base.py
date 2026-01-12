# ui_base.py
class HoverButtonsMixin:
    def bind_hover_buttons(self, buttons, normal_bg, hover_bg):
        for btn in buttons:
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=hover_bg))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=normal_bg))
