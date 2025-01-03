import gspread
import google.auth as auth

# scope = ['https://spreadsheets.google.com/feeds',
#          'https://www.googleapis.com/auth/drive']
# x = auth.load_credentials_from_file('credentials.json', scopes=scope)
# print(x)
# client = gspread.authorize(x[0])
# print(client.open("SETTLEMENT BOT SHEET").sheet1.get_all_records())


class GSheets:
    columns = ("Team Id", "Team Name", "Leader Name", "Leader Email", "verified_1", "discord_id_1", 
                "Member2 Name", "Member2 Email", "verified_2", "discord_id_2", "Member 3 Name", 
                "Member 3 Email", "verified_3", "discord_id_3", "Member 4 Name", "Member 4 Email", 
                "verified_4", "discord_id_4", "Member 5 Name", "Member 5 Email", "verified_5", 
                "discord_id_5", "Member 6 Name", "Member 6 Email", "verified_6", "discord_id_6", "count")

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
    
    def _format_data_list(self, data: list):
        if int(data[-1]) == 0:
            return None
        return self._make_team_record(data)
    
    def _format_data_dict(self, data: dict):
        if int(data["count"]) == 0:
            return None
        return self._make_team_record(list(data.values()))

    def _make_team_record(self, data: list):
        team_details = {
            "Team Id": data[0],
            "Team Name": data[1],
            "Total Members": data[-1],
            "Members": []
        }
        for i in range(2, len(data)-1, 4):
            if data[i+1] == "-":
                continue
            team_details["Members"].append({
                "name": data[i],
                "email": data[i+1],
                "verified": data[i+2],
                "discord_id": data[i+3]
            })
            if i==2:
                team_details["Members"][0]["leader"] = True

        return team_details
        
    def _reformat_data(self, data:dict):
        """
        data: dict (team details format)
        """
        record = [data["Team Id"], data["Team Name"]]
        for member in data["Members"]:
            if member.get("leader"): # maintaing order, leader first
                record.insert(2, member["name"])
                record.insert(3, member["email"])
                record.insert(4, member["verified"])
                record.insert(5, member["discord_id"])
                continue
            record.append(member["name"])
            record.append(member["email"])
            record.append(member["verified"])
            record.append(member["discord_id"])
        if len(data["Members"]) < 6:
            for i in range(6-len(data["Members"])):
                record.extend(["-", "-", "-", "-"])
        record.append(len(data["Members"]))
        return record


    def get_record_by_team_id(self, team_id):
        team_details = self.sheet.find(str(team_id))
        if not team_details:
            return -1
        return self._format_data_list(list(self.sheet.row_values(team_details.row)))

    def get_team_by_email(self, email):
        member_details = self.sheet.find(email)
        if not member_details:
            return -1
        return self._format_data_list(list(self.sheet.row_values(member_details.row)))

    def get_member_details(self, email):
        member_details = self.sheet.find(email)
        if not member_details:
            return -1
        m = member_details.row
        record = self.sheet.row_values(m)
        name, email, verified, discord_id  = record[record.index(email)-1 : record.index(email)+3]
        return {"name": name, "email": email, "verified": verified, "discord_id": discord_id}

    def get_all_records(self):
        return [self._format_data_dict(i) for i in self.sheet.get_all_records() if i["count"] != 0]
    

    def verify_member(self, email, discord_id):
        email_check = self.sheet.find(email)
        if not email_check:  # Email not found
            return -1
        if self.sheet.find(str(discord_id)):    # User already verified
            return -3
        m = email_check.row
        record = self._format_data_list(list(self.sheet.row_values(m)))
        for member in record["Members"]:
            if member["email"] == email:
                if member["verified"] == "Yes": # Email already verified
                    return -2
                member["verified"] = "Yes"
                member["discord_id"] = str(discord_id)
                break
        
        self.sheet.update([self._reformat_data(record)], f"A{m}:AA{m}")
        return 0

    def unverify_member(self, email):
        email_check = self.sheet.find(email)
        if not email_check:
            return -1

        m = email_check.row
        record = self._format_data_list(list(self.sheet.row_values(m)))

        for member in record["Members"]:
            if member["email"] == email:
                if member["verified"] != "Yes":
                    return -2
                member["verified"] = "-"
                member["discord_id"] = "-"
                break
        self.sheet.update([self._reformat_data(record)], f"A{m}:Z{m}")
        return 0


    def update_record(self, record):
        """
        record: dict (team details format)
        """
        #! REFORMAT
        row = self.sheet.find(record["Team Name"]).row
        # self.sheet.update([list(record.values)], f"A{row}:Q{row}")

if __name__ == "__main__":
    gs = GSheets("SETTLEMENT BOT SHEET", "Sheet1")
    print("Calling get all teams")
    print(gs.get_all_records())