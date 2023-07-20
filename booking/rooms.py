
def room_full_name(room_number):
    """
    takes customer's choice of a room number and returns room name
    """
    if room_number == 1:
        return "Kew Gardens Suite"
    elif room_number == 2:
        return "Oxford Suite"
    elif room_number == 3:
        return "London Suite"
    elif room_number == 4:
        return "Verulamium Suite"
    elif room_number == 5:
        return "Cambridge Botanic Gardens"
    elif room_number == 6:
        return "Stonehenge Suite"
    elif room_number == 7:
        return "Lucretia's Suite"
    elif room_number == 8:
        return "Glasgow Suite"
    elif room_number == 9:
        return "Ware Suite"


def room_short_name(room_number):
    """
    takes customer's choice of a room number and returns room name
    """
    if room_number == 1:
        return "Kew"
    elif room_number == 2:
        return "Oxford"
    elif room_number == 3:
        return "London"
    elif room_number == 4:
        return "Verulamium"
    elif room_number == 5:
        return "Cambridge"
    elif room_number == 6:
        return "Stonehenge"
    elif room_number == 7:
        return "Lucretia"
    elif room_number == 8:
        return "Glasgow"
    elif room_number == 9:
        return "Ware"


def change_room_name_to_number(room_short):
    """
    takes the room short name and changes it into the number of the room
    """
    if room_short == "Kew":
        return 1
    elif room_short == "Oxford":
        return 2
    elif room_short == "London":
        return 3
    elif room_short == "Verulamium":
        return 4
    elif room_short == "Cambridge":
        return 5
    elif room_short == "Stonehenge":
        return 6
    elif room_short == "Lucretia":
        return 7
    elif room_short == "Glasgow":
        return 8
    elif room_short == "Ware":
        return 9