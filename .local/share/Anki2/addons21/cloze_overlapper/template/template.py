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
Manages note type and templates
"""

from pathlib import Path
from typing import TYPE_CHECKING, Optional

from anki.consts import MODEL_CLOZE
from aqt import mw

from ..config import config
from ..consts import *
from ..gui.utils import show_tooltip, warn_user

if TYPE_CHECKING:
    from anki.collection import Collection
    from anki.models import NoteType

_template_folder = Path(__file__).parent
_front_template = (_template_folder / "front.html.mustache").read_text(encoding="utf-8")
_back_template = (_template_folder / "back.html.mustache").read_text(encoding="utf-8")
_styling = (_template_folder / "styling.css").read_text(encoding="utf-8")


def check_model(model: "NoteType", fields: bool = True, notify: bool = True) -> bool:
    """Sanity checks for the model and fields"""
    mname = model["name"]
    is_olc = False
    # account for custom and imported note types:
    if mname in config["synced"]["olmdls"] or mname.startswith(OLC_MODEL):
        is_olc = True
    if notify and not is_olc:
        olc_types = sorted(set([OLC_MODEL] + config["synced"]["olmdls"]))
        show_tooltip(
            "Reminder",
            "Can only generate overlapping clozes<br>"
            "on the following note types:<br><br>{}".format(
                ", ".join("'{0}'".format(i) for i in olc_types)
            ),
        )
    if not is_olc or not fields:
        return is_olc
    flds = [f["name"] for f in model["flds"]]
    complete = True
    for fid in OLC_FIDS_PRIV:
        fname = config["synced"]["flds"][fid]
        if fid == "tx":
            # should have at least 3 text fields
            complete = all(fname + str(i) in flds for i in range(1, 4))
        else:
            complete = fname in flds
        if not complete:
            break
    if not complete:
        warn_user(
            "Note Type",
            "Looks like your note type is not configured properly. "
            "Please make sure that the fields list includes "
            "all of the following fields:<br><br><i>%s</i>"
            % ", ".join(
                config["synced"]["flds"][fid] if fid != "tx" else "Text1-TextN"
                for fid in OLC_FIDS_PRIV
            ),
        )
    return complete


def add_model(col: "Collection") -> "NoteType":
    """Add add-on note type to collection"""
    models = col.models
    model = models.new(OLC_MODEL)
    model["type"] = MODEL_CLOZE
    # Add fields:
    for field_id in OLC_FLDS_IDS:
        if field_id == "tx":
            for i in range(1, OLC_MAX + 1):
                fld = models.new_field(OLC_FLDS["tx"] + str(i))
                fld["size"] = 12
                models.add_field(model, fld)
            continue
        fld = models.new_field(OLC_FLDS[field_id])
        if field_id == "st":
            fld["sticky"] = True
        if field_id == "fl":
            fld["size"] = 12
        models.add_field(model, fld)
    # Add template
    template = models.new_template(OLC_CARD)
    template["qfmt"] = _front_template
    template["afmt"] = _back_template
    model["css"] = _styling
    model["sortf"] = 1  # set sortfield to title
    models.add_template(model, template)
    models.add(model)
    return model


def update_template(col: "Collection") -> "Optional[NoteType]":
    """Update add-on card templates"""
    print(f"Updating {OLC_MODEL} card template")
    model = col.models.by_name(OLC_MODEL)
    if model is None:
        return None
    template = model["tmpls"][0]
    template["qfmt"] = _front_template
    template["afmt"] = _back_template
    model["css"] = _styling
    col.models.save()
    return model


def initialize_models():
    if not mw or not mw.col:
        return
    model = mw.col.models.by_name(OLC_MODEL)
    if not model:
        model = add_model(mw.col)
