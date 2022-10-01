import gspread


class Worksheet:
    
    def __init__(self, sheet_name: str):
        self.name = sheet_name

    @classmethod
    def from_service_account(cls, spreadsheet_name: str, sheet_name: str):
        sheet = gspread.service_account().open(spreadsheet_name)

        # row = 0
        # for category, amount in spending.items():
        #     worksheet.update_cell(row, 1, category)
        #     worksheet.update_cell(row, 2, round(amount/months, 2))

        # row += 1

        return cls(
            sheet_name=sheet.worksheet(sheet_name)
        )



