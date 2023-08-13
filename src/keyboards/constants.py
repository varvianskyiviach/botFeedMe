from enum import Enum


class Commands(str, Enum):
    START = "/start"
    HELP = "/help"
    DELETE = "/del"


class Menu(str, Enum):
    ANALYTICS = "📊 Analytics"
    TODAY = "📅 Today"
