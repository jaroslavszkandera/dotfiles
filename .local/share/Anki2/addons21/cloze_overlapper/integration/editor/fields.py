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


import json
import re
from typing import Any, Callable, Optional, Union

from aqt import mw
from aqt.editor import Editor
from aqt.qt import Qt, QWidget
from aqt.utils import showInfo, tooltip

from ...config import config, create_note_settings, parse_note_settings
from ...core.overlapper import ClozeOverlapper
from ...gui.options_note import OlcOptionsNote
from ...template import check_model
from .helpers import editor_save_then, js_format_field_then, refresh_editor

EDITOR_CALLBACK = Callable[[Editor], Optional[Any]]


@editor_save_then(keep_focus=True)
def insert_overlapping_cloze(editor: Editor, same_card: bool = False):
    note = editor.note
    webview = editor.web
    if not note or not webview:
        return

    # find the highest existing cloze
    highest = 0
    for name, val in note.items():
        m = re.findall(r"\[\[oc(\d+)::", val)
        if m:
            highest = max(highest, sorted([int(x) for x in m])[-1])
    # reuse last?
    if not same_card and (
        not editor.mw.app.keyboardModifiers() & Qt.KeyboardModifier.AltModifier
    ):
        highest += 1
    # must start at 1
    highest = max(1, highest)

    webview.eval("wrap('[[oc%d::', ']]');" % highest)


@editor_save_then()
def insert_multiple_clozes(editor: Editor):
    """Wraps each line in a separate cloze"""
    if not editor.note or not editor.web:
        return

    model = editor.note.note_type()
    if not model:
        return

    # check that the model is set up for cloze deletion
    if not re.search("{{(.*:)*cloze:", model["tmpls"][0]["qfmt"]):
        if editor.addMode:
            tooltip(
                "Warning, cloze deletions will not work until "
                "you switch the type at the top to Cloze."
            )
        else:
            showInfo(
                """\
To make a cloze deletion on an existing note, you need to change it \
to a cloze type first, via Edit>Change Note Type."""
            )
            return
    if check_model(model, fields=False, notify=False):
        cloze_re = r"\[\[oc(\d+)::"
        wrap_pre, wrap_post = "[[oc", "]]"
    else:
        cloze_re = r"\{\{c(\d+)::"
        wrap_pre, wrap_post = "{{c", "}}"
    # find the highest existing cloze
    highest = 0
    for name, val in editor.note.items():
        m = re.findall(cloze_re, val)
        if m:
            highest = max(highest, sorted([int(x) for x in m])[-1])
    increment = False
    if not editor.mw.app.keyboardModifiers() & Qt.KeyboardModifier.AltModifier:
        highest += 1
        increment = True
    highest = max(1, highest)
    # process selected text
    settings = {
        "startIndex": highest,
        "increment": increment,
        "openingMarker": wrap_pre,
        "closingMarker": wrap_post,
    }
    editor.web.eval(f"""clozeOverlapper.clozeMultipleLines({json.dumps(settings)})""")


@editor_save_then()
def invoke_note_options(editor: Editor):
    """Invoke note-specific options dialog"""
    note = editor.note
    webview = editor.web
    if not note or not webview:
        return
    model = note.note_type()
    if not model:
        return
    if not model or not check_model(model):
        return

    settings_field_name: str = config["synced"]["flds"]["st"]
    setopts_in = parse_note_settings(note[settings_field_name])

    options_dialog = OlcOptionsNote(setopts_in, editor.parentWindow)
    options_dialog.exec()

    setopts_out = options_dialog.getSetOpts()

    settings_fld = create_note_settings(setopts_out)
    note[settings_field_name] = settings_fld

    editor.loadNote()

    if editor.currentField is not None:
        webview.eval("focusField(%d);" % editor.currentField)
    else:
        webview.eval("focusField(0);")

    regenerate_clozes(editor, parent=editor.parentWindow)  # type: ignore[call-arg]


@editor_save_then()
def regenerate_clozes(
    editor: Editor, markup: Union[str, bool] = False, parent: Optional[QWidget] = None
) -> Optional[bool]:
    """Invokes an instance of the main add-on class"""
    note = editor.note
    webview = editor.web
    if not note or not webview:  # TODO: log
        return False
    model = note.note_type()
    if not model:
        return False

    if not check_model(model):
        return False

    def onFieldReady():
        overlapper = ClozeOverlapper(editor.note, markup=markup, parent=parent)
        overlapper.add()
        refresh_editor(editor)

    if markup:
        field_map = mw.col.models.fieldMap(model)  # type: ignore[union-attr]
        og_fld_name = config["synced"]["flds"]["og"]
        og_fld_idx = field_map[og_fld_name][0]

        field_commands = [
            "selectAll",
            "insertOrderedList" if markup == "ol" else "insertUnorderedList",
        ]
        return js_format_field_then(webview, og_fld_idx, field_commands, onFieldReady)

    return onFieldReady()


@editor_save_then()
def remove_clozes(editor: Editor):
    """Remove cloze markers and hints from selected text"""
    note = editor.note
    webview = editor.web
    if not note or not webview:
        return

    model = note.note_type()
    if not model:
        return

    is_overlapping_cloze = check_model(model, fields=False, notify=False)
    webview.eval(
        f"""clozeOverlapper.removeClozes({json.dumps(is_overlapping_cloze)})"""
    )
