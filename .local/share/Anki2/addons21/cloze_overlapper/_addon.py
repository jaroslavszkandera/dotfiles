# -*- coding: utf-8 -*-

# Cloze Overlapper Add-on for Anki
#
# Copyright (C) 2016-2019  Aristotelis P. <https://glutanimate.com/>
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
Module-level entry point for the add-on into Anki 2.0/2.1
"""

from typing import TYPE_CHECKING

from aqt import mw
from aqt.gui_hooks import profile_did_open

from ._version import __version__  # noqa: F401
from .consts import ADDON
from .libaddon.consts import set_addon_properties

if TYPE_CHECKING:
    assert mw is not None

set_addon_properties(ADDON)

from .gui import initialize_qt_resources
from .gui.options_global import initialize_options
from .integration.addcards import initialize_addcards
from .integration.editcurrent import initialize_editcurrent
from .integration.editor import initialize_editor
from .integration.web import initialize_web_components
from .integration.sched import initialize_scheduler
from .integration.reviewer import initialize_reviewer
from .template import initialize_models

initialize_web_components(addon_manager=mw.addonManager)
initialize_qt_resources()
initialize_options()

profile_did_open.append(initialize_models)

initialize_editor()
initialize_addcards()
initialize_editcurrent()

initialize_scheduler()
initialize_reviewer()
