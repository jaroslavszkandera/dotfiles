# -*- coding: utf-8 -*-

# Cloze Overlapper Add-on for Anki
#
# Copyright (C)  2016-2023 Aristotelis P. <https://glutanimate.com/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version, with the additions
# listed at the end of the license file that accompanied this program
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# NOTE: This program is subject to certain additional terms pursuant to
# Section 7 of the GNU Affero General Public License.  You should have
# received a copy of these additional terms immediately following the
# terms and conditions of the GNU Affero General Public License that
# accompanied this program.
#
# If not, please request a copy through one of the means of contact
# listed here: <https://glutanimate.com/contact/>.
#
# Any modifications to this file must keep this entire header intact.

import os
from dataclasses import dataclass
from types import SimpleNamespace
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    cast,
    Tuple,
)

if TYPE_CHECKING:
    from aqt.editor import Editor, EditorWebView

from anki.consts import MODEL_CLOZE
from aqt.qt import QKeySequence, QShortcut

from ...config import config
from ...libaddon.platform import PATH_THIS_ADDON
from ...template import check_model
from .fields import (
    insert_overlapping_cloze,
    insert_multiple_clozes,
    regenerate_clozes,
    invoke_note_options,
    remove_clozes,
)

ICON_PATH = os.path.join(PATH_THIS_ADDON, "web", "icons")
ICON_REMOVE = os.path.join(ICON_PATH, "oc_remove.svg")
ICON_CLOZE_MULTIPLE_LINES = os.path.join(ICON_PATH, "cloze_multiple_lines.svg")
ICON_TOGGLE_UNORDERED_LIST = os.path.join(ICON_PATH, "toggle_unordered_list.svg")
ICON_TOGGLE_ORDERED_LIST = os.path.join(ICON_PATH, "toggle_ordered_list.svg")
ICON_GENERATE = os.path.join(ICON_PATH, "oc_generate.svg")
ICON_OPTIONS = os.path.join(ICON_PATH, "oc_options.svg")
ICON_ANKI_CLOZE_INCREMENT = os.path.join(ICON_PATH, "cloze_increment.svg")
ICON_ANKI_CLOZE_SAME = os.path.join(ICON_PATH, "cloze_same.svg")


@dataclass
class EditorButton:
    icon: Optional[str]
    cmd: str
    func: Callable[["Editor"], None]
    tip: str = ""
    label: str = ""
    toggleable: bool = False
    keys: Optional[str] = None
    disables: bool = True
    rightside: bool = True
    cloze_overlapper_exclusive: bool = True


def get_editor_buttons() -> List["EditorButton"]:
    hotkey_cloze_multiple_lines = config["local"]["hotkey_cloze_multiple_lines"]
    hotkey_toggle_unordered_list = config["local"]["hotkey_toggle_unordered_list"]
    hotkey_toggle_ordered_list = config["local"]["hotkey_toggle_ordered_list"]
    hotkey_remove_cloze = config["local"]["hotkey_remove_cloze"]
    hotkey_generate_clozes = config["local"]["hotkey_generate_clozes"]
    hotkey_open_note_options = config["local"]["hotkey_open_note_options"]

    return [
        EditorButton(
            icon=ICON_ANKI_CLOZE_INCREMENT,
            cmd="ol-cloze-anki-increment",
            func=insert_overlapping_cloze,
            tip="Overlapping cloze deletion (new card) (Ctrl+Shift+C)",
            keys="Ctrl+Shift+C",
            cloze_overlapper_exclusive=True,
        ),
        EditorButton(
            icon=ICON_ANKI_CLOZE_SAME,
            cmd="ol-cloze-anki-same",
            func=lambda editor: insert_overlapping_cloze(editor, same_card=True),  # type: ignore[call-arg]
            tip="Overlapping cloze deletion (same card) (Ctrl+Alt+Shift+C)",
            keys="Ctrl+Alt+Shift+C",
            cloze_overlapper_exclusive=True,
        ),
        EditorButton(
            icon=ICON_CLOZE_MULTIPLE_LINES,
            cmd="ol-cloze-multiple-lines",
            func=insert_multiple_clozes,
            tip=(
                "Wrap selected lines in overlapping clozes"
                f" ({hotkey_cloze_multiple_lines})"
            ),
            keys=hotkey_cloze_multiple_lines,
            cloze_overlapper_exclusive=False,
        ),
        EditorButton(
            icon=ICON_TOGGLE_UNORDERED_LIST,
            cmd="ol-toggle-unordered-list",
            func=lambda editor, m="ul": regenerate_clozes(  # type: ignore[misc]
                editor=editor, markup=m  # type: ignore[call-arg]
            ),
            tip=(
                "Convert selected lines into a clozed unordered list"
                f" ({hotkey_toggle_unordered_list})"
            ),
            keys=hotkey_toggle_unordered_list,
            cloze_overlapper_exclusive=True,
        ),
        EditorButton(
            icon=ICON_TOGGLE_ORDERED_LIST,
            cmd="ol-toggle-ordered-list",
            func=lambda editor, m="ol": regenerate_clozes(  # type: ignore[misc]
                editor=editor, markup=m  # type: ignore[call-arg]
            ),
            tip=(
                "Convert selected lines into a clozed ordered list"
                f" ({hotkey_toggle_ordered_list})"
            ),
            keys=hotkey_toggle_ordered_list,
            cloze_overlapper_exclusive=True,
        ),
        EditorButton(
            icon=ICON_REMOVE,
            cmd="ol-remove-clozes",
            func=remove_clozes,
            tip=f"Remove all cloze markers in selected text ({hotkey_remove_cloze})",
            keys=hotkey_remove_cloze,
            cloze_overlapper_exclusive=False,
        ),
        EditorButton(
            icon=ICON_GENERATE,
            cmd="ol-generate-clozes",
            func=regenerate_clozes,
            tip=f"Generate overlapping clozes ({hotkey_generate_clozes})",
            keys=hotkey_generate_clozes,
            cloze_overlapper_exclusive=True,
        ),
        EditorButton(
            icon=ICON_OPTIONS,
            cmd="ol-show-options",
            func=invoke_note_options,
            tip=f"Overlapping cloze options ({hotkey_open_note_options})",
            keys=hotkey_open_note_options,
            cloze_overlapper_exclusive=True,
        ),
    ]


def initialize_buttons(buttons: List[str], editor: "Editor"):
    shortcuts: Dict[str, QShortcut] = {}
    for button in get_editor_buttons():
        buttons.append(
            editor.addButton(
                icon=button.icon,
                cmd=button.cmd,
                func=button.func,
                tip=button.tip,
                label=button.label,
                id=button.cmd,
                toggleable=button.toggleable,
                disables=button.disables,
                rightside=button.rightside,
            )
        )

        shortcut = QShortcut(QKeySequence(button.keys), editor.widget)
        shortcut.activated.connect(lambda func=button.func: func(editor))

        shortcuts[button.cmd] = shortcut

    namespace = get_addon_namespace("cloze_overlapper", editor)
    namespace.shortcuts = shortcuts


def toggle_buttons_and_hotkeys(editor: "Editor"):
    if (webview := editor.web) is None:
        return
    if (note := editor.note) is None:
        return
    if (note_type := note.note_type()) is None:
        return

    buttons = get_editor_buttons()
    namespace = get_addon_namespace("cloze_overlapper", editor)
    shortcuts = cast(Dict[str, QShortcut], getattr(namespace, "shortcuts", {}))

    if note_type["type"] != MODEL_CLOZE:
        disable_buttons_and_shortcuts(
            webview=webview, buttons=buttons, shortcuts=list(shortcuts.values())
        )
        return

    if check_model(note_type, fields=False, notify=False):
        hide_anki_cloze_buttons(webview=webview)
        enable_buttons_and_shortcuts(
            webview=webview, buttons=buttons, shortcuts=list(shortcuts.values())
        )
        return

    show_anki_cloze_buttons(webview=webview)

    to_enable = []
    to_disable = []

    for button in buttons:
        if button.cloze_overlapper_exclusive:
            to_disable.append(button)
        else:
            to_enable.append(button)

    enable_buttons_and_shortcuts(
        webview=webview,
        buttons=to_enable,
        shortcuts=[shortcuts[b.cmd] for b in to_enable],
    )

    disable_buttons_and_shortcuts(
        webview=webview,
        buttons=to_disable,
        shortcuts=[shortcuts[b.cmd] for b in to_disable],
    )


def enable_buttons_and_shortcuts(
    webview: "EditorWebView", buttons: List["EditorButton"], shortcuts: List[QShortcut]
):
    for button in buttons:
        webview.eval(
            f"document.getElementById('{button.cmd}').style.display = 'block';"
        )

    for shortcut in shortcuts:
        shortcut.setEnabled(True)


def disable_buttons_and_shortcuts(
    webview: "EditorWebView", buttons: List["EditorButton"], shortcuts: List[QShortcut]
):
    for button in buttons:
        webview.eval(f"document.getElementById('{button.cmd}').style.display = 'none';")

    for shortcut in shortcuts:
        shortcut.setEnabled(False)


def show_anki_cloze_buttons(webview: "EditorWebView"):
    webview.eval(get_anki_cloze_buttons_state_change_command("show"))


def hide_anki_cloze_buttons(webview: "EditorWebView"):
    webview.eval(get_anki_cloze_buttons_state_change_command("hide"))


def get_anki_cloze_buttons_state_change_command(state: Literal["show", "hide"]) -> str:
    return f"""require("anki/ui").loaded.then(() =>
        require("anki/NoteEditor").instances[0].toolbar.toolbar.{state}("cloze"));"""


def get_addon_namespace(name: str, obj: Any) -> SimpleNamespace:
    if namespace := getattr(obj, name, None):
        return namespace
    namespace = SimpleNamespace()
    setattr(obj, name, namespace)
    return namespace


# def handle_cloze_key_conflicts(shortcuts: List[Tuple], editor: "Editor"):
#     filtered_entries: List[Tuple] = []
#     for key, function, *_ in shortcuts:
#         if key in ("Ctrl+Shift+C", "Ctrl+Alt+Shift+C"):
#             continue
