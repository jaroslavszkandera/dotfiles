# -*- coding: utf-8 -*-

# Cloze Overlapper Add-on for Anki
#
# Copyright (C)  2016-2022 Aristotelis P. <https://glutanimate.com/>
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

from anki.hooks import wrap
from aqt.editcurrent import EditCurrent

from ..core.overlapper import ClozeOverlapper
from ..template import check_model
from ..gui.utils import show_tooltip


def on_edit_current(editcurrent: EditCurrent, _old: Callable):
    """Automatically update overlapping clozes when editing cards"""
    editor = editcurrent.editor

    note = editor.note
    if not note:
        return _old(editcurrent)

    model = note.note_type()
    if not model or not check_model(model, notify=False):
        return _old(editcurrent)

    overlapper = ClozeOverlapper(editor.note, silent=True)
    ret, total = overlapper.add()

    # returning here won't stop the window from being rejected, so we simply
    # accept whatever changes the user performed, even if the generator
    # did not fire

    oldret = _old(editcurrent)
    if total:
        show_tooltip("Info", "Updated %d overlapping cloze cards" % total, period=1000)

    return oldret


def initialize_editcurrent():
    EditCurrent._saveAndClose = wrap(
        EditCurrent._saveAndClose, on_edit_current, "around"
    )
