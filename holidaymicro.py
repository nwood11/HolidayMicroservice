import zmq
import json
import configparser
# this next line replace with the request from your program
from client import send_request

# checks if there is a date in the request
def check_if_date(req):
    temp = False
    for char in req:
        if char.isdigit():
            temp = True
    return temp

# returns the date portion of the request
def check_date(req):
    date = ""
    for char in req:
        if char.isdigit():
            date = date + char
    return date

# returns the month portion of the request
def check_month(req):
    month = ""
    for char in req:
        if char.isalpha():
            month = month + char.lower()
    return month

# checks if the string is a month
def valid_month(m):
    valid = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    if m in valid:
        return True
    else:
        return False

# assigns a number to the month string
def conv_month(m):
    month_c = {
        'january': 1,
        'february': 2,
        'march': 3,
        'april': 4,
        'may': 5,
        'june': 6,
        'july': 7,
        'august': 8,
        'september': 9,
        'october': 10,
        'november': 11,
        'december': 12
    }
    if m in month_c:
        return month_c[m]
    else:
        return None

def get_holidays(request):
    # open the txt file
    holiday_file = 'holidays.txt'
    
    with open(holiday_file, 'r') as file:
        holidays_data = file.readlines()
    
    # check if the request contains a date, and check if it is a valid month
    checkd = check_if_date(request);
    cmonth = check_month(request);
    validmcheck = valid_month(cmonth);
    if checkd and validmcheck:
        # Handle date
        cdate = check_date(request)
        conv_m = conv_month(cmonth)
        # add leading 0s for txt file
        if len(cdate) == 1:
            cdate_str = '0' + cdate
        else:
            cdate_str = cdate

        if len(str(conv_m)) == 1:
            conv_m_str = '0' + str(conv_m)
        else:
            conv_m_str = str(conv_m)

        # check for what holidays match
        holidays = [holiday.split(',')[1].strip() for holiday in holidays_data if holiday.startswith(f"{conv_m_str}-{cdate_str}")]
    elif validmcheck:
        # Handle month
        conv_m = conv_month(cmonth)
        # add leading zero if needed
        if len(str(conv_m)) == 1:
            conv_m_str = '0' + str(conv_m)
        else:
            conv_m_str = str(conv_m)

        # check for what holidays match
        holidays = [holiday.split(',')[1].strip() for holiday in holidays_data if holiday.split(',')[0].startswith(conv_m_str)]
    else:
        # not a valid month
        return "Invalid Input"

    
    return holidays

# set up server
def run_server(port):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{port}")

    print(f"Server listening on port {port}")

    while True:
        request_bytes = socket.recv()
        request_str = request_bytes.decode("utf-8")
        request = json.loads(request_str)

        holidays = get_holidays(request)
        response = json.dumps(holidays)
        socket.send(response.encode("utf-8"))

# load this first
def main():
    config = configparser.ConfigParser()
    config.read('server.ini')
    port = int(config['Server']['Port'])
    run_server(port)

if __name__ == "__main__":
    main()
