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
Modifications to Anki's scheduling
"""

from typing import TYPE_CHECKING, Callable

from anki.consts import QUEUE_TYPE_NEW, QUEUE_TYPE_REV
from anki.hooks import wrap

from ..template import check_model

if TYPE_CHECKING:
    from anki.cards import Card, CardId
    from anki.scheduler.v2 import Scheduler

# FIXME: fix type annotations

# Scheduling


def my_bury_siblings(self: "Scheduler", card: "Card", _old: Callable):
    """Skip sibling burying for our note type if so configured"""
    # <MODIFICATION>
    if self.col is None:
        return _old(self, card)
    if self.col.db is None:
        return _old(self, card)
    if not check_model(card.note_type(), fields=False, notify=False):
        return _old(self, card)
    sched_conf = self.col.conf["olcloze"].get("sched", None)
    if not sched_conf:
        return _old(self, card)

    override_new, override_review, bury_full = sched_conf
    if override_new and override_review:
        # sibling burying disabled entirely
        return

    # </MODIFICATION>

    toBury: list["CardId"] = []
    nconf = self._newConf(card)
    buryNew = nconf.get("bury", True)
    rconf = self._revConf(card)
    buryRev = rconf.get("bury", True)
    # loop through and remove from queues
    for cid, queue in self.col.db.execute(
        f"""
select id, queue from cards where nid=? and id!=?
and (queue={QUEUE_TYPE_NEW} or (queue={QUEUE_TYPE_REV} and due<=?))""",
        card.nid,
        card.id,
        self.today,
    ):
        if queue == QUEUE_TYPE_REV:
            # <MODIFICATION>
            if override_review:
                continue
            # </MODIFICATION>
            queue_obj = self._revQueue
            if buryRev:
                toBury.append(cid)
        else:
            # <MODIFICATION>
            if override_new:
                continue
            # </MODIFICATION>
            queue_obj = self._newQueue
            if buryNew:
                toBury.append(cid)

        # even if burying disabled, we still discard to give same-day spacing
        try:
            queue_obj.remove(cid)
        except ValueError:
            pass
    # then bury
    if toBury:
        self.bury_cards(toBury, manual=False)


def initialize_scheduler():
    try:  # < 23.10
        from anki.scheduler.v2 import Scheduler

        Scheduler._burySiblings = wrap(
            Scheduler._burySiblings, my_bury_siblings, "around"
        )
    except (ImportError, ModuleNotFoundError):
        # TODO: Submit PR for per-notetype burying behavior
        pass
