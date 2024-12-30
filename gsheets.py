import gspread
import google.auth as auth

# scope = ['https://spreadsheets.google.com/feeds',
#          'https://www.googleapis.com/auth/drive']
# x = auth.load_credentials_from_file('credentials.json', scopes=scope)
# print(x)
# client = gspread.authorize(x[0])
# print(client.open("SETTLEMENT BOT SHEET").sheet1.get_all_records())


class GSheets:
    def __init__(self, sheet_name, worksheet):
        __scope = ['https://spreadsheets.google.com/feeds',
                      'https://www.googleapis.com/auth/drive']
        __creds = auth.load_credentials_from_file('credentials.json', scopes=__scope)
        self.client = gspread.authorize(__creds[0])
        self.sheet_name = sheet_name
        self.worksheet = worksheet
        self.sheet = self._open_sheet()


    def _open_sheet(self):
        return self.client.open(self.sheet_name).worksheet(self.worksheet)
    
    def get_record_by_team_id(self, team_id):
        team_details = self.sheet.find(team_id)
        if not team_details:
            return -1
        return self.sheet.row_values(team_details.row)

    def get_team_by_email(self, email):
        member_details = self.sheet.find(email)
        if not member_details:
            return -1
        m = member_details.row
        record = self.sheet.row_values(m)
        return record

    def get_member_details(self, email):
        self.sheet.find(email)
        member_details = self.sheet.find(email)
        if not member_details:
            return -1
        m = member_details.row
        record = self.sheet.row_values(m)
        member_name = record[record.index(email)-1]

        return member_name, record

    def get_all_records(self):
        return self.sheet.get_all_records()
    
    def update_record(self, record):
        """
        record: row (list)
        """
        row = self.sheet.find(record[0]).row
        self.sheet.update([record], f"A{row}:Q{row}")