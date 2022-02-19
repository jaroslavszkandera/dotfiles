from aqt.addcards import AddCards
from aqt.utils import tr, TR
from aqt import gui_hooks


def accept_empty_first_field(problem, note):
    if problem == tr.adding_the_first_field_is_empty():
        # recursive call, so that all hooks are run again, removing this problem.
        return gui_hooks.add_cards_will_add_note(None, note)
    else:
        return problem

gui_hooks.add_cards_will_add_note.append(accept_empty_first_field)
