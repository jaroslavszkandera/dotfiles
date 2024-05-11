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
Global settings dialog
"""

from typing import cast

from anki.errors import AnkiError
from aqt import mw
from aqt.qt import *

from ..config import config
from ..consts import *
from ..libaddon.gui.about import getAboutString
from .forms import settings_global

hotkeys = [
    "hotkey_generate_clozes",
    "hotkey_open_note_options",
    "hotkey_remove_cloze",
    "hotkey_toggle_ordered_list",
    "hotkey_toggle_unordered_list",
    "hotkey_cloze_multiple_lines",
    "hotkey_reveal_cloze_hint",
]


class OlcOptionsGlobal(QDialog):
    """Global options dialog"""

    def __init__(self, mw):
        super(OlcOptionsGlobal, self).__init__(parent=mw)
        # load qt-designer form:
        self.form = settings_global.Ui_Dialog()
        self.form.setupUi(self)
        self.setupUI()
        self.fndict = list(
            zip(
                (i for i in OLC_FIDS_PRIV if i != "tx"),
                [self.form.le_og, self.form.le_st, self.form.le_fl],
            )
        )
        self.fsched = (self.form.cb_ns_new, self.form.cb_ns_rev, self.form.cb_sfc)
        self.fopts = (
            self.form.cb_ncf,
            self.form.cb_ncl,
            self.form.cb_incr,
            self.form.cb_gfc,
        )
        self.setupValues(config["synced"])
        self.setupHotkeys(config["local"])

    def setupUI(self):
        self.form.buttonBox.accepted.connect(self.onAccept)
        self.form.buttonBox.rejected.connect(self.onReject)
        self.form.buttonBox.button(
            QDialogButtonBox.StandardButton.RestoreDefaults
        ).clicked.connect(self.onRestore)
        about_string = getAboutString()
        self.form.htmlAbout.setHtml(about_string)

    def setupValues(self, values):
        """Set widget values"""
        form = self.form
        before, prompt, after = values["dflts"]
        before = before if before is not None else -1
        after = after if after is not None else -1
        form.sb_before.setValue(before)
        form.sb_after.setValue(after)
        form.sb_cloze.setValue(prompt)
        form.le_model.setText(",".join(values["olmdls"]))
        for idx, cb in enumerate(self.fsched):
            cb.setChecked(values["sched"][idx])
        for idx, cb in enumerate(self.fopts):
            cb.setChecked(values["dflto"][idx])
        for key, fnedit in self.fndict:
            fnedit.setText(values["flds"][key])

    def setupHotkeys(self, local_config: dict):
        for hotkey in hotkeys:
            key_sequence_edit = cast(QKeySequenceEdit, getattr(self.form, hotkey))
            key_sequence_edit.setKeySequence(QKeySequence(local_config[hotkey]))

    def onAccept(self):
        reset_req = False
        try:
            reset_req = self.renameFields()
        except AnkiError:  # rejected full sync warning
            return
        before = self.form.sb_before.value()
        after = self.form.sb_after.value()
        prompt = self.form.sb_cloze.value()
        before = before if before != -1 else None
        after = after if after != -1 else None
        config["synced"]["dflts"] = [before, prompt, after]
        config["synced"]["sched"] = [i.isChecked() for i in self.fsched]
        config["synced"]["dflto"] = [i.isChecked() for i in self.fopts]
        config["synced"]["olmdls"] = self.form.le_model.text().split(",")
        for hotkey in hotkeys:
            key_sequence_edit = cast(QKeySequenceEdit, getattr(self.form, hotkey))
            config["local"][hotkey] = key_sequence_edit.keySequence().toString()
        config.save(reset=reset_req)
        self.close()

    def onRestore(self):
        self.setupValues(config.defaults["synced"])
        self.setupHotkeys(config.defaults["local"])
        for key, lnedit in self.fndict:
            lnedit.setModified(True)

    def onReject(self):
        self.close()

    def renameFields(self):
        """Check for modified names and rename fields accordingly"""
        modified = False
        model = mw.col.models.byName(OLC_MODEL)
        flds = model["flds"]
        for key, fnedit in self.fndict:
            if not fnedit.isModified():
                continue
            name = fnedit.text()
            oldname = config["synced"]["flds"][key]
            if name is None or not name.strip() or name == oldname:
                continue
            idx = mw.col.models.fieldNames(model).index(oldname)
            fld = flds[idx]
            if fld:
                # rename note type fields
                mw.col.models.renameField(model, fld, name)
                # update olcloze field-id <-> field-name assignment
                config["synced"]["flds"][key] = name
                modified = True
        return modified


def invoke_options_global():
    """Invoke global config dialog"""
    dialog = OlcOptionsGlobal(mw)
    return dialog.exec()


def initialize_options():
    config.setConfigAction(invoke_options_global)
    # Set up menu entry:
    options_action = QAction("Cloze Over&lapper Options...", mw)
    options_action.triggered.connect(invoke_options_global)
    mw.form.menuTools.addAction(options_action)
