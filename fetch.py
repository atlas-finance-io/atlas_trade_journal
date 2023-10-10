from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.execution import ExecutionFilter
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time


class IBapi(EWrapper, EClient):
    def __init__(self, sheet):
        EClient.__init__(self, self)
        self.sheet = sheet

    def execDetails(self, reqId: int, contract: Contract, execution):
        # Handle the incoming trade execution data
        trade_data = [
            contract.symbol,
            execution.execId,
            execution.orderId,
            execution.shares,
            execution.price,
            execution.side
        ]
        print(execution)
        self.sheet.append_row(trade_data)


# Google Sheets setup
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "/Users/markwindsor/Desktop/atlas_trade_journal/credentials/atlas-finance-1c813cd5e826.json", scope)
client = gspread.authorize(creds)
sheet = client.open("TradeJournal").sheet1

# IB API setup
app = IBapi(sheet)
app.connect('127.0.0.1', 7496, 123)

# Request trade executions
app.reqExecutions(1, ExecutionFilter())

# Run the loop
app.run()

time.sleep(5)

app.disconnect()
