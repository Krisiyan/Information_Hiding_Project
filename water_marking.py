import cv2
import numpy as np

def encode_lsb(image_path, output_path):
    """
    Embeds two messages into a color image using Least Significant Bit (LSB) steganography.
    The first message is embedded in the green channel, and the second message in the red channel.
    """
    # Load the color image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not load image. Check the image_path.")
    
    # Convert messages into binary format
    formatted_message = "Original" 
    binary_message = ''.join(format(ord(c), '08b') for c in formatted_message)
    
    height, width, _ = image.shape
    
    # Function to embed a message in a specific color channel
    def embed_message(binary_message, start_row, start_col, channel):
        row, col = start_row, start_col
        data_index = 0
        while data_index < len(binary_message) and row < height and col < width:
            pixel = image[row, col]  # Get the pixel value (in BGR format)
            pixel_bin = format(pixel[channel], '08b')  # Convert the selected channel to binary
            new_pixel_bin = pixel_bin[:-1] + binary_message[data_index]  # Replace LSB
            image[row, col, channel] = int(new_pixel_bin, 2)  # Store it back in the selected channel
            data_index += 1
            row += 1  # Move row by row
    count = 0
    for y in range(0, height, 5 + len(binary_message)):
        if y + 5 + len(binary_message) > height:
            break
        for x in range(0, width, 5):
            # Embed both messages at the selected corners, in green channel
            embed_message(binary_message, *(y, x), channel=1)  # Green channel (channel 1)
            count += 1
        
    # Save the modified image with hidden messages
    cv2.imwrite(output_path, image)
    print(f"Messages embedded successfully in {output_path}")
    print(f"Height: {height}")
    print(f"Width: {width}")
    print(f"Number of embeddings {count}")
    print(f"Length binary message {len(binary_message)}")

if __name__ == '__main__':
    
    # Call the function to embed both messages in the color image
    encode_lsb("./sourceimg/src4.png", "./w4.png")
