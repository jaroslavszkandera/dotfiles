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

from typing import TYPE_CHECKING, Any

from aqt.editor import Editor

from ..libaddon.platform import MODULE_ADDON

if TYPE_CHECKING:
    from aqt.addons import AddonManager
    from aqt.webview import WebContent


def inject_editor_script(web_content: "WebContent", context: Any):
    if isinstance(context, Editor):
        web_content.head += f"""\
<script type="module" src="/_addons/{MODULE_ADDON}/web/editor.js"></script>"""


def initialize_web_components(addon_manager: "AddonManager"):
    from aqt.gui_hooks import webview_will_set_content

    addon_manager.setWebExports(__name__, r"web.*")
    webview_will_set_content.append(inject_editor_script)
