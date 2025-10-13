#!/usr/bin/env python3

from labyrinth_game import player_actions as actions
from labyrinth_game.constants import COMMANDS
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    get_input,
    show_help,
    solve_puzzle,
)


def process_command(game_state: dict, command: str, commands: dict) -> None:
    """Обрабатывает введённую пользователем команду."""
    parts = command.strip().split(maxsplit=1)
    if not parts:
        return

    cmd = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else ""

    if cmd in {"north", "south", "east", "west"}:
        actions.move_player(game_state, cmd)
        return

    match cmd:
        case "look":
            describe_current_room(game_state)
        case "go":
            actions.move_player(game_state, arg)
        case "take":
            actions.take_item(game_state, arg)
        case "use":
            # Победа через сундук должна происходить командой solve в treasure_room.
            actions.use_item(game_state, arg)
        case "inventory":
            actions.show_inventory(game_state)
        case "solve":
            if game_state["current_room"] == "treasure_room":
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case "help" | "?":
            show_help(commands)
        case "quit" | "exit":
            print("Игра завершена. До встречи!")
            game_state["game_over"] = True
        case _:
            print("Неизвестная команда. Введите 'help' для списка команд.")


def main() -> None:
    """Основной игровой цикл."""
    game_state = {
        "player_inventory": [],
        "current_room": "entrance",
        "game_over": False,
        "steps_taken": 0,
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    show_help(COMMANDS)
    describe_current_room(game_state)

    while not game_state["game_over"]:
        cmd = get_input("> ")
        process_command(game_state, cmd, COMMANDS)


if __name__ == "__main__":
    main()