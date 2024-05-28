import zmq
import json
import configparser

# checks if it is in mm-dd-yyyy or mm-yyyy format
def check_format(stringreq):
    if len(stringreq) == 10:
        return 3
    elif len(stringreq) == 7:
        return 2
    else:
        return 0

# takes the month value of the string (first two chars)
def find_month(monthreq):
    return monthreq[:2]

# handles how the holidays are found for the requested month
def handle_month(requestmonth,holidata):
    correctmonth = find_month(requestmonth)
    holidays = set() # used a set for no duplicate holidays
    for holiday in holidata:
        if holiday.split(',')[0].startswith(correctmonth):
            holidays.add(holiday.split(',')[1].strip())
    holidays = list(holidays)
    return holidays

# handles how the holidays are found for specific dates
def handle_date(requestdate,holidata):
    holidays = [holiday.split(',')[1].strip() for holiday in holidata if holiday.startswith(requestdate)]
    return holidays
    
# main function
def get_holidays(request):
    holiday_file = 'holidays.txt'
    
    with open(holiday_file, 'r') as file:
        holidays_data = file.readlines()
    
    format = check_format(request)
    
    if format != 0: # not invalid
        if format == 3: # if date
            holidays = handle_date(request,holidays_data)
        else: # month
            holidays = handle_month(request,holidays_data)
    else:
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
