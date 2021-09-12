from pygsuite import PermissionType

BRIGHT_GREEN_HEX = "#72FF33"


def test_basic_instantiation(test_sheet):
    new_sheet = test_sheet.create_sheet(title="test_sheet", tab_color=BRIGHT_GREEN_HEX)
    test_sheet.flush()
    domain = "@gmail.com"
    test_sheet.share(user=f"pygsuite{domain}", role=PermissionType.WRITER)
