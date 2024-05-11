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
Handles add-on configuration
"""


from typing import TYPE_CHECKING, Dict, List, Optional, Tuple

from anki.utils import strip_html  # 2.1.54+
from aqt import mw

from .consts import *
from .libaddon.anki.configmanager import ConfigManager

if TYPE_CHECKING:
    from typing import Literal, TypedDict
else:
    try:
        from typing import Literal, TypedDict
    except ImportError:
        from typing_extensions import Literal, TypedDict


# TODO: Refactor into explicit types
RAW_SETTINGS_TYPE = List[Literal["all", "1", "0"]]
RAW_OPTIONS_TYPE = List[Literal["y", "n"]]

PARSED_SETTINGS_TYPE = List[Optional[int]]
PARSED_OPTIONS_TYPE = List[bool]

SETOPTS_TYPE = Tuple[PARSED_SETTINGS_TYPE, PARSED_OPTIONS_TYPE]


def parse_note_settings(html: str,) -> SETOPTS_TYPE:
    """Return note settings. Fall back to defaults if necessary."""
    settings: Optional[RAW_SETTINGS_TYPE] = None
    options: Optional[RAW_OPTIONS_TYPE] = None
    sets: Optional[PARSED_SETTINGS_TYPE] = None
    opts: Optional[PARSED_OPTIONS_TYPE] = None

    dflt_set: List[Optional[int]] = config["synced"]["dflts"]
    dflt_opt: List[bool] = config["synced"]["dflto"]

    field = strip_html(html)

    lines = field.replace(" ", "").split("|")
    if not lines:
        return (dflt_set, dflt_opt)

    settings = lines[0].split(",")  # type: ignore
    if len(lines) > 1:
        options = lines[1].split(",")  # type: ignore

    if not options and not settings:
        return (dflt_set, dflt_opt)

    if not settings:
        sets = dflt_set
    else:
        sets = []
        for idx, item in enumerate(settings[:3]):
            try:
                sets.append(int(item))
            except ValueError:
                sets.append(None)
        length = len(sets)
        if length == 3 and isinstance(sets[1], int):
            pass
        elif length == 2 and isinstance(sets[0], int):
            sets = [sets[1], sets[0], sets[1]]
        elif length == 1 and isinstance(sets[0], int):
            sets = [dflt_set[0], sets[0], dflt_set[2]]
        else:
            sets = dflt_set

    if not options:
        opts = dflt_opt
    else:
        opts = []
        for i in range(4):
            try:
                if options[i] == "y":
                    opts.append(True)
                else:
                    opts.append(False)
            except IndexError:
                opts.append(dflt_opt[i])

    return (sets, opts)


def create_note_settings(setopts: SETOPTS_TYPE) -> str:
    """Create plain text settings string"""
    set_str = ",".join(str(i) if i is not None else "all" for i in setopts[0])
    opt_str = ",".join("y" if i else "n" for i in setopts[1])
    return set_str + " | " + opt_str


# TODO: Reconsider how to type the current config system

class _SyncedConfigType(TypedDict):
    dflts: PARSED_SETTINGS_TYPE
    dflto: PARSED_OPTIONS_TYPE
    flds: Dict[str, str]
    sched: List[bool]
    olmdls: List[str]
    version: str


class ConfigType(TypedDict):
    local: None
    synced: _SyncedConfigType


# TODO: refactor lists into dicts
# dflts: before, prompt, after
# dflto: no-context-first, no-context-last, gradual ends, no full cloze
# sched: no-siblings new, no-siblings review, auto-suspend full cloze

config_defaults: ConfigType = {
    "local": None,  # read from config.json
    "synced": {
        "dflts": [1, 1, 0],
        "dflto": [False, False, False, False],
        "flds": OLC_FLDS,
        "sched": [True, True, False],
        "olmdls": [OLC_MODEL],
        "version": ADDON.VERSION,
    }
}

config = ConfigManager(mw, config_dict=config_defaults, conf_key="olcloze")
