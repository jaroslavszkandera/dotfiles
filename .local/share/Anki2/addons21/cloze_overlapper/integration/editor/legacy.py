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

from typing import Callable

from aqt.editor import Editor

from ...template import check_model
from .fields import insert_overlapping_cloze




def on_insert_cloze(editor: Editor, _old: Callable):
    """Editor.onCloze monkey-patch

    Maintained for (partial) compatibility with Customize Keyboard Shortcuts add-on
    """
    note = editor.note
    if not note:
        # TODO: log
        return _old(editor)
    model = note.note_type()
    if not model or not check_model(model, fields=False, notify=False):
        return _old(editor)

    insert_overlapping_cloze(editor)


def legacy_patch_editor_oncloze():
    from anki.hooks import wrap

    try:
        Editor.onCloze = wrap(  # type: ignore[method-assign]
            Editor.onCloze, on_insert_cloze, "around"
        )
    except Exception as e:
        print(f"Could not apply legacy editor patch: {e}")
