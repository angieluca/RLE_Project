from console_gfx import ConsoleGfx

dict_hex = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
            '8': 8, '9': 9, 'A': 10, 'a': 10, 'B': 11, 'b': 11, 'C': 12, 'c': 12,
            'D': 13, 'd': 13, 'E': 14, 'e': 14, 'F': 15, 'f': 15}

dict_dec_to_hex = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8,
                   9: 9, 10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f'}


# define a function to print the menu options
def menu_display():
    print("\nRLE Menu")
    print("--------")
    print("0. Exit")
    print("1. Load File")
    print("2. Load Test Image")
    print("3. Read RLE String")
    print("4. Read RLE Hex String")
    print("5. Read Data Hex String")
    print("6. Display Image")
    print("7. Display RLE String")
    print("8. Display Hex RLE Data")
    print("9. Display Hex Flat Data\n")


def to_hex_string(data):  # method 1
    hex_string = ""
    for i in data:
        hex_string += str(hex(i))
    return hex_string.replace("0x","")


def count_runs(flat_data):  # method 2
    count = 1
    num_runs = 0
    for i in range(1, len(flat_data)):
        if flat_data[i] != flat_data[i-1]:
            count += 1
        if flat_data[i] == flat_data[i-1]:
            num_runs += 1
            if num_runs == 15:
                count += 1
                num_runs = 0
                continue
    return count


def encode_rle(flat_data):  # method 3
    count = 1
    encode_list = []
    for i in range(1, len(flat_data)):
        if flat_data[i] == flat_data[i-1]:
            count += 1
            if count > 14:
                encode_list.extend([count, flat_data[i - 1]])
                count = 0
        else:
            encode_list.extend([count, flat_data[i - 1]])
            count = 1
    encode_list.extend([count, flat_data[i]])
    return encode_list


def get_decoded_length(rle_data):  # method 4
    count = 0
    for i in range(0, len(rle_data), 2):
        count += rle_data[i]
    return count


def decode_rle(rle_data):  # method 5
    new_list = []
    for i in range(0, len(rle_data) - 1, 2):
        repeat = rle_data[i]
        value = rle_data[i + 1]
        for times in range(0, int(repeat)):
            new_list.append(value)
    return new_list


def string_to_data(data_string):  # method 6
    hex_list = []
    for i in range(0, len(data_string), 2):
        hex_list.append(dict_hex[data_string[i]])
    return hex_list


def to_rle_string(rle_data):  # method 7
    # change value to hex
    for i in range(0,len(rle_data),2):
        rle_data[i:i+2] = hex(str(rle_data[i:i+2]))
    return rle_data[:-1]  # to not include the final delimiter


def string_to_rle(rle_string):  # method 8
    # remove the colons
    rle_split = rle_string.split(":")
    rle_list = []
    # create a list without the colons
    for element in rle_split:
        first_byte = element[0:-1]
        last_byte = dict_hex[element[-1]]
        rle_list.append(int(first_byte))
        rle_list.append(last_byte)
    return rle_list


def main():
    # welcome message & spectrum img are not in menu_display()
    # since we don't want to call them each time the menu is called
    print("Welcome to the RLE image encoder!")
    print("\n Displaying Spectrum Image:\n")
    ConsoleGfx.display_image(ConsoleGfx.test_rainbow)

    user_input = 0
    image_data = None
    final_image_data = None

    # program loop
    while True:
        menu_display()
        # prompt user for menu selection
        user_input = int(input("Select a Menu Option: "))

        # Exit program
        if user_input == 0:
            break

        # Load file
        elif user_input == 1:
            image_data = None
            final_image_data = None
            final_image_data = ConsoleGfx.load_file(input("Enter name of file to load: "))

        # Load Test Image
        elif user_input == 2:
            final_image_data = ConsoleGfx.test_image
            print("Test image data loaded.")

        # Read RLE String
        elif user_input == 3:
            input_data = input("Enter an RLE string to be decoded: ")
            # use string_to_rle to remove colons and create new list without hex values
            # user decode_rle to change RLE to Flat data
            final_image_data = decode_rle(string_to_rle(input_data))

        # Read RLE Hex String, uses method 6: string_to_data
        elif user_input == 4:
            image_data = str(input("Enter the hex string holding RLE data: "))
            # use string_to_data to change the hex values to decimal like f to 15
            # user decode_rle to change RLE to Flat data
            final_image_data = decode_rle(string_to_data(image_data))
            print(string_to_data(image_data))
            print(final_image_data)

        # Read Flat Data Hex String
        elif user_input == 5:
            image_data = str(input("Enter the hex string holding flat data: "))
            # use method 6 to change flat hexadecimal to byte
            final_image_data = string_to_data(image_data)

        # Display image
        elif user_input == 6:
            print("Displaying image...")
            if final_image_data != None:  # checks first that there is data to decode
                ConsoleGfx.display_image(final_image_data)  #STOPPED HERE FIX THIS!
            else:
                print("(no data)")

        # Display RLE String
        elif user_input == 7:
            if final_image_data != None:  # checks first that there is data to decode
                # calls method 3 to change flat byte to RLE Byte Data
                image_data = encode_rle(final_image_data)
                # calls method 7 to change array to RLE w/ delimiter
                print("RLE representation:", to_rle_string(image_data))
            else:
                print("RLE representation: (no data)")

        # Display Hex RLE Data
        elif user_input == 8:
            if final_image_data != None:  # checks first that there is data to decode
                # calls method 3 to change to RLE Byte Data
                image_data = encode_rle(final_image_data)
                # calls method 1 to change array to string with hex
                print("RLE hex values: ", to_hex_string(image_data))
            else:
                print("RLE hex values: (no data)")

        # Display Hex Flat Data after methods 3-5 were previously called
        elif user_input == 9:
            if final_image_data != None:  # checks first that there is data to decode
                # calls method 1 to change array to string with hex
                print("Flat hex values: ", to_hex_string(final_image_data))
            else:
                print("Flat hex values: (no data)")

        # User input a value outside of menu options
        else:
            print("Error! Invalid input.")


if __name__ == '__main__':
    main()


