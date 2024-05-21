# HolidayMicroservice
Microservice that returns the holiday on a given day or month. Uses ZeroMQ, and takes in a string.

# Setup
- Download the .py, .ini, and .txt files (all in the same file)
- Note: You can change the txt file to include more holidays, but make sure to keep it in MM-DD format (with a comma)
- Make sure to download ZeroMQ import before running
- Have the .py file running in another terminal when using it

# Requesting Data
- To request data, send a ZeroMQ Request to the specified port (you can change it in the .ini file)
- In the .py file, make sure to import the request function from your program (I have provided a test file that you can use if you want. I did this to make sure it was in the correct format)
  - The request should be the month followed by the date (if needed). It is not case sensitive, and a space is not needed
  - However, the month should be written out, with the date as a number
  - Call format: socket.send(json.dumps(string).encode("utf-8"))
  - Example Call: socket.send_string("December 25") (for a date) or
  - socket.send_string("December") (for just the month)
  - You don't need to specify date or month. The program will use a date if a number is included in the request, and a month if not.

# Receiving Data
Returned as an array
- An example of how to receive the data:
  - response = socket.recv()
  - final_response = json.loads(response.decode("utf-8"))
