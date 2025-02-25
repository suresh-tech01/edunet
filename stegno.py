from PIL import Image

def text_to_binary(text):
    """Converts text to binary and adds a null terminator."""
    return ''.join(format(ord(char), '08b') for char in text) + '00000000'  # End marker

def binary_to_text(binary):
    """Converts binary to text, stopping at the first null character."""
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(b, 2)) for b in chars if b != "00000000")  # Stop at null character

def encode_message(image_path, message, output_path):
    """Encodes a message into an image."""
    try:
        img = Image.open(image_path)
        img = img.convert("RGB")  # Ensure it's in RGB mode
        pixels = img.load()
        width, height = img.size

        binary_message = text_to_binary(message)
        index = 0

        for y in range(height):
            for x in range(width):
                if index < len(binary_message):
                    r, g, b = pixels[x, y]
                    new_r = (r & 0xFE) | int(binary_message[index])  # Modify LSB
                    pixels[x, y] = (new_r, g, b)
                    index += 1
                else:
                    img.save(output_path)
                    print(f"✅ Message encoded successfully into {output_path}!")
                    return
        
        print("❌ Message is too long for the image size!")

    except Exception as e:
        print(f"❌ Error: {e}")

def decode_message(image_path):
    """Decodes a message from an image."""
    try:
        img = Image.open(image_path)
        img = img.convert("RGB")  # Ensure correct format
        pixels = img.load()
        width, height = img.size

        binary_message = ""

        for y in range(height):
            for x in range(width):
                r, _, _ = pixels[x, y]
                binary_message += str(r & 1)  # Extract LSB
                
                if len(binary_message) % 8 == 0 and binary_message[-8:] == "00000000":
                    message = binary_to_text(binary_message)
                    print(f"✅ Decoded Message: {message}")
                    return
        
        print("❌ No hidden message found!")

    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    while True:
        print("\n🖼️ Steganography - Hide Secret Messages in Images 🖼️")
        print("1️⃣ Encode a message into an image")
        print("2️⃣ Decode a message from an image")
        print("3️⃣ Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            image_path = input("Enter image filename to encode (e.g., input.png): ")
            message = input("Enter secret message: ")
            output_path = input("Enter output image filename (e.g., output.png): ")
            encode_message(image_path, message, output_path)
        
        elif choice == '2':
            image_path = input("Enter image filename to decode (e.g., output.png): ")
            decode_message(image_path)
        
        elif choice == '3':
            print("👋 Exiting program. Have a great day!")
            break
        
        else:
            print("❌ Invalid choice! Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
