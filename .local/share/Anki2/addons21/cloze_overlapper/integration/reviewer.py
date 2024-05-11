# -*- coding: utf-8 -*-

# Cloze Overlapper Add-on for Anki
#
# Copyright (C)  2016-2019 Aristotelis P. <https://glutanimate.com/>
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

"""
Additions to Anki's card reviewer
"""

from typing import Callable, List, Tuple

from aqt import mw
from aqt.gui_hooks import state_shortcuts_will_change
from aqt.reviewer import Reviewer

from ..config import config


def on_hint_reveal_hotkey(reviewer: Reviewer):
    if reviewer.state != "answer":
        return
    reviewer.web.eval(
        """\
var btn = document.getElementById("btn-reveal");
if (btn) { btn.click(); };\
"""
    )


def on_state_shortcuts_will_change(state: str, shortcuts: List[Tuple[str, Callable]]):
    if state != "review":
        return
    shortcuts.append(
        (
            config["local"]["hotkey_reveal_cloze_hint"],
            lambda r=mw.reviewer: on_hint_reveal_hotkey(r),  # type: ignore[union-attr]
        )
    )


def initialize_reviewer():
    state_shortcuts_will_change.append(on_state_shortcuts_will_change)
