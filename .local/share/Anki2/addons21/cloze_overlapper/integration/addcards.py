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

from typing import TYPE_CHECKING, Callable

from anki.hooks import wrap
from aqt import mw
from aqt.addcards import AddCards

from ..config import config
from ..core.overlapper import ClozeOverlapper
from ..template import check_model
from ..gui.utils import show_tooltip
from .editor import refresh_editor

if TYPE_CHECKING:
    from anki.notes import Note


def on_add_cards(addcards: AddCards, _old: Callable):
    """Automatically generate overlapping clozes before adding cards"""
    editor = addcards.editor

    note = editor.note
    if not note:
        return _old(addcards)

    model = note.note_type()
    if not model or not check_model(model, notify=False):
        return _old(addcards)

    overlapper = ClozeOverlapper(editor.note, silent=True)
    ret, total = overlapper.add()

    if ret is False:
        return

    refresh_editor(editor)

    oldret = _old(addcards)
    if total:
        show_tooltip("Info", "Added %d overlapping cloze cards" % total, period=1000)

    return oldret


def on_add_note(addcards: AddCards, note: "Note", _old: Callable) -> "Note":
    """Suspend full cloze card if option active"""
    note = _old(addcards, note)
    if not note:
        # FIXME: log
        return note

    model = note.note_type()

    if not model or not check_model(model, fields=False, notify=False):
        return note

    sched_conf = config["synced"].get("sched", None)
    if not sched_conf or not sched_conf[2]:
        return note
    maxfields = ClozeOverlapper.get_max_fields(
        note.note_type(), config["synced"]["flds"]["tx"]
    )
    last = note.cards()[-1]
    if last.ord == maxfields:  # is full cloze (ord starts at 0)
        if mw and mw.col:
            mw.col.sched.suspend_cards([last.id])

    return note


def initialize_addcards():
    # AddCard / EditCurrent
    ##########################################################################
    # AddCards.addNote = wrap(AddCards.addNote, on_add_note, "around")
    # always use the methods that are fired on editor save:
    AddCards._add_current_note = wrap(
        AddCards._add_current_note, on_add_cards, "around"
    )
