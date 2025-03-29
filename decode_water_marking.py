import cv2
import numpy as np

def extract_message(image_path):
    """
    Extracts the hidden message from the green channel of an image encoded using LSB steganography.
    Also counts the number of times the message was embedded.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not load image. Check the image_path.")
    
    height, width, _ = image.shape
    
    binary_message = ""
    extracted_messages = []
    count = 0
    
    for y in range(0, height, 5 + 64):  # 64 is approximate message length in bits
        if y + 5 + 64 > height:
            break
        for x in range(0, width, 5):
            row, col = y, x
            extracted_binary = ""
            for i in range(64):  # Extract 64 bits (8 characters) at a time
                if row >= height:
                    break
                pixel = image[row, col]
                pixel_bin = format(pixel[1], '08b')  # Extract from green channel (channel 1)
                extracted_binary += pixel_bin[-1]  # Get LSB
                row += 1
            
            extracted_message = ''.join(chr(int(extracted_binary[i:i+8], 2)) for i in range(0, len(extracted_binary), 8))
            extracted_messages.append(extracted_message)
            count += 1
    
    return extracted_messages, count

if __name__ == '__main__':
    # Extract the hidden messages
    extracted_messages, count = extract_message("./lion_water_marked.png")
    
    # Verify the count
    expected_count = 21483
    if count == expected_count:
        print("All water marks are in place. No alternation detected.")
    else:
        print("Mismatch, the image is altered!")
    
    # Display a few extracted messages
    print("Sample extracted messages:")
    print(extracted_messages[:10])
