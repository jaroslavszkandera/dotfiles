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

from typing import Any, Callable, List, Optional

from aqt.editor import Editor, EditorWebView

EDITOR_CALLBACK = Callable[[Editor], Optional[Any]]


def editor_save_then(
    keep_focus=False,
) -> Callable[[EDITOR_CALLBACK], EDITOR_CALLBACK]:
    """
    Anki executes JS asynchronously. In order to assure that we are working
    with the most recent field contents, we use a decorator to fire the
    button/hotkey callback after evaluating the pertinent JS:
    """

    def inner(callback: EDITOR_CALLBACK) -> EDITOR_CALLBACK:
        def onSaved(editor: Editor, *args, **kwargs):
            # uses evalWithCallback internally:
            editor.saveNow(
                lambda: callback(editor, *args, **kwargs),  # type: ignore[call-arg]
                keepFocus=keep_focus,
            )

        return onSaved

    return inner


def js_format_field_then(
    webview: EditorWebView, field_idx: int, commands: List[str], callback: Callable
):
    """
    In some cases we need to apply changes to field HTML via JS before
    proceeding:
    """
    cmd_str = "\n".join(
        """document.execCommand("{}");""".format(cmd) for cmd in commands
    )

    js = """
focusField(%(field_idx)d);
%(cmd_str)s
""" % {
        "field_idx": field_idx,
        "cmd_str": cmd_str,
    }

    webview.evalWithCallback(js, lambda res: callback())


def refresh_editor(editor: Editor):
    editor.loadNote()
    focus = editor.currentField or 0
    if not editor.web:
        return
    editor.web.eval("focusField({});".format(focus))
