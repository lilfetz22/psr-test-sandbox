class Widget:
    """A new widget component."""

    def __init__(self, name: str):
        self.name = name

    def render(self) -> str:
        return f"<widget>{self.name}</widget>"

    def render_dashboard(self) -> str:
        return f"<dashboard><widget>{self.name}</widget></dashboard>"
