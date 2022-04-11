#!/usr/bin/python3
import cv2, math, logging, numpy, argparse

parser = argparse.ArgumentParser(description='This program hides images into other images in lossless format.')
parser.add_argument( "-x", "--xcrypt", help='Decrypts or encrypts image using a XOR formula'
                    , metavar="<key>", required=False, default=None)
parser.add_argument( "-d", "--debug", help='Enables debug mode', action="store_true"
                    , required=False)
req_args = parser.add_mutually_exclusive_group(required=True)
req_args.add_argument("-c", "--cloak", help='Cloaks an image in another image'
                      , metavar=('<secret image>','<cover image>',"<output>")
                      , nargs=3)
req_args.add_argument("-r", "--reveal", help="Reveals an image hidden by this program. the output format must match the orginal hidden file format"
                      , metavar=('<target file>',"<output>")
                      , nargs=2)
args = parser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.DEBUG,format='\n%(asctime)s : %(message)s\n')
else:
    logging.basicConfig(level=logging.INFO, format='\n%(asctime)s : %(message)s\n')


def cloak(_secret_image,_new_file_name,_cover_image, _key=''):
    while True:
        with open(_secret_image, "rb") as f:
            image_to_hide_data = f.read()
        if args.xcrypt is not None:
            image_to_hide_data = xor_cryptor(_data=image_to_hide_data,_key=_key)
        image_to_hide_data = [format(hex_byte, '08b') for hex_byte in image_to_hide_data]
        cover_image_data = cv2.imread(_cover_image)
        image_to_hide_info = cv2.imread(_secret_image)
        h_height, h_width, h_color_depth = image_to_hide_info.shape
        logging.debug(f'secret image info:\ncolor depth: {h_color_depth}\nwidth: {h_width}\nheight: {h_height}')
        h_required_pixels = len(image_to_hide_data) * int(h_color_depth)
        logging.debug(f'need at least {h_required_pixels} pixels on the cover image')
        c_height, c_width, c_color_depth = cover_image_data.shape
        logging.debug(f'cover image info:\ncolor depth: {c_color_depth}\nwidth: {c_width}\nheight: {c_height}')
        row_count = math.ceil(h_required_pixels/c_width)
        logging.debug(f'row count is {row_count}')
        bytes_passed_inrow = 0
        byte_count = 0
        new_image_data = cover_image_data
        try:
            for row in range(row_count + 1):
                while(bytes_passed_inrow < c_width and byte_count < len(image_to_hide_data)):
                    byte = image_to_hide_data[byte_count]
                    byte_count += 1
                    for byte_index, byte in enumerate(byte):
                        current_byte = new_image_data[row][bytes_passed_inrow]
                        logging.debug(f'current row is: {row}\n{bytes_passed_inrow} bytes have passed')
                        if (byte == '0'):
                            if (current_byte[byte_index % 3] % 2 == 1):
                                current_byte[byte_index % 3] -= 1
                        elif (byte == '1'):
                            if (current_byte[byte_index % 3] % 2 == 0):
                                current_byte[byte_index % 3] -= 1
                        if (byte_index % 3 == 2):
                            bytes_passed_inrow += 1
                        elif (byte_index == 7):
                            if (byte_count*3 < h_required_pixels):
                                if (current_byte[2] % 2 == 1):
                                    current_byte[2] -= 1
                            elif (byte_count*3 >= h_required_pixels):
                                if (current_byte[2] % 2 == 0):
                                    current_byte[2] -= 1
                            bytes_passed_inrow += 1
                bytes_passed_inrow = 0
        except:
            print('your cover image is not big enough')
            break
        cv2.imwrite(_new_file_name, new_image_data)
        break


def reveal(_target_file, _uncovered_file_name, _key=''):
    target_file_data = cv2.imread(_target_file)
    hidden_file_data = []
    end = False
    for byte_index, byte in enumerate(target_file_data):
        byte.tolist()
        for bit_index, bit in enumerate(byte):
            if (bit_index % 3 == 2):
                hidden_file_data.append(bin(bit[0])[-1])
                hidden_file_data.append(bin(bit[1])[-1])
                if (bin(bit[2])[-1] == '1'):
                    end = True
                    break
            else:
                hidden_file_data.append(bin(bit[0])[-1])
                hidden_file_data.append(bin(bit[1])[-1])
                hidden_file_data.append(bin(bit[2])[-1])
        if end:
            break
    hidden_file_data_array = []
    for byte in range(int((len(hidden_file_data)+1)/8)):
        hidden_file_data_array.append(hidden_file_data[byte*8:(byte*8+8)])
    hidden_file_data = [''.join(byte) for byte in hidden_file_data_array]
    hex_image_data = bytearray()
    for byte in hidden_file_data:
        hex_image_data.append(int(byte, 2))
    if args.xcrypt is not None:
        hex_image_data = xor_cryptor(_data=hex_image_data,_key=_key)
    with open(_uncovered_file_name, "wb") as file:
        file.write(hex_image_data)
        file.close()


def xor_cryptor(_data, _key):
    one_byte_key = sum([ord(char) for char in _key]) % 256
    xor_ed_data=bytearray()
    for byte in _data:
        xor_ed_data.append(byte ^ one_byte_key)
    return xor_ed_data


if __name__ == '__main__':
    if args.cloak is not None:
        if args.xcrypt is None:
            cloak(_secret_image=args.cloak[0], _cover_image=args.cloak[1], _new_file_name=args.cloak[2])
        else:
            cloak(_secret_image=args.cloak[0], _cover_image=args.cloak[1], _new_file_name=args.cloak[2]
                , _key=args.xcrypt)
    elif args.reveal is not None:
        if args.xcrypt is None:
            reveal(_target_file=args.reveal[0],_uncovered_file_name=args.reveal[1])        
        else:
            reveal(_target_file=args.reveal[0],_uncovered_file_name=args.reveal[1], _key=args.xcrypt)

        